class Bouton:  # Classe permettant de créer des boutons
    def __init__(self, coords, text, size, screen, alphaSurface, font):
        self.rect = pygame.Rect(coords, size)
        self.coords = coords
        self.size = size
        self.screen = screen
        self.text = text
        self.alphaSurface = alphaSurface
        self.font = font

    def draw(self, mousePos):
        texte = self.font.render(self.text, 1, (0, 0, 0))
        if self.rect.collidepoint(mousePos):
            pygame.draw.rect(self.screen, pygame.Color(255, 255, 255, 127), pygame.Rect(self.coords[0], self.coords[1], self.rect.size[0], self.rect.size[1]))
            self.screen.blit(texte, (self.coords[0] + self.size[0] / 2 - texte.get_size()[0] / 2, self.coords[1] + self.size[1] / 2 - texte.get_size()[1] / 2))
        else:
            pygame.draw.rect(self.alphaSurface, pygame.Color(255, 255, 255, 127), pygame.Rect(self.coords[0], self.coords[1], self.rect.size[0], self.rect.size[1]))
            self.alphaSurface.blit(texte, (self.coords[0] + self.size[0] / 2 - texte.get_size()[0] / 2, self.coords[1] + self.size[1] / 2 - texte.get_size()[1] / 2))
