var conn = null;
const msCooldown = 100;
var lastMsg;
var posX = null,
    posY = null;
var resX = null,
    resY = null;
var t1;
var dx, dy;
var team = null, color = null;
var powerupNames = ["gottaGoFast", "mildPower", "paintMore"];
var powerupImages = {};
const tailleImagesPowerup = 0.2;
var activePU = null;
var wraparound = false;

// Envoi la direction choisie par le joueur au serveur
function envoyerDirection(angle, vitesse) {
    // Vérifications
    if (angle == null || vitesse == null)
        return;

    // On calcule le déplacement à effectuer 
    dx = parseInt(Math.cos(angle) * vitesse);
    dy = parseInt(Math.sin(angle) * vitesse);

    // On prépare le paquet à envoyer
    var paquet = { "action": "deplacement", dx, dy };
    envoyerPaquet(paquet);

    // On démarre un timer
    t1 = performance.now();
}

// Envoi le paquet donné au serveur si assez de temps s'est écoulé depuis le dernier
function envoyerPaquet(packet) {
    // Vérification du cooldown
    let now = Date.now();
    if ((now < lastMsg + msCooldown && vitesse != 0))
        return;

    // On prépare le paquet à envoyer
    var msg = JSON.stringify(packet);

    // On envoie le paquet
    if (conn != null)
        conn.send(msg);
    else
        console.error("Erreur! Connection non initialisé");
    lastMsg = now;
}

// Etablie une connection websocket au serveur
function connect() {
    disconnect();
    var wsUri = (window.location.protocol == 'https:' && 'wss://' || 'ws://') + window.location.host;
    conn = new WebSocket(wsUri);

    console.log("Tentative de connection...");

    // Lorsque la connection est établie
    conn.onopen = function() {
        console.log("Connection établie.");
    };

    // Lorsqu'un message est reçue
    conn.onmessage = function(e) {
        var data = JSON.parse(e.data);

        switch (data.action) {
            case 'init':
                resX = data.resX;
                resY = data.resY;
                team = data.team;
                color = data.color;
                // On initialise également la position
            case 'update':
                // On arrête le timer et on affiche le ping
                if (t1) document.getElementById("affichagePing").innerHTML = (performance.now() - t1) + "ms";

                // On met à jour la position sur la minimap
                posX = data.x;
                posY = data.y;

                // On charge les images correspondant aux powerup actifs s'il y a eu un changement
                if (data.pu && data.pu != [] && (activePU == null || activePU != data.pu)) {
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
                break;
            case 'go':
                // Le jeu est lancé, on affiche la manette suivant l'appareil utilisé
                let device = getDeviceType()
                if (device == "mobile" || device == "tablet")
                    window.location.pathname = '/manette.html';
                else
                    window.location.pathname = '/manette_pc.html';
                break;
            case 'attente':
                // On revient à l'écran d'attente
                let waitUrl = window.location.origin + '/introduction.html#skip';
                document.location.href = waitUrl;
                location.reload();
                break;
            case 'fin':
                // On affiche l'écran de fin de jeu
                let isWinner = null;
                if (team != null) isWinner = data.winner == team;

                let endUrl = window.location.origin + '/introduction.html#end#' + data.winner + '#' + isWinner;
                document.location.href = endUrl;
                break;
            default:
                return;
        }
    };

    // Lorsque la connection est fermé par le serveur
    conn.onclose = function() {
        console.log("Connection fermé.")
        conn = null;
    };
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

// Renvoie la taille de l'écran (en pixels)
function getResX() {
    return resX;
}

function getResY() {
    return resY;
}

function getColor() {
    if (color) return "rgb("+color[0]+","+color[1]+","+color[2]+")";
    else return 'rgba(100, 100, 100, 1)';
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

connect();