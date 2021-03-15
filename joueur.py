#Classe servant a instancier des joueurs
import pygame

class Joueur(object):
    def __init__(self, id, x, y, equipe):
        self.id = id
        self.x = x
        self.y = y
        self.dead = False
        self.equipe = equipe
        if equipe == 0:
            self.color = (0, 127, 255)
        elif equipe == 1:
            self.color = (255, 255, 0)
        elif equipe == 2:
            self.color = (187, 11, 11)
        elif equipe == 3:
            self.color = (0,255,0) 
    def translation(self, dx, dy):
        self.x += dx
        self.y += dy
    def isDead(self):
        return self.dead
    def setDead(self, valeur):
        self.dead = valeur
    def afficher(self, fenetre):
        if self.isDead():
            self.x = -1
            self.y = -1
        else:
            pygame.draw.circle(fenetre, self.color, [self.x, self.y], 5)