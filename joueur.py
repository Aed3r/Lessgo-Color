#Classe servant a instancier des joueurs
class Joueur:
    def __init__(self, id):
        self.id = id
        self.x = 0
        self.y = 0
    def translation(self, dx, dy):
        self.x += dx
        self.y += dy
    def isDead(self):
        return self.dead