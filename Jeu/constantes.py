# ----------------- Display.py ----------------- #
resolution = (1080, 720)
playerSize = 5
tailleCase = 20

fps = 60

# ------------------ Main.py ------------------- #
port = 8081

# ------------------ Joueur.py ----------------- #
#   placementInitial
placex1 = 12                            # equipe1 
placey1 = 12                            #
placex2 = 1900                          # equipe 2
placey2 = 12                            #
placex3 = 1900                          # equipe 3
placey3 = 1000                          #
placex4 = 12                            # equipe 4
placey4 = 1000                          #
#Valeurs par défaut
defRayonCouleur = 1
defVitesse = 1
# ----------------- plateau.py ----------------- #
nbPowerup = 3
neutral = 0
paintMore = 1
gottaGoFast = 2
mildPower = 3
# Pour stocker la valeur a ajouter aux stats du joueur pour chaque powerups on va utiliser un tableau de vecteurs [Vitesse, rayon, Durée(sec)]
listeValeurs = [[0, 0, 0], [0, 2, 10], [2, 0, 10], [1, 1, 10]]