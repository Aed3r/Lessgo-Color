var destinationX = null, destinationY = null;
var res = null;
const minAcceptDist = 20;
var timeoutHandler = null;

function getRandomPos() {
    while (res == null) res = getRes();

    destinationX = Math.floor(Math.random() * res.x);
    destinationY = Math.floor(Math.random() * res.y);
}

function distanceToDest () {
    let pos = null;
    while (pos == null) pos = getRealPos();
    let dist = Math.sqrt(Math.pow(destinationX - pos.x, 2)+Math.pow(destinationY - pos.y, 2));
    return dist;
}

function sendStep() {
    let dest = distanceToDest();
    if (destinationX == null || dest < minAcceptDist) getRandomPos();

    let pos = null;
    while (pos == null) pos = getRealPos();

    let angle = Math.atan2(destinationY-pos.y, destinationX-pos.x);
    
    if (angle < 0) angle += 2 * Math.PI;

    let vitesse = Math.floor((Math.random() / 2 + 0.5) * 100);
    if (dest < vitesse) vitesse = dest;

    envoyerDirection(angle, vitesse);
    timeoutHandler = setTimeout(sendStep, getCooldown());
}

function stopBot() {
    clearTimeout(timeoutHandler);
}

function botIntro() {
    let packet = {action:"init", team:0, nom:"bot", estBot:1};
    envoyerPaquet(packet, true);
    setReady();
    let endUrl = window.location.origin + '/bot.html#intro';
    document.location.href = endUrl;
}