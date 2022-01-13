import pygame
import sys
from pygame.locals import *
import time
import random

pygame.init()

clock=pygame.time.Clock() #this is for regulating fps

explosion = pygame.mixer.Sound("explosion.wav")

#setting up display
width = 1000
height = 650
disp = pygame.display.set_mode((width,height))
pygame.display.set_caption("Cat game")

#different elements
character = pygame.image.load("cat.png").convert_alpha()
mouse = pygame.image.load("mouse.png").convert_alpha()
dog = pygame.image.load("dog.png").convert_alpha()
rectangle  = pygame.Surface((350,100))
square = pygame.Surface((100,100))

black = (0,0,0)
purple = (124,27,198)
lime = (200,250,35)
turquise = (22,213,235)
red = (185, 47, 47)
colour = purple #later it will change to random

rectangle.fill(colour)
square.fill(turquise)

#positions of elements
whereCharacter = character.get_rect()
whereRectangle = rectangle.get_rect()
whereSquare = square.get_rect()
whereMouse = mouse.get_rect()
whereDog = dog.get_rect()

#starting positions
whereMouse.left = 0
whereMouse.top = 0
whereCharacter.left = 425
whereCharacter.top = 200
whereRectangle.left = 300
whereRectangle.top = 250
whereDog.left = 600
whereDog.top = 0
whereSquare.left = 600
whereSquare.top = 0

squareSpeed = [0,1] #square moves up and down
dogSpeed = [1,1] #dog moves diagonally

mouseEvent = pygame.event.Event(pygame.USEREVENT)
pygame.time.set_timer(mouseEvent, 1700)     #timer for mice appearing

#lists for all the mice and related info
mouseList = []  
whereList = []
speedList = []
pointsList = []

points = 0
highScore = 0
mousePoints = 1
speeding = 0 #for speeding up the dog from time to time

#fonts and texts
fontPoints = pygame.font.SysFont('Comic Sans MS', 30)
pointsText = fontPoints.render('Points: '+str(points), True, turquise)
highScoreText = fontPoints.render('High Score: '+str(points), True, lime)
fontGameOver = pygame.font.SysFont('Comic Sans MS', 60)
fontPlayAgain = pygame.font.SysFont('Comic Sans MS', 20)
gameOverText = fontGameOver.render('GAME OVER', True, turquise)
playAgainText = fontPlayAgain.render('To play again press space bar', True, lime)

