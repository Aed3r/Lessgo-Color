import pygame
import UI.bouton as b
from constantes import *

boutons = []
rectBoutons = []
orientation = None # 'V' ou 'H' 
doDraw = False

# Crée ou supprime les boutons du menu d'attente sélectionné
def toggle (etat):
    global boutons, orientation, doDraw

    if not doDraw: # Création des boutons
        orientation = 'V'
        doDraw = True
        if etat == "attente":
            boutons.append(b.Bouton(LANCERJEU, policeTitres, buttonBGcol, buttonFGcol))
            boutons.append(b.Bouton(QUITTERJEU, policeTitres, buttonBGcol, buttonFGcol))
        elif etat == "jeu":
            boutons.append(b.Bouton(REDEMJEU, policeTitres, buttonBGcol, buttonFGcol))
            boutons.append(b.Bouton(REVATTENTE, policeTitres, buttonBGcol, buttonFGcol))
            boutons.append(b.Bouton(INITTIMER, policeTitres, buttonBGcol, buttonFGcol))
            boutons.append(b.Bouton(FINIRJEU, policeTitres, buttonBGcol, buttonFGcol))
            boutons.append(b.Bouton(QUITTERJEU, policeTitres, buttonBGcol, buttonFGcol))
        elif etat == "fin":
            boutons.append(b.Bouton(REVATTENTE, policeTitres, buttonBGcol, buttonFGcol))
            boutons.append(b.Bouton(QUITTERJEU, policeTitres, buttonBGcol, buttonFGcol))
    else: # Suppression des boutons
        boutons.clear()
        rectBoutons.clear()
        orientation = None
        doDraw = False

# Affiche les boutons potentiellement prédéfinies (selon l'orientation donnée)
def afficherMenu(fenetre):
    global boutons, rectBoutons, orientation, doDraw

    if not doDraw:
        return

    # Fond noir
    alphaSurface = pygame.Surface(fenetre.get_size(), pygame.SRCALPHA)
    alphaSurface.fill((0, 0, 0, 128))
    fenetre.blit(alphaSurface, (0, 0))

    # Boutons

    if (orientation == 'H'):
        espacement = fenetre.get_size()[0] / (len(boutons)+1)
    else:
        espacement = fenetre.get_size()[1] / (len(boutons)+1)
    
    rectBoutons.clear()

    for i in range(len(boutons)):
        if (orientation == 'H'):
            rectBoutons.append(boutons[i].draw(fenetre, ((i+1)*espacement, fenetre.get_size()[1]/2)))
        else:
            rectBoutons.append(boutons[i].draw(fenetre, (fenetre.get_size()[0]/2, (i+1)*espacement)))

def verifClic(position):
    global boutons, rectBoutons

    for i in range(len(rectBoutons)):
        if rectBoutons[i].collidepoint(position):
            return boutons[i].getText()
    
    return None