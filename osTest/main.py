import pygame

pygame.init()
pygame.display.set_caption("JEU_OS_TEST")
resolution = (800,600)
fenetre = pygame.display.set_mode(resolution,pygame.RESIZABLE) #FULLSCREEN

pygame.display.flip() #actualise

boucler = True

while boucler:
    
    fenetre.fill((80,80,80)) #couleur fenetre
    
    # pygame.draw.line(fenetre,(0,0,0),[0,0],[800,600])

    #pygame.draw.rect(fenetre,(0,0,0),pygame.Rect(10,10,2,2))

    pygame.draw.circle(fenetre,(0,0,0),[150, 100], 5)
    
    pygame.display.flip() #actualise
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            boucler = False
