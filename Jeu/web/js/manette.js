var canvas1, contex1, canvas2, contex2, canvas3, contex3;
var heightCanvas1, widthCanvas1, heightCanvas2, widthCanvas2, heightCanvas3, widthCanvas3;
var largeur = 0,
    hauteur = 0;
var xClient = 0,
    yClient = 0;
var xBouton = 0,
    yBouton = 0;
var longeurBouton = 0,
    largeurBouton = 0;
var xJoy = 0,
    yJoy = 0;
var xJoyMouvement = 0,
    yJoyMouvement = 0;
var rayonInterieur = 0,
    rayonExterieur = 0;
var jj = false;
var jooy = false;
var bout = false;
var dessine = false;
var dist = 0;
var pi = Math.PI;
var i = 0;
var servPosX = 0,
    servPosY = 0;
var posJX = 0,
    posJY = 0;

function chargementfini() {
    canvas1 = document.getElementById('canvas1');
    context1 = canvas1.getContext('2d');
    canvas2 = document.getElementById('canvas2');
    context2 = canvas2.getContext('2d');
    canvas3 = document.getElementById('canvas3');
    context3 = canvas3.getContext('2d');
    document.addEventListener('touchstart', debut);
    document.addEventListener('touchmove', debut);
    canvas2.addEventListener('touchend', finBouton);
    canvas2.addEventListener('touchcancel', finBouton);
    canvas3.addEventListener('touchend', finJoy);
    canvas3.addEventListener('touchcancel', finJoy);
    document.body.className += " charger";
    window.addEventListener('resize', redimentionne);
    redimentionne();
    miniMap();
}

function redimentionne() {
    largeur = (window.innerWidth)-10;
    hauteur = (window.innerHeight)-10;
    canvas1.width = largeur;
    canvas1.height = hauteur;
    if (largeur > hauteur) {
        canvas2.width = largeur * 0.5;
        canvas2.height = hauteur;
        longeurBouton = canvas2.height * 0.2;
        largeurBouton = canvas2.width * 0.4;
        xBouton = canvas2.width * 0.5 - largeurBouton * 0.5;
        yBouton = canvas2.height * 0.5 - longeurBouton * 0.5;
        canvas3.width = largeur * 0.5;
        canvas3.height = hauteur;
        rayonInterieur = canvas3.height * 0.2;
        rayonExterieur = rayonInterieur + 5;
        xJoy = canvas3.width * 0.5;
        yJoy = canvas3.height * 0.5;
        bouton();
        joystick();
    } else {
        canvas2.width = largeur * 0.5;
        canvas2.height = hauteur;
        longeurBouton = canvas2.width * 0.2;
        largeurBouton = canvas2.height*0.4;
        xBouton = canvas2.width * 0.5 - largeurBouton * 0.5;
        yBouton = canvas2.height * 0.5 - longeurBouton * 0.5;
        canvas3.width = largeur * 0.5;
        canvas3.height = hauteur;
        rayonInterieur = canvas3.width * 0.2;
        rayonExterieur = rayonInterieur + 5;
        xJoy = canvas3.width * 0.5;
        yJoy = canvas3.height*0.5;
        bouton();
        joystick();
    }
    heightCanvas1 = document.getElementById("canvas1").clientHeight;
    widthCanvas1 = document.getElementById("canvas1").clientWidth;
    heightCanvas2 = document.getElementById("canvas2").clientHeight;
    widthCanvas2 = document.getElementById("canvas2").clientWidth;
    heightCanvas3 = document.getElementById("canvas3").clientHeight;
    widthCanvas3 = document.getElementById("canvas3").clientWidth;
}

function debut(event) {
    dessine = true;
    utiliser(event);
}

function finBouton(event) {
    dessine = false;
    bout = false;
    utiliser(event);
}

function finJoy(event) {
    dessine = false;
    jj = false;
    jooy = false;
    vitesse = 0;
    envoyerDirection(0, 0);
    utiliser(event);
}

function bouton() {
    context2.clearRect(0, 0, widthCanvas2, heightCanvas2);
    context2.fillStyle = 'rgba(150, 0, 0, 0.5)';
    context2.fillRect(xBouton, yBouton, largeurBouton, longeurBouton);
    context2.lineWidth = "5";
    context2.strokeStyle = 'rgba(150, 0, 0, 1)';
    context2.strokeRect(xBouton + 5, yBouton + 5, largeurBouton - 10, longeurBouton - 10);
}

