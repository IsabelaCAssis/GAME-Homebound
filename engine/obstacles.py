import pygame
from settings import LARGURA, COR_MOEDA

class Moeda(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Representação visual da moeda (Círculo Dourado)
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, COR_MOEDA, (10, 10), 10)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        # Aqui você poderia adicionar uma animação de "flutuar" depois
        pass

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo):
        super().__init__()
        self.tipo = tipo
        # Exemplo: Lata de Lixo (Cinza) ou Carro (Azul)
        if tipo == "lixeira":
            self.image = pygame.Surface((30, 40))
            self.image.fill((100, 100, 100))
        else: # Carro
            self.image = pygame.Surface((60, 30))
            self.image.fill((0, 0, 150))
            
        self.rect = self.image.get_rect(midbottom=(x, y))