import pygame
import threading
import time
import joueur
import plateau
import constantes as cst
import os

# Timer
chronoDebut = None
place = True
fond = None
fondChrono = None

# Temps de calcul alloué pour une image
msPerFrame = int(1000 / cst.fps)

def afficherJoueurs(fenetre):
    for j in joueur.getJoueurs():
        pygame.draw.circle(fenetre, j.getCouleur(), j.getPos(), j.getRayon()*cst.tailleCase)   

# (Ré-)initialise le chronomètre
def initChrono():
    global chronoDebut
    chronoDebut = time.time() + cst.tempsPartie

# AfficehRenvoie True si la partie est finie, False sinon
def drawChrono(fenetre):
    global chronoDebut, place, fondChrono, fond

    tActuelle=time.time()
    t0=chronoDebut - tActuelle
    #print("t0 = " + str(t0) + "t0 % 10 =" + str(t0%10))
    #print(place)
    if ((int)(t0 % 10) == 0) and (place == True):
        plateau.getTerrain().placerPowerupAlea()
        place = False
    elif ((int)(t0 % 10) != 0):
        place = True
    t0 = int(t0)
    minute= str(t0//60)
    seconde = str(t0%60)
    if (t0 == 0):
        return True
    text = cst.policeBold.render (minute + ":" + seconde, True, (255,255,255))

    if fondChrono == None:
        fond = pygame.image.load(os.path.join("Data", "Images", "styleChrono.png")).convert_alpha()
        fondChrono = pygame.transform.smoothscale(fond, ((int) (text.get_width()*1.50), (int) (text.get_height() + (text.get_width()*0.5))))
    chronoPos = ((int) (cst.getRes()[0]/2 - text.get_width()*1.5/2), (int) (50 - text.get_width()*0.5/2))

    fenetre.blit(fondChrono, chronoPos)
    fenetre.blit(text, (cst.getRes()[0]/2 - text.get_width()/2, 50))   
    return False      

# Annonces
annonceDebut = None
annonce = None

def afficherAnnonce(fenetre):
    global annonceDebut, annonce

    if annonceDebut == None:
        return

    if time.time() >= annonceDebut+cst.tempsAnnonces:
        annonceDebut = None
        annonce = None
        return
    
    fenetre.blit(annonce, (cst.getRes()[0]/2 - annonce.get_width()/2, 120))

def definirAnnonce (texte):
    global fond, annonceDebut, annonce

    annonceDebut = time.time()
    text = cst.policeBold.render (texte, True, (255,255,255))
    text = pygame.transform.smoothscale(text, ((int) (cst.getRes()[0]*cst.largeurAnnonces), int((text.get_height() / text.get_width()) * (cst.getRes()[0]*cst.largeurAnnonces))))
    if fond == None:
        fond = pygame.image.load(os.path.join("Data", "Images", "styleChrono.png")).convert_alpha()
    annonce = pygame.transform.smoothscale(fond, ((int) (text.get_width()*1.2), (int) (text.get_height() + (text.get_width()*0.05))))
    annonce.blit(text, (text.get_width()*0.1, text.get_width()*0.025))

def drawAll(fenetre, pause):
    # Mesure du temps d'affichage de la frame
    start = time.time() * 1000

    # Affichage du terrain
    plateau.getTerrain().afficheTerrain(fenetre)

    # Affiche les proportions des zones coloriées
    plateau.getTerrain().afficheProp(fenetre)
    
    # Affichage des joueurs
    afficherJoueurs(fenetre)

    # Affichage du chrono
    if not pause:
        gameDone = drawChrono(fenetre)
    else:
        gameDone = False

    # Affichage des annonces
    if not pause:
        afficherAnnonce(fenetre)

    # Fin de la mesure du temps et attente pour afficher la prochaine frame
    end = time.time() * 1000

    # Affichage fps
    tempsCalcul = end - start # ms
    if cst.afficherFPS:
        text = cst.policeMedium.render(str(min(cst.fps, round(1000 / tempsCalcul))) + " fps", True, (0,0,0), (255,255,255))
        fenetre.blit(text, (cst.getRes()[0] - text.get_width(), 0))   

    sleep = (msPerFrame - tempsCalcul)/1000.
    if (sleep > 0): 
        time.sleep(sleep)

    return gameDone