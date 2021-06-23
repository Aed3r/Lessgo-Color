//3canvas 3context dans lordre miniMap, bouton, joy.
var canvas1, contex1, canvas2, contex2, canvas3, contex3;
//toutes les variable de dimentions et positions sont initialiser et mit a la bonne taille dans la fonction de redimentionnage.
//dimmention que l'on sauvegarde pour ne pas recharger a chaque fois.
var heightCanvas1, widthCanvas1, heightCanvas2, widthCanvas2, heightCanvas3, widthCanvas3;
//largeur et auteur de l'ecran.
var largeur = 0,
    hauteur = 0;
//position x et y ecran.
var xClient = 0,
    yClient = 0;
//position bouton x et y.
var xBouton = 0,
    yBouton = 0;
//taille bouton longeur et largeur.
var longeurBouton = 0,
    largeurBouton = 0;
//position xJoy et yJoy.
var xJoy = 0,
    yJoy = 0;
//position du joyistique effet tirer.
var xJoyMouvement = 0,
    yJoyMouvement = 0;
//dimmention du joyistique.
var rayonInterieur = 0,
    rayonExterieur = 0;
//test si entrer dans boucle.
var jj = false;
var jooy = false;
var dessine = false;
//utiliser pour dessiner le jotistique au bonne endroit effet tirer.
var dist = 0;
var pi = Math.PI;
//position du joueur.
var servPosX = 0,
    servPosY = 0;
var posJX = 0,
    posJY = 0;
var taillePolice = 40;

