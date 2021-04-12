var conn = null;
var msCooldown = 100;
var lastMsg;
var posX = null, posY = null;
var resX = null, resY = null;
var t1;

// Envoi la direction choisie par le joueur au serveur
function envoyerDirection(angle, vitesse) {
    // Vérifications
    if (angle == null || vitesse == null)
        return;

    // On calcule le déplacement à effectuer 
    var dx = parseInt(Math.cos(angle) * vitesse);
    var dy = parseInt(Math.sin(angle) * vitesse);

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
    console.log("Envoi du paquet " + msg);

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
        console.log("Paquet Reçu: " + e.data);

        var data = JSON.parse(e.data);

        switch (data.action) {
            case 'init':
                resX = data.resX; 
                resY = data.resY;
            case 'position':
                // On arrête le timer et on affiche le ping
                if (t1) document.getElementById("affichagePing").innerHTML = (performance.now() - t1) + "ms";
                posX = data.x;
                posY = data.y;
                break;
            case 'go':
                window.location.pathname = '/manette.html';
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
    return posX;
}
function getPosY() {
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

connect();