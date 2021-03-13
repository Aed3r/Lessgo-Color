***REMOVED***
from joueur import Joueur

***REMOVED***
pygame.display.set_caption("Tutut")
resolution = (1920,1080)
fenetre = pygame.display.set_mode(resolution,pygame.RESIZABLE) #FULLSCREEN

pygame.display.flip() #actualise

ok = True

listeJoueurs = [Joueur(1, 12, 12, 0), Joueur(2, 1900, 12, 1), Joueur(3, 1900, 1000, 2), Joueur(4, 12, 1000, 3)]

while ok:
    
    fenetre.fill((80,80,80)) #couleur fenetre
    
    for j in listeJoueurs :
        j.afficher(fenetre)
        j.translation(0.1,0)
    


    pygame.display.flip() #actualise
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ok = False