function boutonA() {
    context2.clearRect(0, 0, widthCanvas2, heightCanvas2);
    context2.fillStyle = 'rgba(250, 0, 0, 0.5)';
    context2.fillRect(xBouton, yBouton, largeurBouton, longeurBouton);
    context2.lineWidth = "5";
    context2.strokeStyle = 'rgba(250, 0, 0, 1)';
    context2.strokeRect(xBouton + 5, yBouton + 5, largeurBouton - 10, longeurBouton - 10);
    bout = true;
}

function joystick() {
    context3.clearRect(0, 0, widthCanvas3, heightCanvas3);
    context3.beginPath();
    context3.fillStyle = 'rgba(150, 0, 0, 0.5)';
    context3.arc(xJoy, yJoy, rayonInterieur, 0, 2 * pi);
    context3.fill();
    context3.closePath();
    context3.beginPath();
    context3.strokeStyle = 'rgba(150, 0, 0, 1)';
    context3.lineWidth = "5";
    context3.arc(xJoy, yJoy, rayonInterieur + 1, 0, 2 * pi);
    context3.stroke();
    context3.closePath();
}

function joystickA(xJoyMouvement, yJoyMouvement) {
    context3.clearRect(0, 0, widthCanvas3, heightCanvas3);
    context3.beginPath();
    context3.fillStyle = 'rgba(255, 0, 0, 0.5)';
    context3.arc(xJoyMouvement, yJoyMouvement, rayonInterieur, 0, 2 * pi);
    context3.fill();
    context3.closePath();
    context3.beginPath();
    context3.strokeStyle = 'rgba(255, 0, 0, 1)';
    context3.lineWidth = "5";
    context3.arc(xJoyMouvement, yJoyMouvement, rayonInterieur + 1, 0, 2 * pi);
    context3.stroke();
    context3.closePath();
    jooy = true;
}

function miniMap() {
    servPosX = getPosX();
    servPosY = getPosY();

    posJX = servPosX * widthCanvas1;
    if (posJX > widthCanvas1) {
        posJX - widthCanvas1;
    }
    posJY = servPosY * heightCanvas1;
    if (posJY > heightCanvas1) {
        posJY - heightCanvas1;
    }

    context1.clearRect(0, 0, widthCanvas1, heightCanvas1);
    context1.beginPath();
    context1.fillStyle = 'rgba(100, 100, 100, 1)';
    context1.arc(posJX, posJY, 10, 0, 2 * pi);
    context1.fill();
    context1.closePath();
    setTimeout('miniMap()', 50);
}

function utiliser(event) {
    if (dessine) {
        for (i = 0; i < event.touches.length; i++) {
            xClient = event.touches[i].clientX;
            yClient = event.touches[i].clientY;
            xClientJoy = (xClient - largeur + widthCanvas2);
            yClientJoy = (yClient - hauteur + heightCanvas1);
            if (xClient > 0 && xClient < widthCanvas2) {
                if (((xClient > xBouton + 5) && (xClient < xBouton + largeurBouton)) && ((yClient > heightCanvas1 + yBouton + 5) && (yClient < heightCanvas1 + yBouton + longeurBouton))) {
                    boutonA();
                    if (!document.fullscreenElement) {
                        document.documentElement.requestFullscreen();
                    }
                }
            }
            if (xClient > widthCanvas2 && xClient < largeur) {
                angle = Math.atan2((yClientJoy - yJoy), (xClientJoy - xJoy));
                dist = Math.sqrt(Math.pow(xClientJoy - xJoy, 2) + Math.pow(yClientJoy - yJoy, 2));
                if (dist < rayonExterieur) {
                    vitesse = parseInt(((dist / rayonExterieur) * 100), 10);
                    joystickA(xClientJoy, yClientJoy);
                    jj = true;
                } else {
                    if (jj) {
                        xJoyMouvement = rayonExterieur * Math.cos(angle) + xJoy;
                        yJoyMouvement = rayonExterieur * Math.sin(angle) + yJoy;
                        joystickA(xJoyMouvement, yJoyMouvement);
                        if (angle < 0) {
                            angle += 2 * pi;
                        }
                    }
                }
            }
        }
        envoyerDirection(angle, vitesse);
    }
    if (!jooy) {
        joystick();
    }
    if (!bout) {
        bouton();
    }
}