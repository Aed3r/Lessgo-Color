var conn = null;
var msCooldown = 100;
var lastMsg;
var posX = null,
    posY = null;
var resX = null,
    resY = null;
var t1;
var dx, dy;
var team = null, color = null, nom = null;
var powerupNames = ["gottaGoFast", "mildPower", "paintMore", "paintMoreGold", "gottaGoFastGold"];
var powerupImages = {};
const tailleImagesPowerup = 0.2;
var activePU = null;
var wraparound = false;
const afficherPing = true;
var lastPing = -1;
var ready = false;
var isEndCard = false;
var isBot = (document.location.pathname == "/bot.html");

/* Initialisations */
if (!afficherPing) t1.style.visibility = "hidden"
let params = new URLSearchParams(document.location.search.substring(1));
nom = params.get("nom");
if (nom != null) {
    document.getElementById("pseudoBox").value = nom;
}

// Envoi la direction choisie par le joueur au serveur
function envoyerDirection(angle, vitesse) {
    // Vérifications
    if (angle == null || vitesse == null)
        return;
    
    // On calcule le déplacement à effectuer 
    dx = Math.round(Math.cos(angle) * vitesse);
    dy = Math.round(Math.sin(angle) * vitesse);

    // On prépare le paquet à envoyer
    let paquet = { "action": "deplacement", dx, dy };
    if (dx == 0 && dy == 0)
        envoyerPaquet(paquet, true);
    else
        envoyerPaquet(paquet, false);
}

// Envoi le paquet donné au serveur si assez de temps s'est écoulé depuis le dernier
function envoyerPaquet(packet, force) {
    // Vérification du cooldown
    let now = Date.now();
    if (!force && now < lastMsg + msCooldown)
        return;

    // On ajoute le dernier ping
    packet["ping"] = lastPing;

    // On prépare le paquet à envoyer
    var msg = JSON.stringify(packet);

    // On envoie le paquet
    if (conn != null && conn.readyState == 1)
        conn.send(msg);
    else
        console.error("Erreur! Connection non initialisé");

    // On démarre un timer pour calculer le prochain ping
    t1 = performance.now();

    lastMsg = now;
}

// Etablie une connection websocket au serveur
function connect() {
    disconnect();
    var wsUri = (window.location.protocol == 'https:' && 'wss://' || 'ws://') + window.location.host;
    conn = new WebSocket(wsUri);

    console.log("Tentative de connection...");

    // Lorsque la connection est établie
    conn.onopen = function () {
        console.log("Connection établie.");

        if (isBot) {
            // On vérifie s'il faut introduire le bot au serveur ou non
            let hash = location.hash.split('#');

            if (!(hash && hash.length > 0 && hash[1] == "intro"))
                botIntro();
            else // On enlève le hash
                history.pushState("", document.title, window.location.pathname);
        }
    };

    // Lorsqu'un message est reçue
    conn.onmessage = function (e) {
        var data = null;
        try {
            data = JSON.parse(e.data);
        } catch (e) {
            console.error("Invalid json packet received : '" + e.data + "'");
            return;
        }

        if (!data || !data.action) return;

        switch (data.action) {
            case 'init':
                resX = data.resX;
                resY = data.resY;
                team = data.team;
                color = data.color;
                msCooldown = data.coolDown;
                nom = data.nom;
                if (isEndCard) {
                    document.getElementById("contentQuestion").innerHTML = "Vous avez colorié <b>" + data.score + "</b> cases!"
                }
            // VVV On initialise également la position VVV
            case 'update':
                // On met à jour la position sur la minimap
                posX = data.x;
                posY = data.y;

                // On lance le bot après initialisation
                if (data.action == "init" && isBot) sendStep();

                // On charge les images correspondant aux powerup actifs s'il y a eu un changement
                if (!isBot && data.pu && data.pu != [] && (activePU == null || activePU != data.pu)) {
                    activePU = data.pu
                    // On enlève les anciennes images
                    let puDisplay = document.getElementById("powerUpDisplay");
                    while (puDisplay.hasChildNodes()) {
                        puDisplay.removeChild(puDisplay.lastChild);
                    }
                    // On ajoute les nouvelles
                    data.pu.forEach(pu => {
                        let img = powerupImages[pu].cloneNode(false);
                        puDisplay.appendChild(img);
                    });
                }
            // VVV On met également à jour le dernier ping VVV
            case 'stresstest':
                // On arrête le timer et on affiche le ping
                if (t1) {
                    lastPing = performance.now() - t1;
                    if (afficherPing) document.getElementById("affichagePing").innerHTML = lastPing + "ms";
                } else lastPing = -1;
                break;
            case 'go':
                // On ne lance le jeu que si le joueur a choisit un nom et une équipe
                if (!ready) return;
                // On redirige les bots sur eux même
                if (isBot) {
                    location.reload();
                    return;
                }
                // Le jeu est lancé, on affiche la manette suivant l'appareil utilisé
                let device = getDeviceType()
                if (device == "mobile" || device == "tablet")
                    window.location.pathname = '/manette.html';
                else
                    window.location.pathname = '/manette_pc.html';
                break;
            case 'attente':
                if (isBot) {
                    // On revient à l'écran d'attente 'bot'
                    location.reload();
                } else {
                    // On revient à l'écran d'attente
                    let waitUrl = window.location.origin + '/introduction.html';
                    if (nom != null) waitUrl += '?nom=' + nom;
                    document.location.href = waitUrl;
                    //location.reload();
                }
                break;
            case 'fin':
                if (isBot) {
                    stopBot();
                } else {
                    // On affiche l'écran de fin de jeu
                    let isWinner = null;
                    if (team != null) isWinner = data.winner == team;

                    let endUrl = window.location.origin + '/introduction.html#end#' + data.winner + '#' + isWinner;
                    document.location.href = endUrl;
                }
                break;
            case 'newCooldown':
                msCooldown = data.coolDown;
                console.log("cooldown: " + msCooldown + "ms");
                break;
            default:
                return;
        }
    };

    // Lorsque la connection est fermé par le serveur
    conn.onclose = function () {
        console.log("Connection fermé.");
        conn = null;
    };
}

