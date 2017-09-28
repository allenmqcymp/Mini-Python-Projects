import pygame
import os, sys

# preset color variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


# directories of image resources
# take the head of the absolute directory
mainDir = os.path.split(os.path.abspath(__file__))[0]
dataDir = os.path.join(mainDir, "Assets")

# loads an image
def loadImage(name, lead_x, lead_y, colorkey=None):
    fullname = os.path.join(dataDir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print "Cannot load" + name 
    # create a new surface for blitting
    image = image.convert_alpha()
    if colorkey is not None:
        # if an invalid colorkey is present, set colorkey to that of top left pixel
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect(topleft=(lead_x, lead_y))


# this class has a function that extracts a sprite from a spritesheet
class SpriteSheet(object):
    def __init__(self, name):
        # load the whole sprite sheet
        # center at 0,0 since we are going to cut out a sprite from spritesheet anyway
        self.spriteSheet = loadImage(name, 0, 0, None)

    # getSprite takes a tuple of 4 measures as argument
    def getSprite(self, (x, y, width, height)):
        image = pygame.Surface([width, height])
        image.convert_alpha()
        # blit whole spriteSheet onto defined image
        # this effectively crops the desired sprite from spritesheet
        # take only the image from the tuple returned by loadImage function
        image.blit((self.spriteSheet)[0], (0,0), (x, y, width, height))
        image.set_colorkey(BLACK)
        return image
        
