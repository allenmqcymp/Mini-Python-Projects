import pygame
import utility
from random import randrange

class Cactus(pygame.sprite.Sprite):

    def __init__(self, lead_x, lead_y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utility.loadImage("cactus.png", lead_x, lead_y,
                                                   None)
        self.tooClose = False
    
    def update(self):
        # move the cactus
        self.rect.x -= 19
        # recycle the cactus once it moves off screen
        if self.rect.centerx <= 0:
            # move off screen and spawn randomly again
            self.rect.x = randrange(800, 1600)
        if self.tooClose == True:
            self.rect.x = randrange(800, 1600)
            self.tooClose = False
        

class BigCactus(Cactus):
    # TODO: add image for bigCactus - make it appear less frequently
    # than regular cactus
    pass

class SmallCactus(Cactus):
    # TODO: add image for smaller cactus - make it appear less frequently
    # than regular cactus
    pass
