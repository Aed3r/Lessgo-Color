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
tempsPartie = 5

# ------------------ Plateau ------------------- #
tailleCase = 10
propZoneInit = 0.2 # Contrôle la taille des zones initiales en *100 %
tailleBarre = 20
resolutionPlateau = (resolution[0], resolution[1] - tailleBarre)
couleurFond = (255, 255, 255)

# ------------------ Joueur ----------------- #
playerSize = 5

#Valeurs par défaut
defRayonCouleur = 1
defVitesse = 1.2
# ----------------- Gameplay ----------------- #
msPowerup = 10000
nbPowerup = 1
neutral = 0
paintMore = 1
gottaGoFast = 2
# Pour stocker la valeur a ajouter aux stats du joueur pour chaque powerups on va utiliser un tableau de vecteurs [Vitesse, rayon]
listeValeurs = [[0, 0], [0, 1], [1, 0]]

# ----------------- Ecran d'attente ----------------- #
margins = {'left': 5, 'right': 5, 'top': 20, 'bottom': 10} # En %
tailleCompteur = 0.05 # En % de la hauteur de la fenêtre
titleColor = (49, 51, 53) # Couleurs du texte sur fond blanc
margeCompteur = 5

# ----------------- Polices ----------------- #
policeNoms = pygame.font.Font(os.path.join("Data", "Fonts", "Quicksand-VariableFont_wght.ttf"), 30)
policeTitres = pygame.font.Font(os.path.join("Data", "Fonts", "Quicksand-VariableFont_wght.ttf"), 60)