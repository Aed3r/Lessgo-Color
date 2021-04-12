var conn = null;
var msCooldown = 100;
var lastMsg;
var pos = null
var res = null

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
                res = (data.resX, data.resY);
            case 'position':
                pos = (data.x, data.y);
                break;
            case 'go':
                window.location.pathname = '/manette.html';
        }
    };

    // Lorsque la connection est fermé par le serveur
    conn.onclose = function() {
        console.log("Connection fermé.")
        conn = null;
    };
}

// Renvoie la position actuel du joueur (en % de l'écran)
function getPos() {
    return pos;
}

// Renvoie la taille de l'écran (en pixels)
function getRes() {
    return res;
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