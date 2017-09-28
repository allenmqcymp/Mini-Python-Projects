import pygame
import utility

class Cloud(pygame.sprite.Sprite):

    def __init__(self, lead_x, lead_y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utility.loadImage("cloud.png", lead_x, lead_y,
                                                  None)
        
    def update(self):
        self.rect.centerx -= 5
        if self.rect.centerx <= 0:
            self.rect.x = 1000
