***REMOVED***
from pygame.constants import JOYBUTTONDOWN
from joueur import *

***REMOVED***
pygame.display.set_caption("Tutut")
resolution = (1920,1080)
fenetre = pygame.display.set_mode(resolution,pygame.RESIZABLE) #FULLSCREEN

pygame.display.flip() #actualise

ok = True

listeJoueurs = ListeJoueurs()
j = Joueur(0,1)
listeJoueurs.ajouter(j)
listeJoueurs.ajouter(Joueur(2, 2))
listeJoueurs.ajouter(Joueur(3, 3))
listeJoueurs.ajouter(Joueur(4, 4))

listeJoueurs.placementJoueurs()

while ok:
    
    fenetre.fill((80,80,80)) #couleur fenetre
    
    listeJoueurs.afficher(fenetre)

    j.translation(1, 1)


    pygame.display.flip() #actualise
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ok = False
