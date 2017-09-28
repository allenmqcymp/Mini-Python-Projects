import pygame
from utility import SpriteSheet

# player class
class Block(pygame.sprite.Sprite):

    
    SPRITE_ONE = (680, 5, 40, 40)
    SPRITE_TWO = (723, 5, 40, 40)
    SPRITE_THREE = (768, 5, 40, 40)
    SPRITE_FOUR = (811, 5, 40, 40)
    SPRITE_FIVE = (855, 5, 40, 40)


    def __init__(self, lead_x, lead_y, speed):
        pygame.sprite.Sprite.__init__(self)

        self.initialSpeed = speed
        self.speed = speed
        self.lead_x = lead_x
        self.lead_y = lead_y
        self.jumpFlag = False
        self.isJumping = False
        self.isCollided = False

        self.spriteSheet = SpriteSheet("offline-sprite-1x.gif")
        self.image = self.spriteSheet.getSprite((680, 5, 40, 40))
        self.rect = self.image.get_rect(center=(lead_x, lead_y))

        # save all the sprite sheet sprites in a list
        self.spriteList = []
        for iteration in [self.SPRITE_ONE, self.SPRITE_TWO, self.SPRITE_THREE, self.SPRITE_FOUR, self.SPRITE_FIVE]:
            self.image = self.spriteSheet.getSprite(iteration)
            self.spriteList.append(self.image)

        self.numberImages = 8
        self.currentImage = 0

    def jumpBlock(self):
        self.lead_y -= self.speed
        if self.lead_y > 400:
            self.lead_y = 400
            self.jumpFlag = False
            self.speed = self.initialSpeed
        if self.lead_y is not 400:
            self.isJumping = True
        else:
            self.isJumping = False
        return self.lead_y
        
    def updateBlock(self):
        self.rect = self.image.get_rect(center=(self.lead_x, self.lead_y))

    def update(self):

        # for updating the spriteSheet
        # updateBlock updates self.rect and self.image
        # every 4th frame, update the spritesheet
        if self.currentImage >= self.numberImages:
            self.currentImage = 0
        else:
            self.currentImage += 1

        # change the image according to spriteSheet
        if self.currentImage == 0:
            self.image = self.spriteList[0]
        elif self.currentImage == 2:
            self.image = self.spriteList[1]
        elif self.currentImage == 4:
            self.image = self.spriteList[2]
        elif self.currentImage == 6:
            self.image = self.spriteList[3]

        # when jumping, change the image
        if self.isJumping == True:
            self.image = self.spriteList[0]
            
        # when collided with cactus, display shocked image
        if self.isCollided == True:
            self.image = self.spriteList[4]
        
        
