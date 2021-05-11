import pygame
import os

pygame.init()

# ----------------- Affichage ----------------- #
pleinEcran = False # Si False utilise la résolution définit ci-dessous
_resolution = (pygame.display.Info().current_w, pygame.display.Info().current_h) if pleinEcran else (1000, 700)
fps = 60
couleursPlateau = [(60, 23, 66), (243, 255, 185), (196, 32, 33), (115,210,222)]
couleursJoueurs = [(30, 11, 33), (183, 221, 0), (98, 16, 16), (32,125,137)]
afficherFPS = False
tempsAnnonces = 3 # secondes
largeurAnnonces = 0.7 # % de la largeur de l'écran

def getRes():
    global _resolution
    return _resolution

def getResP():
    global _resolutionPlateau
    return _resolutionPlateau

def setRes(res):
    global _resolution, _resolutionPlateau
    _resolution = res
    _resolutionPlateau = (res[0], res[1] - tailleBarre)

# ------------------ Main ------------------- #
port = 8081
tempsPartie = 300 # secondes

# ------------------ Plateau ------------------- #
tailleCase = 10 # Modifier les tiles dans Data/Images/Tiles également
propZoneInit = 0.2 # Contrôle la taille des zones initiales en *100 %
tailleBarre = 20
_resolutionPlateau = (_resolution[0], _resolution[1] - tailleBarre)
couleurFond = (255, 255, 255)
wrapAround = False
taillePowerUp = 50 # pixels
effetFondu = 20 # 0 (très lent) - 255 (instant)

# ------------------ Joueur ----------------- #
playerSize = 5

#Valeurs par défaut
defRayonCouleur = 1
defVitesse = 1

collisions = True
vitesseMax = 5 # Sans powerup
# ----------------- Gameplay ----------------- #
nbPowerup = 3
nbSpecial = 2
paintMore = 0
gottaGoFast = 1
mildPower = 2
teamPaintMore = 3
teamGoFast = 4
# Pour stocker la valeur a ajouter aux stats du joueur pour chaque powerups on va utiliser un tableau de vecteurs [Vitesse, rayon, Durée(sec)]
listeValeurs = [[0, 1, 10, "paintMore"], [2, 0, 10, "gottaGoFast"], [1, 1, 10, "mildPower"], [0, 1, 5, "paintMoreGold"], [2, 0, 5, "gottaGoFastGold"]]

#Nombre de PowerUp présent au démarage
powerUpsDemarage = 4
# ----------------- Ecran d'attente ----------------- #
margins = {'left': 5, 'right': 5, 'top': 20, 'bottom': 10} # En %
tailleCompteur = 0.05 # En % de la hauteur de la fenêtre
titleColor = (49, 51, 53) # Couleurs du texte sur fond blanc
margeCompteur = 5

# ----------------- Menu pause ----------------- #
buttonBGcol = (255,255,255,255)
buttonFGcol = titleColor

# ----------------- Polices ----------------- #
policeThin = pygame.font.Font(os.path.join("Data", "Fonts", "static", "Quicksand-Light.ttf"), 30)
policeMedium = pygame.font.Font(os.path.join("Data", "Fonts", "static", "Quicksand-Medium.ttf"), 30)
policeBold = pygame.font.Font(os.path.join("Data", "Fonts", "static", "Quicksand-SemiBold.ttf"), 60)

# ----------------- Strings ----------------- #
LANCERJEU = "Lancer le jeu"
QUITTERJEU = "Quitter le jeu"
REDEMJEU = "Redémarrer le jeu"
REVATTENTE = "Revenir au menu attente"
INITTIMER = "Réinitialiser le timer"
FINIRJEU = "Finir le jeu"
ENATTENTE = "En attente de joueurs..."

# ----------------- Ecran fin ----------------- #
largeurBarres = 60