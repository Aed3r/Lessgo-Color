import pygame

#INITIALISATION

pygame.init()
pygame.display.set_caption("JEU_OS_TEST")
info = pygame.display.Info()                                                        #recupere l'information de la machine en cours
resolution = (info.current_w,info.current_h)                                        #resolution de l'ecrant a partir de info
fenetre = pygame.display.set_mode(resolution,pygame.FULLSCREEN)                     #FULLSCREEN
boucler = True

#BOUCLE PRINCIPALE

while boucler:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            boucler = False
        if event.type == pygame.KEYDOWN:
            boucler = False
            
    fenetre.fill((210,210,210))                                                     #couleur fenetre
    pygame.draw.circle(fenetre,(0,0,0),[150, 100], 5)
    pygame.display.flip()                                                           #actualise
