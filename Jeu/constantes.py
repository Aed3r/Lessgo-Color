# ----------------- Display.py ----------------- #
resolution = (1920, 1080)
pleinEcran = 0 # Si 0 utilise la résolution définit ci-dessus
fps = 60

# ------------------ Main.py ------------------- #
port = 8081

# ------------------ Plateau ------------------- #
tailleCase = 10
propZoneInit = 8 # Contrôle la taille des zones initiales
tailleBarre = 20
resolutionPlateau = (resolution[0], resolution[1] - tailleBarre)

# ------------------ Joueur.py ----------------- #
#   placementInitial
playerSize = 5
placex1 = 12
placey1 = 12
placex2 = (int) (resolutionPlateau[0] * 0.9)
placey2 = 12
placex3 = (int) (resolutionPlateau[0] * 0.9)
placey3 = (int) (resolutionPlateau[1] * 0.9)
placex4 = 12
placey4 = (int) (resolutionPlateau[1] * 0.9)