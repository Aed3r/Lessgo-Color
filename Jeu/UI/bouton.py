import pygame

class Bouton:  # Classe permettant de créer des boutons
    def __init__(self, text, font, color):
        self.text = text
        self.font = font
        self.color = color

    # Affiche le bouton centré sur le point coords de la fenêtre screen. 
    # Renvoie le rectangle dans lequel se trouve le bouton
    def draw(self, screen, coords, clic):
        texte = self.font.render(self.text, 1, (0, 0, 0))
        tTexte = texte.get_size()
        tBouton = (tTexte[0]*2, tTexte[1]*1.6)
        tempSurface = pygame.Surface(tBouton)
        tempSurface.fill(self.color)
        tempSurface.blit(texte, (tBouton[0]/2 - tTexte[0]/2, tBouton[1]/2 - tTexte[1]/2))
        posEcran = (coords[0]-tBouton[0]/2, coords[1]-tBouton[1]/2)
        if not pygame.Rect(posEcran[0], posEcran[1], tBouton[0], tBouton[1]).collidepoint(pygame.mouse.get_pos()):
            tempSurface.set_alpha(127)
        screen.blit(tempSurface, posEcran)
        return pygame.Rect(posEcran, tBouton)
