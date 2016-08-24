import pygame
from cell import Cell
import random
import time
import sys


'''
Utility methods
'''

def draw_ladder(start, end):
    pygame.draw.line(gameDisplay, red, (start.center_x, start.center_y), (end.center_x, end.center_y), 6)
    Ladders[start] = end

def draw_all_ladders():
    draw_ladder(Cells[6], Cells[31])
    draw_ladder(Cells[20], Cells[39])
    draw_ladder(Cells[61], Cells[99])
    draw_ladder(Cells[77], Cells[97])
    draw_ladder(Cells[67], Cells[86])
    draw_ladder(Cells[71], Cells[92])

def draw_snake(start, end):
    pygame.draw.line(gameDisplay, blue, (start.center_x, start.center_y), (end.center_x, end.center_y), 6)
    Snakes[start] = end

def draw_all_snakes():
    draw_snake(Cells[44], Cells[3])
    draw_snake(Cells[53], Cells[34])
    draw_snake(Cells[63], Cells[37])
    draw_snake(Cells[68], Cells[27])
    draw_snake(Cells[75], Cells[43])
    draw_snake(Cells[96], Cells[83])

def draw_pointer(x, y):
    pygame.draw.circle(gameDisplay, white, (x, y), 25, 2)

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def button(msg, x, y, w, h, ic, ac, action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y :
        pygame.draw.rect(gameDisplay, ac, (x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText, yellow)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def random_generator():

    global to_move
    global number_of_moves

    smallText = pygame.font.Font("freesansbold.ttf",40)
    pygame.draw.circle(gameDisplay, black, (1100,600), 30, 0)

    to_move = random.randint(1,6)
    number_of_moves += 1
    textSurf, textRect = text_objects(str(to_move), smallText, yellow)
    textRect.center = (1100, 600)
    gameDisplay.blit(textSurf, textRect)

    move_pointer()

def move_pointer():
    global pointer_location
    global to_move
    global Ladders
    global Snakes
    global done
    global won

    current_cell = Cells[pointer_location]
    pygame.draw.rect(gameDisplay, black, (current_cell.x, current_cell.y, cell_width, cell_height), 0)
    c = Cell(current_cell.x, current_cell.y, str(pointer_location + 1), gameDisplay)

    pointer_location = pointer_location + to_move

    if (pointer_location >= 99):
        done = True
        won = True
        print_victory_message()

    else:
        new_cell = Cells[pointer_location]

        if new_cell in Ladders.keys() :
            new_cell = Ladders[new_cell]
            draw_pointer(new_cell.center_x, new_cell.center_y)

        elif new_cell in Snakes.keys() :
            new_cell = Snakes[new_cell]
            draw_pointer(new_cell.center_x, new_cell.center_y)

        else:
            draw_pointer(new_cell.center_x, new_cell.center_y)

        pointer_location = int(new_cell.number) - 1

        if pointer_location == 99 :
            done = True
            print_victory_message()

def print_victory_message():
    global number_of_moves
    smallText = pygame.font.SysFont('comicsansms', 50)
    textSurf, textRect = text_objects("Game over! You completed in " + str(number_of_moves) + " moves", smallText, red)
    textRect.center = (600,100)
    gameDisplay.blit(textSurf, textRect)


'''
main loop with the game loop inside
'''

pygame.init()

display_width = 1200
display_height = 900

cell_width = 70
cell_height = 70

first_cell_x = 250
first_cell_y = 800

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snakes and Ladders')

black = (0,0,0)
white = (255,255,255)
yellow = (255,255,0)
red = (255,0,0)
blue = (0,0,255)
bright_green = (0, 255, 0)
green = (0, 200, 0)

clock = pygame.time.Clock()
done = False
won = False

Cells = []
Ladders = {}
Snakes = {}

to_move = 0
pointer_location = 0
number_of_moves = 0

draw_pointer(first_cell_x + cell_width/2, first_cell_y + cell_height/2)

while not done:
    fwd = True
    cur_x, cur_y = first_cell_x , first_cell_y
    for i in xrange(10):
        for j in xrange(1, 11):
            if (fwd):
                c = Cell(cur_x, cur_y, str(i*10 + j), gameDisplay)
                cur_x = cur_x + cell_width
                Cells.append(c)

            else:
                c = Cell(cur_x, cur_y, str(i*10 + j), gameDisplay)
                cur_x = cur_x - cell_width
                Cells.append(c)

        cur_y = cur_y - cell_height
        if (fwd):
            cur_x = cur_x - cell_width
        else:
            cur_x = cur_x + cell_width

        fwd = not fwd

    draw_all_ladders()
    draw_all_snakes()

    button("Roll it!", 1050, 400, 100, 50, green, bright_green, random_generator)

    pygame.draw.circle(gameDisplay, white, (1100, 600), 50, 5)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                random_generator()

    pygame.display.update()
    clock.tick(30)

if (done and not won):
    pygame.quit()

else:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
