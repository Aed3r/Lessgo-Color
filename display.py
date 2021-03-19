***REMOVED***
import threading
import time
from joueur import *

class affichage(threading.Thread):  
    def __init__(self):  
        threading.Thread.__init__(self)
  
    def run(self):  
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            # Affichage du plateau et des joueurs, s'arrête avec le serveur
            # afficherJoueur(fenetre) 
            pass

def afficherJoueurs(fenetre):
    fenetre.fill((80,80,80)) #couleur fenetre
    joueurs.sort(key=comparJoueur) # Trie les joueurs suivant leurs ordonnées 
    for joueur in joueurs:
        joueur.afficher(fenetre)