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

# ------------------ Joueur.py ----------------- #
#   placementInitial
playerSize = 5
placex1 = 12
placey1 = 12
placex2 = (int) ((resolution[0] - tailleBarre) * 0.9)
placey2 = 12
placex3 = (int) ((resolution[0] - tailleBarre) * 0.9)
placey3 = (int) ((resolution[1] - tailleBarre) * 0.9)
placex4 = 12
placey4 = (int) ((resolution[1] - tailleBarre) * 0.9)