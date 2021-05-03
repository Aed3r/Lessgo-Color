var conn = null;
var msCooldown = 100;
var lastMsg;
var posX = null,
    posY = null;
var resX = null,
    resY = null;
var t1;
var dx, dy;

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
                // On initialise également la position
            case 'position':
                // On arrête le timer et on affiche le ping
                if (t1) document.getElementById("affichagePing").innerHTML = (performance.now() - t1) + "ms";
                // On met à jour la position sur la minimap
                posX = data.x;
                posY = data.y;
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
                let newUrl = window.location.origin + '/introduction.html#skip';
                document.location.href = newUrl;
                break;
            case 'fin':
                // On affiche l'écran de fin de jeu
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
    posX += dx/10000;
    if (posX > 1) posX = 0;
    return posX;
}
function getPosY() {
    posY += dy/10000;
    if (posY > 1) posY = 0;
    return posY;
}

// Renvoie la taille de l'écran (en pixels)
function getResX() {
    return resX;
}
function getResY() {
    return resY;
}
// Déconnecte la connection websocket existante
function disconnect() {
    if (conn != null) {
        console.log("Déconnexion...");
        conn.close();
        conn = null;
    }
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