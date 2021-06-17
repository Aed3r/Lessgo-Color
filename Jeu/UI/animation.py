import math

# Renvoi une valeur incrémentée selon la progression d'une courbe sinus au moment t
def sineWave (duree, destination, t):
    if t <= 0:
        return 0
    elif t >= duree:
        return destination
    else:
        return math.sin(t * ((2 * math.pi) / (duree*4))) * destination