import pygame
import random
import os

pygame.mixer.init()  # this is for music

pygame.init()


# colors
white = (255, 255, 255)
red = (255, 0 , 0)
black = (0, 0, 0)

# creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

#Background Image
bgimg = pygame.image.load("background.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

bgimg2 = pygame.image.load("snake.jpg")
bgimg2 = pygame.transform.scale(bgimg2, (screen_width, screen_height)).convert_alpha()

bgimg3 = pygame.image.load("oops.jpg")
bgimg3 = pygame.transform.scale(bgimg3, (screen_width, screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption("SnakesWithAnkit")
pygame.display.update()

clock = pygame.time.Clock()



font = pygame.font.SysFont(None, 55)    # here NONE means default font which is there that i am taking, and 55 is font size.
def text_screen(text, color, x, y):  # here arguments are text-what i want to put on screen, color- color of the text, and x,y is the position where i want to put this text on my screen.
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [round(x),round(y)])

def plot_snake(gameWindow, color, snake_list, snake_size):
    for x,y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])   

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((233,210,229))
        gameWindow.blit(bgimg2, (0,0))
        text_screen("WELCOME TO SNAKES", red, 230, 265)    
        text_screen("Press SpaceBar to Play", red, 230, 315)    
        text_screen("Made By", red, 50, 515)    
        text_screen("Upadhyay Ankit", red, 70, 550)    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('back.mp3')
                    pygame.mixer.music.play()
                    gameloop()    

        pygame.display.update()
        clock.tick(40)        


# Game loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    init_velocity = 5
    snake_size = 20
    food_x = random.randint(20, screen_width/2)
    food_y = random.randint(20, screen_height/2)
    score = 0
    fps = 40
    snake_list = []
    snake_length = 1    
    # check if highscore file exists or not
    if(not os.path.exists("highscore.txt")):   # means what this does, if you have deleted your highscore file then this will automatically create that file.
        with open ("highscore.txt","w") as f:
            f.write("0")
    with open("highscore.txt","r") as f:
        highscore = f.read()

    while not exit_game:
        if game_over:
            with open("highscore.txt","w") as f:
                f.write(str(highscore))
            gameWindow.fill(white)
            gameWindow.blit(bgimg3, (0,0))
            text_screen("Game Over! Press Enter to continue", red, 100, 265)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()   

        else:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:   # this means when user click on above x button then game will exit 
                    exit_game = True

                if event.type == pygame.KEYDOWN:  # KEYDOWN means whenever i click any of the button and if that button is right, left, or down or top then what to do that depends on code.
                    if event.key == pygame.K_RIGHT:
                        # snake_x = snake_x + 10
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        # snake_x = snake_x - 10  
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        # snake_y = snake_y - 10
                        velocity_y = -init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        # snake_y = snake_y + 10    
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_q:
                        score += 10    

            snake_x += velocity_x
            snake_y += velocity_y            

            if abs(snake_x - food_x) < 6 and abs(snake_y - food_y) < 6:
                score += 10
                # print("score : ",score*10)  
                food_x = random.randint(20, screen_width/2)
                food_y = random.randint(20, screen_height/2)
                snake_length += 5
                if score > int(highscore):   # here we are typecasting the highscore to integer as it is coming from text as a string
                    highscore = score

            gameWindow.fill(white) 
            gameWindow.blit(bgimg, (0,0))
            text_screen("Score : " + str(score) + " HighScore : " + str(highscore), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > (snake_length):
                del snake_list[0]

            if head in snake_list[:-1]:    # means if head is there snake_list excluding last element i.e first head of snake
                game_over = True    
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True  
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play() 
                # print("Game Over")

            # pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size, snake_size])   # here it is use to draw rectangle. now it's argument gameWindow is where i am making this rectangle, another is color which i am keeping as black,then we give a list which contains the initial positions of the snake and then it's width(snake_size) and height(snake_size).
            plot_snake(gameWindow, black, snake_list, snake_size)
        pygame.display.update()   
        clock.tick(fps)   # In 1 sec how much frame we want it will give us that

    pygame.quit()
    quit()

welcome()   

