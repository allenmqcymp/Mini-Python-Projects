"""
---------------------------
To start the game, run this module
---------------------------
Contains main function
Contains a game class to make the code more modular
Written by Allen Ma

"""

# ----- Setup Modules -----
import pygame
import time
import sys
from random import randrange
import utility
from utility import WHITE, BLACK, RED

# ---- Game Modules -----
import cactus
import cloud
import blocky

# ----- Constants -------
# WHITE, BLACK, RED
SCREENWIDTH = 800
SCREENHEIGHT = 800


# ----- Game Class -----
# gameActive and gameOver scenes added to this class
class Game(object):
    def __init__(self):
        # create game objects
        self.block = blocky.Block(50, 400, 38)
        self.cactusSprites = pygame.sprite.Group()
        self.cloudSprites = pygame.sprite.Group()
        self.allsprites = pygame.sprite.Group([self.block])

        self.cactus1 = cactus.Cactus(randrange(800, 1600), 370)
        self.cactus2 = cactus.Cactus(randrange(800, 1600), 370)
        self.cactus3 = cactus.Cactus(randrange(800, 1600), 370)
        self.cactusSprites.add(self.cactus1, self.cactus2, self.cactus3)

        # create 2 clouds
        # cloud1 will lag behind cloud2 in a set pattern
        self.cloud1 = cloud.Cloud(1900, 200)
        self.cloud2 = cloud.Cloud(1800, 250)
        self.cloudSprites.add(self.cloud1, self.cloud2)

        # set initial score to 0
        self.score = 0

        # set gameOver to False intially
        self.gameOver = False

    def setHighScore(self, highScore):
        if self.gameOver:
            if self.score > highScore:
                highScore = self.score
        return highScore


    def computeScore(self, display):
        timeElapsed = pygame.time.get_ticks()
        self.score += timeElapsed // 1000

        # display score
        smallfont = pygame.font.SysFont("comicsansms", 25)
        displayText = smallfont.render("Score: "+str(self.score), True, BLACK)
        display.blit(displayText, (0, 0))



    def runLogic(self):
        # make the block jump
        if self.block.jumpFlag:
            self.block.lead_y = self.block.jumpBlock()
            # decrease the speed by 4 each frame to account for gravity
            self.block.speed -= float(4.5)
            self.block.updateBlock()

        # check for collision
        blockHitList = pygame.sprite.spritecollide(self.block, self.cactusSprites, False)
        if blockHitList:
            self.block.isCollided = True
            self.gameOver = True

       # check if the cacti are too close together
        for icactus in self.cactusSprites:
            self.cactusSprites.remove(icactus)
            if pygame.sprite.spritecollide(icactus, self.cactusSprites, False,
                                           pygame.sprite.collide_rect_ratio(2)):

                icactus.tooClose = True
            self.cactusSprites.add(icactus)



    # args passed in represents image to be detected
    def processEvents(self):
        # event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # set jumpFlag to make block jump
                    self.block.jumpFlag = True

        return False
    
    def displayFrame(self, display, background, highScore):

        # draw all sprites out and update their states each frame
        display.blit(background, (0, 0))
        self.cloudSprites.update()
        self.cloudSprites.draw(display)
        self.cactusSprites.update()
        self.cactusSprites.draw(display)
        self.allsprites.update()
        self.allsprites.draw(display)

        # display the score
        self.computeScore(display)
        highScore = self.setHighScore(highScore)

        # display the high score
        smallerFont = pygame.font.SysFont("comicsansms", 20)
        displayText2 = smallerFont.render("High score: " + str(highScore), True, BLACK)
        display.blit(displayText2, (0, 30))

        pygame.display.flip()

        return highScore
        
class GameOver(object):

    def __init__(self):
        self.gameStillOver = True

        largefont = pygame.font.SysFont("comicsansms", 50)
        self.gameOverText = largefont.render("GAME OVER", True, BLACK)

        self.quitImageRect = (utility.loadImage("quit.png", 420, 250))[1]
        self.quitImage     = (utility.loadImage("quit.png", 420, 250))[0]

        self.restartImageRect = (utility.loadImage("restart.png", 320, 250))[1]
        self.restartImage     = (utility.loadImage("restart.png", 320, 250))[0]


    def processEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.gameStillOver = False
                    time.sleep(0.3)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.isCollide(pos, self.quitImageRect) and event.button == 1:
                    pygame.quit()
                    quit()
                elif self.isCollide(pos, self.restartImageRect) and event.button == 1:
                    self.gameStillOver = False

    def drawFrame(self, display):
        display.blit(self.gameOverText, (250, 150))
        display.blit(self.quitImage, (410, 250))
        display.blit(self.restartImage, (320, 250))
        pygame.display.update()
        

    def isCollide(self, mousePos, imageRect):
        return imageRect.collidepoint(mousePos)



# ------ Main function - Entry Point ----------
def main():
    # set display surface, give a name to the game
    pygame.init()
    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('GoogleDino')

    # create the background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(WHITE)

    # display the background
    screen.blit(background, (0, 0))
    pygame.display.update()

    # draw a base line
    pygame.draw.line(background, BLACK, (0, 410), (800, 410), 1)
    pygame.display.update()

    # prepare the clock object
    clock = pygame.time.Clock()

    # prepare the game object
    game = Game()

    # prepare the gameOver object
    gameOver = GameOver()

    # main game loop
    # runs once per frame
    gameExit = False

    # global variable high score
    highScore = 0

    while not gameExit:
        clock.tick(100)
        
        if not game.gameOver:
            gameExit = game.processEvents()

            game.runLogic()

            highScore = game.displayFrame(screen, background, highScore)
        else:

            gameOver.drawFrame(screen)
            gameOver.processEvents()

        if gameOver.gameStillOver == False:
            game = Game()
            gameOver.gameStillOver = True

             
    pygame.quit()
    quit()


# ------ Run the module ------
if __name__ == "__main__":
    main()