//lorsque la page est totalement charger avec les 3 canvas on met en place les listener, puis lance la fonction redimentionn pour initialiser les dimmention des different elemeents.
function chargementfini() {
    canvas1 = document.getElementById('canvas1');
    context1 = canvas1.getContext('2d');
    canvas2 = document.getElementById('canvas2');
    context2 = canvas2.getContext('2d');
    canvas3 = document.getElementById('canvas3');
    context3 = canvas3.getContext('2d');
    document.addEventListener('mousedown', debut);
    document.addEventListener('mouseup', fin);
    document.addEventListener('mousemove', utiliser);
    document.body.className += " charger";
    window.addEventListener('resize', redimentionne);
    redimentionne();
    miniMap();
}
//fonction qui met en place tout les elemeent selont les dimention hauteur largeur mode paysage ou normal.
function redimentionne() {
    //recupere dimmention de l'ecrant.
    largeur = (window.innerWidth) - 10;
    hauteur = (window.innerHeight) - 10;
    taillePolice = largeur/100*2;
    //canvas1 qui est la miniMap prend la totaliter de l'écrant.
    canvas1.width = largeur;
    canvas1.height = hauteur;
    if (largeur > hauteur) { //pour gerer le mode paysage ou normal.
        //canvas2 le bouton prend 50% en largeur et toutes la hauteur
        canvas2.width = largeur * 0.5;
        canvas2.height = hauteur;
        //dimmention et position du bouton parraport au canvas qui lui appartiens.
        longeurBouton = canvas2.height * 0.2;
        largeurBouton = canvas2.width * 0.4;
        xBouton = canvas2.width * 0.5 - largeurBouton * 0.5;
        yBouton = canvas2.height * 0.5 - longeurBouton * 0.5;
        //position et dimmention du joyistique parraport au canvas qui lui appartiens.
        canvas3.width = largeur * 0.5;
        canvas3.height = hauteur;
        rayonInterieur = canvas3.height * 0.2;
        rayonExterieur = rayonInterieur + 5;
        xJoy = canvas3.width * 0.5;
        yJoy = canvas3.height * 0.5;
        //affichage sans aucune selection.
        if (!document.fullscreenElement) {
            bouton();
        }
        joystick();
    } else {
        //pareille qu'au dessus avec les dimmentions differents.
        canvas2.width = largeur * 0.5;
        canvas2.height = hauteur;
        longeurBouton = canvas2.width * 0.3;
        largeurBouton = canvas2.width * 0.3;
        xBouton = canvas2.width * 0.5 - largeurBouton * 0.5;
        yBouton = canvas2.height * 0.5 - longeurBouton * 0.5;
        canvas3.width = largeur * 0.5;
        canvas3.height = hauteur;
        rayonInterieur = canvas3.width * 0.2;
        rayonExterieur = rayonInterieur + 5;
        xJoy = canvas3.width * 0.5;
        yJoy = canvas3.height * 0.5;
        if (!document.fullscreenElement) {
            bouton();
        }
        joystick();
    }
    //dimmention des 3 canvas sur lecrant utilisateur utiliser par la suite.
    heightCanvas1 = document.getElementById("canvas1").clientHeight;
    widthCanvas1 = document.getElementById("canvas1").clientWidth;
    heightCanvas2 = document.getElementById("canvas2").clientHeight;
    widthCanvas2 = document.getElementById("canvas2").clientWidth;
    heightCanvas3 = document.getElementById("canvas3").clientHeight;
    widthCanvas3 = document.getElementById("canvas3").clientWidth;
}
//fonction lancer lorsque le listener detecte un debut de mouvement.
function debut(event) {
    dessine = true;
    utiliser(event);
}
//fonction lancer lorsque le listener detecte un fin de mouvement.
function fin(event) {
    dessine = false;
    jj = false;
    jooy = false;
    vitesse = 0;
    envoyerDirection(0, 0);
    utiliser(event);
}
//dessine le bouton pas selectionner dans le canvas 2.
function bouton() {
    context2.clearRect(0, 0, widthCanvas2, heightCanvas2);
    context2.fillStyle = 'rgba(150, 0, 0, 0.5)';
    context2.fillRect(xBouton, yBouton, largeurBouton, longeurBouton);
    context2.lineWidth = "5";
    context2.strokeStyle = 'rgba(150, 0, 0, 1)';
    context2.strokeRect(xBouton + 5, yBouton + 5, largeurBouton - 10, longeurBouton - 10);
    context2.fillStyle = 'rgba(255, 255, 255, 1)';
    context2.font = taillePolice + 'px sans-serif';
    context2.fillText('Plein écran', xBouton + (largeurBouton / 2) - (2.5 * taillePolice), yBouton + (longeurBouton / 2));
}
//dessine le joyistique pas selectionner dans le canvas 3.
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
//dessine le joyistique selectionner dans le canvas 3.
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
//dessine la mini map dans le canvas 1.
function miniMap() {
    servPosX = getPosX();
    servPosY = getPosY();

    posJX = servPosX * widthCanvas1;
    posJY = servPosY * heightCanvas1;

    context1.clearRect(0, 0, widthCanvas1, heightCanvas1);
    context1.beginPath();
    context1.fillStyle = getColor();
    context1.arc(posJX, posJY, 10, 0, 2 * pi);
    context1.fill();
    context1.lineWidth = 2;
    context1.strokeStyle = 'darkslategray';
    context1.stroke();
    setTimeout('miniMap()', 50);
}
//fonction principale qui gere les evenement, et affiche les bons élémenets selon la situation.
function utiliser(event) {
    if (dessine) {
        //recupere position utilisateur.
        xClient = event.clientX;
        yClient = event.clientY;
        //position utilisateur pour le canvas du joyistique
        xClientJoy = (xClient - largeur + widthCanvas2);
        yClientJoy = (yClient - hauteur + heightCanvas1);
        //si le client est dans le canvas du bouton
        if (xClient > 0 && xClient < widthCanvas2) {
            if (((xClient > xBouton + 5) && (xClient < xBouton + largeurBouton)) && ((yClient > yBouton + 5) && (yClient < yBouton + longeurBouton))) {
                if (!document.fullscreenElement) {
                    document.documentElement.requestFullscreen();
                }
            }
        }
        //si le client est dans le canvas du joyistique
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
        //envoie au serveure l'angle et la vitesse du mouvement.
        if (angle) envoyerDirection(angle, vitesse);
    }
    if (!jooy) {
        joystick();
    }
}