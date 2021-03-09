#Classe servant a instancier des joueurs
class Joueur:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.dead = False
    def translation(self, dx, dy):
        self.x += dx
        self.y += dy
    def isDead(self):
        return self.dead
    def setDead(self, valeur):
        self.dead = valeur