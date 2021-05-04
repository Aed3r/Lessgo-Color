import pygame
import os

# ----------------- Affichage ----------------- #
pleinEcran = False # Si False utilise la résolution définit ci-dessous
pygame.init()
resolution = (pygame.display.Info().current_w, pygame.display.Info().current_h) if pleinEcran else (1500, 1000)
fps = 60
couleursPlateau = [(60, 23, 66), (243, 255, 185), (196, 32, 33), (115,210,222)]
couleursJoueurs = [(30, 11, 33), (183, 221, 0), (98, 16, 16), (32,125,137)]

# ------------------ Main ------------------- #
port = 8081
tempsPartie = 300

# ------------------ Plateau ------------------- #
tailleCase = 10 # Modifier les tiles dans Data/Images/Tiles également
propZoneInit = 0.2 # Contrôle la taille des zones initiales en *100 %
tailleBarre = 20
resolutionPlateau = (resolution[0], resolution[1] - tailleBarre)
couleurFond = (255, 255, 255)
wrapAround = False

# ------------------ Joueur ----------------- #
playerSize = 5

#Valeurs par défaut
defRayonCouleur = 1
defVitesse = 1
# ----------------- Gameplay ----------------- #
nbPowerup = 3
paintMore = 0
gottaGoFast = 1
mildPower = 2
# Pour stocker la valeur a ajouter aux stats du joueur pour chaque powerups on va utiliser un tableau de vecteurs [Vitesse, rayon, Durée(sec)]
listeValeurs = [[0, 1, 10, "paintMore.png"], [2, 0, 10, "gottaGoFast.png"], [1, 1, 10, "mildPower.png"]]

# ----------------- Ecran d'attente ----------------- #
margins = {'left': 5, 'right': 5, 'top': 20, 'bottom': 10} # En %
tailleCompteur = 0.05 # En % de la hauteur de la fenêtre
titleColor = (49, 51, 53) # Couleurs du texte sur fond blanc
margeCompteur = 5

# ----------------- Menu pause ----------------- #
buttonBGcol = (255,255,255,255)
buttonFGcol = titleColor

# ----------------- Polices ----------------- #
policeNoms = pygame.font.Font(os.path.join("Data", "Fonts", "Quicksand-VariableFont_wght.ttf"), 30)
policeTitres = pygame.font.Font(os.path.join("Data", "Fonts", "Quicksand-VariableFont_wght.ttf"), 60)

# ----------------- Strings ----------------- #
LANCERJEU = "Lancer le jeu"
QUITTERJEU = "Quitter le jeu"
REDEMJEU = "Redémarrer le jeu"
REVATTENTE = "Revenir au menu attente"
INITTIMER = "Réinitialiser le timer"
FINIRJEU = "Finir le jeu"
ENATTENTE = "En attente de joueurs..."