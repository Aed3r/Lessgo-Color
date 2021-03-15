import pygame
from joueur import *

pygame.init()
pygame.display.set_caption("Tutut")
resolution = (1920,1080)
fenetre = pygame.display.set_mode(resolution,pygame.RESIZABLE) #FULLSCREEN

pygame.display.flip() #actualise

ok = True

listeJoueurs = ListeJoueurs()
listeJoueurs.ajouter(Joueur(0, 1))
listeJoueurs.ajouter(Joueur(2, 2))
listeJoueurs.ajouter(Joueur(3, 3))
listeJoueurs.ajouter(Joueur(4, 4))

while ok:
    
    fenetre.fill((80,80,80)) #couleur fenetre
    
    listeJoueurs.placementJoueurs()
    listeJoueurs.afficher(fenetre)
    


    pygame.display.flip() #actualise
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ok = False
