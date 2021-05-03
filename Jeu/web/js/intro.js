var packet = {} // Le paquet envoyé au serveur
var step = 0; // Evite les accidents

// Place la div principale verticalement
function alignBox() {
    var box = document.getElementById("mainDiv");
    mainDiv.style.marginTop = Math.round(window.innerHeight / 2 - box.clientHeight / 2) + 'px';
}

// Met à jour l'emplacement de la div principale lors de redimensionnement
window.addEventListener("load", function() {
    alignBox();
});

// Enregistre le nom choisie et charge la sélection de l'équipe
function choisirNom() {
    var textBox = document.getElementById("pseudoBox");

    if (step == 0) step++;
    else return;

    // Vérifie si le nomp est valide
    if (isNullOrWhitespace(textBox.value)) {
        textBox.classList.add("invalidEntry");
        textBox.value = "";
        return;
    }

    packet["nom"] = textBox.value;

    // On cache l'entré courante
    var namePicker = document.getElementById("namePicker");
    namePicker.style.display = "none";

    // On affiche la nouvelle entré
    var teamPicker = document.getElementById("teamPicker");
    teamPicker.style.position = "static";
    teamPicker.style.opacity = "1";
    alignBox();

    // On modifie le texte
    document.getElementById("greet").innerHTML = "Okay, " + packet["nom"];
    document.getElementById("contentQuestion").innerHTML = "Dans quel équipe souhaite tu jouer ?";
}

// Enregistre l'équipe choisie, envoie les infos puis se place en attente
function choisirTeam(team) {
    if (step != 1) return;

    packet["team"] = team;

    // On affiche le prochain écran
    loadWaitScreen();

    // On envoie les infos
    packet["action"] = "init";
    envoyerPaquet(packet);
}

function loadWaitScreen() {
    // On cache l'entrée active
    if (step == 0) {
        var namePicker = document.getElementById("namePicker");
        namePicker.style.display = "none";
    } else if (step == 1) {
        var teamPicker = document.getElementById("teamPicker");
        teamPicker.style.position = "absolute";
        teamPicker.style.opacity = "0";
    }
    alignBox();

    // On modifie le texte
    document.getElementById("greet").innerHTML = "Bonne chance";
    document.getElementById("contentQuestion").innerHTML = "En attente du début du jeu...";

    // On enlève le hash
    history.pushState("", document.title, window.location.pathname);

    step = 2;
}

function loadEndCard(winner, isWinner) {
    // On cache l'entrée active
    if (step == 0) {
        var namePicker = document.getElementById("namePicker");
        namePicker.style.display = "none";
    } else if (step == 1) {
        var teamPicker = document.getElementById("teamPicker");
        teamPicker.style.position = "absolute";
        teamPicker.style.opacity = "0";
    }
    alignBox();

    // On modifie le texte
    if (isWinner == 'true') {
        document.getElementById("greet").innerHTML = "Félicitation !";
        document.getElementById("contentQuestion").innerHTML = "Votre équipe à gagner";
    } else if (isWinner == 'false') {
        document.getElementById("greet").innerHTML = "Dommage...";
        document.getElementById("contentQuestion").innerHTML = "Votre équipe à perdu";
    } else {
        document.getElementById("greet").innerHTML = "Game Over";
        document.getElementById("contentQuestion").innerHTML = "L'équipe " + (winner+1) + " gagne!";
    }

    // On enlève le hash
    history.pushState("", document.title, window.location.pathname);

    step = 3;
}

// On vérifie s'il ne faut pas immédiatement montrer l'écran d'attente
var hash = location.hash.split('#');

if (hash && hash.length > 0) {
    if (hash[1] == "skip") loadWaitScreen();
    else if (hash[1] == "end") loadEndCard(hash[2], hash[3]);
}

// Vérifie si un chaîne de caractères est vide
// https://stackoverflow.com/a/5559461
function isNullOrWhitespace(input) {

    if (typeof input === 'undefined' || input == null) return true;

    return input.replace(/\s/g, '').length < 1;
}