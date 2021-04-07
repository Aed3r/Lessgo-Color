/*
     fonctionnaliter : manette de jeu, jouable ecrant tactile ou souris
    */
var canvas, contex;
/*dimention de la fenetre*/
var largeur = 0, hauteur = 0;
/*variable de configuration*/
var dessiner = false;                                       //test si on est entraint de dessiner
var jj = false;                                             //test d'entrer dans la boucle
var xJoy = 100, yJoy = 300;                                     //position x,y joyistick
var xClient = 0, yClient = 0;                                //position souris ou tactile utilisateur
var rayonM = 55, rayonE = 60;                                    //rayon millieu et exterieur joyistick
var dist = 0;                                               //distnance d'un point avec un autre
var pi = Math.PI;                                           //PI
var xBouton = 210, yBouton = 200;                                //poisition x,y bouton
var longeurBouton = 80, largeurBouton = 160;                     //largeur et longeur bouton
var angle, xJoyMouvement, yJoyMouvement, vitesse;

/*lorsque le chargement est fini on fait apparaitre en fondu + les élément de la manette de base*/
function chargementfini() {
    canvas = document.getElementById('canvas');
    context = canvas.getContext('2d');
    //les ecouteurs des entrer ecrant tactile
    document.addEventListener('touchstart', debut);             //executer au toucher
    document.addEventListener('touchend', fin);                 //ececuter quand relacher
    document.addEventListener('touchcancel', fin);              //execution a l'interuption
    document.addEventListener('touchmove', manetteUtiliser);    //executer lors d'un mouvement sur l'ecrant
    /*executer lors du redimentionage de la fenetre*/
    window.addEventListener('resize', redimentionne);
    /*les ecouteur des entrer souris*/
    document.addEventListener('mousedown', debut);              //executer au click souris
    document.addEventListener('mouseup', fin);                  //executer lorsque la souris est relacher
    document.addEventListener('mousemove', manetteUtiliser);    //executer lorsqu'un mouvement de souris est effectuer
    document.body.className += " charger";                      //effet fondu
    redimentionne();
    manetteBase();
}
function manetteBase() {
    fond();
    joystick();
    bouton();
}
function redimentionne() {
    /*full canvas*/
    largeur = (window.innerWidth) - 10;
    hauteur = (window.innerHeight) - 10;
    canvas.width = largeur;
    canvas.height = hauteur;
    /*dimention*/
    if (hauteur < largeur) {                                        //verification si téléphone/tablette/ecrant est en mode "horizontal" et choisit les dimention en sorte d'obtenir le bonne affichage 
        rayonM = (hauteur / 100) * 10;
        rayonE = rayonM - 5;
        longeurBouton = rayonM * 1.5;
        largeurBouton = rayonM * 3;
    } else {                                                        //verification si téléphone/tablette/ecrant est en mode "verticale" et choisit les dimention en sorte d'obtenir le bonne affichage
        rayonM = (largeur / 100) * 10;
        rayonE = rayonM - 5;
        longeurBouton = rayonM * 1.5;
        largeurBouton = rayonM * 3;
    }
    /*pos*/
    xJoy = (largeur / 100) * 80;
    yJoy = (hauteur / 100) * 80;
    xBouton = (largeur / 100) * 20;
    yBouton = yJoy - longeurBouton / 2;
    manetteBase();
}
/*executer si un ecouteur de click est lancer*/
function debut(event) {
    dessiner = true;
    manetteUtiliser(event);
}
/*executer si un ecouteur de relacher click est lancer*/
function fin() {
    if (dessiner) {
        dessiner = false;
        jj = false;
        manetteBase();
        vitesse = 0;
        envoyerDirection(0, 0);
    }
}
/*le fond de la manette, encoche des boutons*/
function fond() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    //joyistick
    context.beginPath();
    context.fillStyle = "#ffffff"
    context.arc(xJoy, yJoy, rayonE, 0, 2 * pi);
    context.fill();
    context.closePath();
    //bouton
    context.fillRect(xBouton, yBouton, largeurBouton, longeurBouton);
}
/*joystick de base et joystickA lorsque selectionner*/
function joystick() {
    context.beginPath();
    context.fillStyle = "#555555"
    context.arc(xJoy, yJoy, rayonM, 0, 2 * pi);
    context.fill();
    context.closePath();
    context.beginPath();
    context.lineWidth = "4";
    context.arc(xJoy, yJoy, rayonM, 0, 2 * pi);
    context.stroke();
    context.closePath();
}
function joystickA(xJoyMouvement, yJoyMouvement) {
    context.beginPath();
    context.fillStyle = "#333333";
    context.arc(xJoyMouvement, yJoyMouvement, rayonM, 0, 2 * pi);
    context.fill();
    context.closePath();
    context.beginPath();
    context.lineWidth = "4";
    context.arc(xJoyMouvement, yJoyMouvement, rayonM, 0, 2 * pi);
    context.stroke();
    context.closePath();
}
/*bouton de base et boutonA lorsque selectionner*/
function bouton() {
    context.fillStyle = "#555555"
    context.fillRect(xBouton + 5, yBouton + 5, largeurBouton - 10, longeurBouton - 10);
    context.strokeRect(xBouton + 5, yBouton + 5, largeurBouton - 10, longeurBouton - 10);
}
function boutonA() {
    context.fillStyle = "#333333";
    context.fillRect(xBouton + 5, yBouton + 5, largeurBouton - 10, longeurBouton - 10);
    context.strokeRect(xBouton + 5, yBouton + 5, largeurBouton - 10, longeurBouton - 10);
}
/*executer lorsque l'ecouteur de mouvement est lancer ou lors d'un apuis bouton, cette fonction est le coeur de la manette*/
function manetteUtiliser(event) {
    if (dessiner) {
        xClient = event.clientX || event.touches[0].clientX;
        yClient = event.clientY || event.touches[0].clientY;
        angle = Math.atan2((yClient - yJoy), (xClient - xJoy));
        dist = Math.sqrt(Math.pow(xClient - xJoy, 2) + Math.pow(yClient - yJoy, 2));
        fond();
        if (((xClient > xBouton + 5) && (xClient < xBouton + largeurBouton)) && ((yClient > yBouton + 5) && (yClient < yBouton + longeurBouton))) {
            boutonA();
        } else {
            bouton();
        }
        if (dist < rayonE) {
            vitesse = parseInt(((dist / rayonE) * 100), 10);                                                      //calcul de la vitesse
            joystickA(xClient, yClient);
            jj = true;
        } else {
            if (jj) {
                xJoyMouvement = rayonE * Math.cos(angle) + xJoy;
                yJoyMouvement = rayonE * Math.sin(angle) + yJoy;
                joystickA(xJoyMouvement, yJoyMouvement);
                // envoyerPosition(xJoyMouvement, yJoyMouvement, vitesse);
                if (angle < 0) {
                    angle += 2 * pi;
                }
            } else {
                joystick();
            }
        }
        envoyerDirection(2 * pi - angle, vitesse);
    }
}