import pygame

class Bouton:  # Classe permettant de créer des boutons
    def __init__(self, text, font, color):
        self.text = text
        self.font = font
        self.color = color

        # On prépare la surface tenant le texte
        texte = self.font.render(self.text, 1, (0, 0, 0))
        tTexte = texte.get_size()
        self.tBouton = (tTexte[0]*2, tTexte[1]*1.6)
        self.buffer = pygame.Surface(self.tBouton)
        self.buffer.fill(self.color)
        self.buffer.blit(texte, (self.tBouton[0]/2 - tTexte[0]/2, self.tBouton[1]/2 - tTexte[1]/2))

    # Affiche le bouton centré sur le point coords de la fenêtre screen. 
    # Renvoie le rectangle dans lequel se trouve le bouton
    def draw(self, screen, coords):
        # On rend le bouton translucide si la souris ne se trouve pas au dessus
        posEcran = (coords[0]-self.tBouton[0]/2, coords[1]-self.tBouton[1]/2)
        if not pygame.Rect(posEcran[0], posEcran[1], self.tBouton[0], self.tBouton[1]).collidepoint(pygame.mouse.get_pos()):
            self.buffer.set_alpha(127)
        else:
            self.buffer.set_alpha(255)

        # On affiche la surface au bon endroit
        screen.blit(self.buffer, posEcran)

        # On renvoie le rectangle dans lequel se trouve le bouton
        return pygame.Rect(posEcran, self.tBouton)

    def getText (self):
        return self.text

    def getTaille(self):
        return self.tBouton
