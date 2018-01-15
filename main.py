import pygame
import time
import random
pygame.init()

window = (800, 600)  # width and height of the screen
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 100, 150)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BackGroundColor = (140, 0, 50)
GREEN = (0, 140, 0)

gameDisplay = pygame.display.set_mode(window)  # Name of the main screen
pygame.display.set_caption('Snake')  # Title of the game
icon = pygame.image.load('Snake.png')
pygame.display.set_icon(icon)

img = pygame.image.load('Snake.png')
appleImg = pygame.image.load('Apple.png')

clock = pygame.time.Clock()
FPS = 60
block_size = 20

direction = "right"


def game_intro():
    intro = True
    while intro:
        gameDisplay.fill(WHITE)
        message_to_screen_center("Welcome to Snake Game", GREEN, 60, -100)
        message_to_screen_center("Press 'Space' to start the game", BLUE, 60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
                    return True
        pygame.display.update()
        clock.tick(60)


def snake(block_size, snakeList):
    if direction == "right":
        head = pygame.transform.rotate(img, 270)
    elif direction == "left":
        head = pygame.transform.rotate(img, 90)
    elif direction == "up":
        head = img
    elif direction == "down":
        head = pygame.transform.rotate(img, 180)

    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, GREEN, [XnY[0], XnY[1], block_size, block_size])  # Draw snake
    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))


def text_objects(text, color, font):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen_center(message, color, fontSize, y_displace=0, x_displace=0):
    font = pygame.font.SysFont(None, fontSize)
    textSurf, textRect = text_objects(message, color, font)
    textRect.center = (window[0] / 2) + x_displace, (window[1] / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)


def message_to_screen(message, color, fontSize, x_pos=window[0]/3, y_pos=window[1]/3, second=0):
    font = pygame.font.SysFont(None, fontSize)
    screen_text = font.render(message, True, color)
    gameDisplay.blit(screen_text, [x_pos, y_pos])
    time.sleep(second)


def newHighScore(score):
    write = open("highScore.txt", "w")
    write.write(str(score))
    write.close()


def gameLoop():
    global direction
    gameExit = False
    gameOver = False
    score = 0

    count = 0.0

    file = open("highScore.txt", "r")
    highScore = str(file.read())
    file.close()

    speed = 5
    lead_x = window[0] / 2
    lead_y = window[1] / 2
    lead_x_change = 0
    lead_y_change = 0

    snakeList = []
    snakeLength = 1

    AppleThickness = 20

    randAppleX = round(random.randrange(0, window[0]-AppleThickness))  # / float(block_size))*float(block_size)
    randAppleY = round(random.randrange(0, window[1]-AppleThickness))  # / float(block_size))*float(block_size)

    while not gameExit and intro:
        gameDisplay.fill(BackGroundColor)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if lead_x_change != speed:
                        lead_x_change = -speed
                        lead_y_change = 0
                        direction = "left"
                elif event.key == pygame.K_RIGHT:
                    if lead_x_change != -speed:
                        lead_x_change = speed
                        lead_y_change = 0
                        direction = "right"
                elif event.key == pygame.K_UP:
                    if lead_y_change != speed:
                        lead_y_change = -speed
                        lead_x_change = 0
                        direction = "up"
                elif event.key == pygame.K_DOWN:
                    if lead_y_change != -speed:
                        lead_y_change = speed
                        lead_x_change = 0
                        direction = "down"
            # if event.type == pygame.KEYUP:
            #   if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            #        lead_x_change = 0
        if lead_x >= window[0]:
            lead_x = 0
        elif lead_x < 0:
            lead_x = window[0]
        elif lead_y >= window[1]:
            lead_y = 0
        elif lead_y < 0:
            lead_y = window[1]
		
        lead_x += lead_x_change
        lead_y += lead_y_change
        # Background Color

        # pygame.draw.rect(gameDisplay, YELLOW, [randAppleX, randAppleY, AppleThickness, AppleThickness])  # Draw apple
        gameDisplay.blit(appleImg, (randAppleX, randAppleY))

        snakeHead = []
        snakeHead.append(lead_x)  # Add snake's head coordinates to snakeList
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:  # Remove tail in every while loop
            del snakeList[0]

        for eachSegment in snakeList[:-1]:  # Check the collision
            if eachSegment == snakeHead:
                gameOver = True

        snake(block_size, snakeList)  # Draw Snake

        message_to_screen(str(score), WHITE, 30, window[0]-50, 10)
        message_to_screen("Highest Score: " + highScore, WHITE, 30, 10, 10)
        # gameDisplay.fill(RED, rect=[200, 200, 50, 50])
        pygame.display.update()

        # if randAppleX - block_size <= lead_x <= randAppleX + AppleThickness:
        #     if randAppleY - block_size <= lead_y <= randAppleY + AppleThickness:
        #         randAppleX = round(random.randrange(0, window[0] - AppleThickness))  # / float(block_siz))*float(block_size)
        #         randAppleY = round(random.randrange(0, window[1] - AppleThickness))  # / float(block_siz))*float(block_size)
        #         score += 10
        #         snakeLength += 1

        if randAppleX <= lead_x <= randAppleX + AppleThickness or randAppleX + AppleThickness > lead_x + block_size > randAppleX:
            if randAppleY <= lead_y <= randAppleY + AppleThickness or randAppleY + AppleThickness > lead_y + block_size > randAppleY:
                randAppleX = round(random.randrange(0, window[0] - AppleThickness))
                randAppleY = round(random.randrange(0, window[1] - AppleThickness))
                score += 10
                snakeLength += 1
                count += 0.1
                if speed < 20:
                    speed += int(count)
                if count > 1:
                    count = 0.0

        clock.tick(FPS)
        
        while gameOver:
            gameDisplay.fill(WHITE)
            message_to_screen_center("Game Over!", RED, 40, -50)
            message_to_screen_center("Press Space to play again or ESC to quit!", BLACK, 50)
            pygame.display.update()
            if score > int(highScore):
                newHighScore(score)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gameExit = True
                        gameOver = False
                    elif event.key == pygame.K_SPACE:
                        gameLoop()

    pygame.quit()
    quit()


intro = game_intro()
gameLoop()
