"""
    main execution loop of the game
"""
# import necessary packages
import pygame
import time
from random import randrange
from utility import WHITE, BLACK, RED

# import sprite modules
import cactus
import cloud
import blocky

pygame.init()

# keep track of the score based on time elapsed
# return score as an integer
def computeScore(score, display):
    timeElapsed = pygame.time.get_ticks()
    score += timeElapsed // 100
    smallFont = pygame.font.SysFont("comicsansms", 25)
    text = smallFont.render("Score: "+str(score), True, BLACK)
    display.blit(text, (660, 0))
    

def main():

    # initialize everything
    gameExit = False
    screen = pygame.display.set_mode((800, 800)) 
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

    # prepare game objects
    clock = pygame.time.Clock()
    block = blocky.Block(30, 400, 40)
    cactusSprites = pygame.sprite.Group()
    cloudSprites = pygame.sprite.Group()
    allsprites = pygame.sprite.Group([block])

    cactus1 = cactus.Cactus(randrange(800, 1600), 390)
    cactus2 = cactus.Cactus(randrange(800, 1600), 390)
    cactus3 = cactus.Cactus(randrange(800, 1600), 390)
    cactusSprites.add(cactus1, cactus2, cactus3)

    # create 2 clouds
    # cloud1 will lag behind cloud2 in a set pattern
    cloud1 = cloud.Cloud(1900, 200)
    cloud2 = cloud.Cloud(1800, 250)
    cloudSprites.add(cloud1, cloud2)

    # main game loop
    while not gameExit:

        # limit clock speed
        clock.tick(60)

        # event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    block.jumpFlag = True

        if block.jumpFlag:
            block.lead_y = block.jumpBlock()
            # decrease the speed by 1 each frame to account for gravity
            block.speed -= 4
            block.updateBlock()

        # check for collision
        blockHitList = pygame.sprite.spritecollide(block, cactusSprites, False)
        if blockHitList:
            block.isCollided = True
            pygame.quit()
            quit()
       
        for icactus in cactusSprites:
            # use 1.5 size ratio for collision detection between cacti
            # this is to make gap spacing between cacti more fairs
            # remove icactus to prevent testing for itselfs
            cactusSprites.remove(icactus)
            if pygame.sprite.spritecollide(icactus, cactusSprites, False, pygame.sprite.collide_rect_ratio(2)):
                icactus.tooClose = True
            cactusSprites.add(icactus)

        #draw everything else out
        screen.blit(background, (0, 0))
        cloudSprites.update()
        cloudSprites.draw(screen)
        cactusSprites.update()
        cactusSprites.draw(screen)
        allsprites.update()
        allsprites.draw(screen)

        # update the score
        computeScore(0, screen)
        
        pygame.display.update()


    # quit pygame if player decides to stop
    pygame.quit()
    quit()
    sys.exit(0)

##if __name__ == "__main__":
##    main()
