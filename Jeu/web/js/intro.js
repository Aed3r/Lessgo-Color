packet = {} // Le paquet envoyé au serveur

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
    packet["team"] = team;

    // On cache l'entré courante
    var teamPicker = document.getElementById("teamPicker");
    teamPicker.style.position = "absolute";
    teamPicker.style.opacity = "0";
    alignBox();

    // On modifie le texte
    document.getElementById("greet").innerHTML = "Bonne chance";
    document.getElementById("contentQuestion").innerHTML = "En attente du début du jeu...";

    // On envoie les infos
    packet["action"] = "init";
    envoyerPaquet(packet);
}

// Vérifie si un chaîne de caractères est vide
// https://stackoverflow.com/a/5559461
function isNullOrWhitespace(input) {

    if (typeof input === 'undefined' || input == null) return true;

    return input.replace(/\s/g, '').length < 1;
}