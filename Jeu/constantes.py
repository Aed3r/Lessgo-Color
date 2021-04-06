# ----------------- Display ----------------- #
resolution = (1920, 1080)
pleinEcran = 0 # Si 0 utilise la résolution définit ci-dessus
fps = 60
couleursPlateau = [(60, 23, 66), (243, 255, 185), (196, 32, 33), (250,166,19)]
couleursJoueurs = [(30, 11, 33), (183, 221, 0), (98, 16, 16), (132,85,2)]

# ------------------ Main ------------------- #
port = 8081

# ------------------ Plateau ------------------- #
tailleCase = 10
propZoneInit = 0.2 # Contrôle la taille des zones initiales en *100 %
tailleBarre = 20
resolutionPlateau = (resolution[0], resolution[1] - tailleBarre)

# ------------------ Joueur ----------------- #
playerSize = 5

#Valeurs par défaut
defRayonCouleur = 1
defVitesse = 1

# ----------------- Gameplay ----------------- #
msPowerup = 10000
nbPowerup = 1
neutral = 0
paintMore = 1
gottaGoFast = 2
# Pour stocker la valeur a ajouter aux stats du joueur pour chaque powerups on va utiliser un tableau de vecteurs [Vitesse, rayon]
listeValeurs = [[0, 0], [0, 1], [1, 0]]

# ----------------- Ecran d'attente ----------------- #
marginsH = 0.1 # *100 %
marginsTop = 0.2 # *100 %
marginsBottom = 0.1 # *100 %