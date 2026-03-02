import pygame
from settings import LARGURA, GRAVIDADE, VEL_PULO, VEL_ANDAR

class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((139, 69, 19))
        self.rect = self.image.get_rect(midbottom=(100, 500))
        self.vel_y = 0
        self.no_chao = True

    def update(self):
        keys = pygame.key.get_pressed()
        
        # Movimento Lateral (Tipo Mario)
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= VEL_ANDAR
        if keys[pygame.K_RIGHT] and self.rect.right < LARGURA:
            self.rect.x += VEL_ANDAR

        # Pulo
        self.vel_y += GRAVIDADE
        self.rect.y += self.vel_y

        if self.rect.bottom >= 500:
            self.rect.bottom = 500
            self.vel_y = 0
            self.no_chao = True

        if keys[pygame.K_SPACE] and self.no_chao:
            self.vel_y = VEL_PULO
            self.no_chao = False