while True:
    for gameEvent in pygame.event.get():    #closing the game
        if gameEvent.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if gameEvent.type == KEYDOWN:
            if gameEvent.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
                
        if gameEvent.type == pygame.USEREVENT:
            # happens every 1,7 seconds
            mouse=pygame.image.load("mouse.png").convert_alpha()
            mouseList.append(mouse)
            whereList.append(mouse.get_rect())
            speedList.append([random.randrange(1,7),random.randrange(1,7)]) #mouse gets random speed and direction
            pointsList.append(mousePoints)
            speeding = speeding + 1
            if speeding > 5:    #dog speeds up every 5 mice
                if dogSpeed[0] > 0: #check the current direction
                    dogSpeed[0] = dogSpeed[0] + random.randrange(1,3) #adds 1 or 2 to speed
                else:
                    dogSpeed[0] = dogSpeed[0] - random.randrange(1,3)
                if dogSpeed[1] > 0:
                    dogSpeed[1] = dogSpeed[1] + random.randrange(1,3)
                else:
                    dogSpeed[1] = dogSpeed[1] - random.randrange(1,3)
                speeding = 0 #reset counter
                
                
    clock.tick(90) #affects the speed of the game (fps)

    for i in range(0,len(mouseList)):  #controls all the mice
        whereList[i]=whereList[i].move(speedList[i])    #positions
        if whereList[i].left < 0 or whereList[i].right > width:
            speedList[i][0] = -speedList[i][0]
        if whereList[i].top < 0 or whereList[i].bottom > height:
            speedList[i][1] = -speedList[i][1]
        if whereRectangle.colliderect(whereList[i]): #mouse doesn't go through rectangle
            if whereRectangle.colliderect(whereList[i].move(-speedList[i][0],0)):
                speedList[i][1] = -speedList[i][1]
            if whereRectangle.colliderect(whereList[i].move(0,speedList[i][1])):
                speedList[i][0] = -speedList[i][0]
            colour = (random.randrange(0,256),random.randrange(0,256),random.randrange(0,256))
            rectangle.fill(colour) #change colour of rectangle to new random colour if mouse touches it
            pointsList[i]=pointsList[i]*2
            #points for a mouse double whenever mouse hits rectangle
            #so you want to let the mouse hit rectangle many times before collecting it


    whereDog.move_ip(dogSpeed)
    #keep dog from going off screen
    if whereDog.left < 0 or whereDog.right > width:
        dogSpeed[0] = -dogSpeed[0]
    if whereDog.top < 0 or whereDog.bottom > height:
        dogSpeed[1] = -dogSpeed[1]
    
    whereSquare.move_ip(squareSpeed)
    #keep square from going off screen
    if whereSquare.top < 0 or whereSquare.bottom > height:
        squareSpeed[1] = -squareSpeed[1]
        if squareSpeed[1] > 0:
            square.fill(turquise) #one colour when moving down
        else:
            square.fill(lime) #another colour when moving up

    j = 0   #to help go through mice
    for i in range(0,len(mouseList)):  #removes a mouse when it's eaten
        if whereCharacter.colliderect(whereList[i-j]):
            mouseList.pop(i-j)
            whereList.pop(i-j)
            speedList.pop(i-j)
            points = points + pointsList[i-j] #count the points before removing them from list
            pointsList.pop(i-j)
            j = j + 1

    #character hits square or dog catches character -> game over
    if whereCharacter.colliderect(whereSquare) or whereCharacter.colliderect(whereDog): 
        pygame.mixer.Sound.play(explosion)  #sound effect
        disp.blit(gameOverText,(60, 400))
        disp.blit(playAgainText, (90, 470))
        if points > highScore:
            highScore = points
            highScoreText = fontPoints.render('High Score: '+str(points), True, lime)
            #replaces high score if needed, but it updates on the screen only if game is restarted
        pygame.display.update()
        restart = False
        while not restart:
            for gameEvent in pygame.event.get():
                if gameEvent.type == pygame.QUIT: #possible to close the game
                    pygame.quit()
                    sys.exit()
                if gameEvent.type == KEYDOWN:  #can close with esc too
                    if gameEvent.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if gameEvent.key == K_SPACE:  #hitting space restarts the game
                        restart = True
                        points = 0
                        dogSpeed = [1,1]
                        whereCharacter.left = 425
                        whereCharacter.top = 200
                        whereDog.left = 600
                        whereDog.top = 0
                        mouseList = []
                        whereList = []
                        speedList = []
                        pointsList = []
                        #resets (almost) everything to start again
                        #square continues from the same place where it was
                        #rectangle keeps the same colour as it was

    keyPress = pygame.key.get_pressed() 
    if keyPress[K_a]:                   #moving with WASD
        whereCharacter.move_ip((-5,0))  
    if keyPress[K_d]:
        whereCharacter.move_ip((5,0))
    if keyPress[K_s]:
        whereCharacter.move_ip((0,5))
    if keyPress[K_w]:
        whereCharacter.move_ip((0,-5))
    if keyPress[K_LEFT]:                #moving faster with arrows
        whereCharacter.move_ip((-10,0))  
    if keyPress[K_RIGHT]:
        whereCharacter.move_ip((10,0))
    if keyPress[K_DOWN]:
        whereCharacter.move_ip((0,10))
    if keyPress[K_UP]:
        whereCharacter.move_ip((0,-10))

    if whereCharacter.left > width: #character comes out from the other side when going out of window
        whereCharacter.right = 0
    if whereCharacter.right < 0:
        whereCharacter.left = width
    if whereCharacter.top > height:
        whereCharacter.bottom = 0
    if whereCharacter.bottom < 0:
        whereCharacter.top = height

    if whereCharacter.left > width: #character bounces from the edge
        whereCharacter.left = whereCharacter.left-70
    if whereCharacter.right < 0:
        whereCharacter.right = whereCharacter.right+70
    if whereCharacter.top > height:
        whereCharacter.top = whereCharacter.top-70
    if whereCharacter.bottom < 0:
        whereCharacter.bottom = whereCharacter.bottom+70

    if whereCharacter.left < 0 or whereCharacter.right > width or whereCharacter.top < 0 or whereCharacter.bottom > height:
        disp.fill(red) #while character is partly out of window background turns red
    else:
        disp.fill(black) #otherwise background is black

    pointsText = fontPoints.render('Points: '+str(points), True, turquise)

    #displaying everything
    for i in range(0,len(mouseList)):
        disp.blit(mouseList[i], whereList[i])
    disp.blit(character, whereCharacter)
    disp.blit(rectangle, whereRectangle)
    disp.blit(square, whereSquare)
    disp.blit(dog, whereDog)
    disp.blit(pointsText, (0,0))
    disp.blit(highScoreText, (0, 30))

    pygame.display.flip()   #updates
