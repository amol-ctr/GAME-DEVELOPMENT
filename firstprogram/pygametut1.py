import pygame
import random
import os

#for importing music
pygame.mixer.init()

#FOR CHECKING WHETHER PYGAME IS IMPORTED PROPERLY
x=pygame.init()

# for background image
bgimg = pygame.image.load('snakes.jpg')
bgimg = pygame.transform.scale(bgimg, (900, 500))#.convert_alpha()
bgimg1 = pygame.image.load('game.jpg')
bgimg1 = pygame.transform.scale(bgimg1, (900, 500))#.convert_alpha()
bgimg2 = pygame.image.load('game_over.jpeg')
bgimg2 = pygame.transform.scale(bgimg2, (900, 500))#.convert_alpha()

#INITIALILIZING GAME WINDOW VARIABLES
gameWindow=pygame.display.set_mode((900,500))
pygame.display.set_caption(("Snake Game"))
pygame.display.update()

#colors
white=(255,255,255)
red=(255,0,0)
black=(0,0,0)

def text_screen(text,color,x,y,font_size):
    font = pygame.font.SysFont(None, font_size, bold=False, italic=False)
    screen_text=font.render(text,True,color)
    gameWindow.blit(screen_text,[x,y])
#clock
clock=pygame.time.Clock()

#creating snake and increasing the length
def plot_snake(gameWindow,color,snk_list,snk_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow,black,[x,y,snk_size,snk_size])

def welcome():
    exit_game=False
    while not exit_game:

        # defining color of game screen
        gameWindow.fill(white)
        gameWindow.blit(bgimg,(0,0))

        text_screen("WELCOME TO SNAKES", black, 20,400,35)
        text_screen("PRESS ENTER TO PLAY", black, 20,430,35)
        pygame.display.update()

        for event in pygame.event.get():
            pygame.mixer.music.load('beginning.mp3')
            pygame.mixer.music.play()
            if event.type == pygame.QUIT:
                exit_game=True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameloop()
        pygame.display.update()
def gameloop():
    fps=60 #FRAMES PER SECOND

    #POSITION AND VELOCITY OF SNAKE
    snake_x=63
    snake_y=42
    snake_size=20
    velocity_x=0
    velocity_y=0

    init_velocity=5

    #position for food
    food_x=random.randint(200,700) #we are taking such range so that food remains in the middle of screen
    food_y=random.randint(150,300)

    #score
    score=0

    snk_list=[]
    snake_list_size=1

    # checking if hiscore exists
    if(not os.path.exists("hiscore.txt")):
        with open("hiscore.txt", "w") as f:
            f.write("0")

    with open("hiscore.txt","r") as f:
        hiscore=f.read()
        hiscore1 = int(hiscore)
    exit_game=False
    game_over=False

    while not exit_game:

        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))

            gameWindow.fill((233,220,229))
            gameWindow.blit(bgimg2, (0, 0))

            text_screen("Game over!",red,60,200,55)
            text_screen("Press Enter to return to main window", red, 60, 250, 55)
            text_screen("Press space bar to continue", red, 60, 300, 55)
            if(score>hiscore1):
                text_screen("CONGRATULATIONS! YOU HAVE MADE A NEW HIGH SCORE: "+str(score), (0,0,255), 40, 100, 30)
            else:
                text_screen("SCORE: " + str(score), (0, 0, 255), 60, 100, 50)
            pygame.display.update()
            for event in pygame.event.get():
                pygame.mixer.music.load('beginning.mp3')
                pygame.mixer.music.play(0,2,0)
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        exit_game = True
                        welcome()
                    if event.key==pygame.K_SPACE:
                        gameloop()

        else:
            for event in pygame.event.get():
                #QUITING THE GAME
                if event.type==pygame.QUIT:
                    exit_game=True

                #IF USER PRESSES ANY KEY
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RIGHT:
                        snake_x=snake_x+10
                        velocity_y=0
                        velocity_x=init_velocity
                    if event.key==pygame.K_LEFT:
                        snake_x=snake_x-10
                        velocity_y=0
                        velocity_x = -init_velocity
                    if event.key==pygame.K_DOWN:
                        snake_y=snake_y+10
                        velocity_x=0
                        velocity_y = init_velocity
                    if event.key==pygame.K_UP:
                        snake_y=snake_y-10
                        velocity_x=0
                        velocity_y = -init_velocity
                    # CHEAT CODES
                    if event.key==pygame.K_q:
                        score+=5
                        print("SCORE: ", score)
                        text_screen("Score: " + str(score) + "  HIGH SCORE: " + str(hiscore), red, 600,10,25)
            snake_x=snake_x+velocity_x
            snake_y=snake_y+velocity_y

            if abs(food_x - snake_x) < snake_size and abs(food_y - snake_y) < snake_size:
                score += 10
                pygame.mixer.music.load('beep.mp3')
                pygame.mixer.music.play()
                print("SCORE: ", score)
                food_x = random.randint(100,700)  # we are taking such range so that food remains in the middle
                food_y = random.randint(50,400)
                snake_list_size += 5

            if(score>int(hiscore)):
                hiscore=score

            gameWindow.fill((233,220,229))
            gameWindow.blit(bgimg1, (0, 0))
            text_screen("Score: "+str(score)+"  HIGH SCORE: "+str(hiscore),red,600,10,25)
            plot_snake(gameWindow,black,snk_list,snake_size)
            pygame.draw.ellipse(gameWindow,red,[food_x,food_y,20,20])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if (len(snk_list) > snake_list_size):
                del snk_list[0]

            # collision with itself
            if head in snk_list[:-1]:
                pygame.mixer.music.load('collision.mp3')
                pygame.mixer.music.play(0,-10,0)
                pygame.display.update()
                game_over = True

            if snake_x < 63 or snake_x > 820 or snake_y < 42 or snake_y > 445:
                pygame.mixer.music.load('collision.mp3')
                pygame.mixer.music.play(0,-10,0)
                pygame.display.update()
                game_over = True

        clock.tick(fps)
        pygame.display.update()

    pygame.quit()
    quit()
welcome()