function randomInt() {
    return Math.floor(Math.random() * 100000);
}

// Envoie des paquets aléatoire en continue
function stressTest() {
    let val1 = randomInt(), val2 = randomInt();
    let paquet = { "action": "stresstest", val1, val2 };
    envoyerPaquet(paquet, true);
    setTimeout(stressTest, msCooldown);
}

// Renvoie la position actuel du joueur (en % de l'écran)
function getPosX() {
    posX += dx / 10000;
    if (wraparound) {
        if (posX > 1) posX = 0;
        else if (posX < 0) posX = 1;
    } else {
        if (posX > 1) posX = 1;
        else if (posX < 0) posX = 0;
    }
    return posX;
}

function getPosY() {
    posY += dy / 10000;
    if (wraparound) {
        if (posY > 1) posY = 0;
        else if (posY < 0) posY = 1;
    } else {
        if (posY > 1) posY = 1;
        else if (posY < 0) posY = 0;
    }
    return posY;
}

// Renvoie la position sur le plateau de jeu
function getRealPos() {
    if (posX == null) return null;
    else return { x: posX*resX, y: posY*resY };
}

// Renvoie la taille de l'écran (en pixels)
function getResX() {
    return resX;
}

function getResY() {
    return resY;
}

function getRes() {
    if (resX == null) return null;
    return { x: resX, y: resY };
}

function getColor() {
    if (color) return "rgb(" + color[0] + "," + color[1] + "," + color[2] + ")";
    else return 'rgba(100, 100, 100, 1)';
}

function getCooldown() {
    return msCooldown;
}

// Déconnecte la connection websocket existante
function disconnect() {
    if (conn != null) {
        console.log("Déconnexion...");
        conn.close();
        conn = null;
    }
}

// Chargement paresseux des images de powerUp
async function loadImages() {
    powerupNames.forEach(pu => {
        let tmp = new Image();
        tmp.src = pu + ".png";
        powerupImages[pu] = tmp;
    });
}

// Indique qu'il s'agit de l'écran de fin
function setEndCard() {
    isEndCard = true;
}

// On ne charge les images que si le jeu est lancé
if (window.location.pathname[1] == "m") {
    loadImages();
}

// Vérifie si l'appareil actuel est un smartphone ou une tablette
// https: //dev.to/itsabdessalam/detect-current-device-type-with-javascript-490j
const getDeviceType = () => {
    const ua = navigator.userAgent;
    if (/(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(ua)) {
        return "tablet";
    }
    if (
        /Mobile|iP(hone|od)|Android|BlackBerry|IEMobile|Kindle|Silk-Accelerated|(hpw|web)OS|Opera M(obi|ini)/.test(
            ua
        )
    ) {
        return "mobile";
    }
    return "desktop";
};

function setReady() {
    ready = true;
}

connect();