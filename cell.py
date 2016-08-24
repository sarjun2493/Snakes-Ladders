import pygame

white = (255,255,255)
yellow = (255,255,0)

cell_width = 70
cell_height = 70

class Cell:

    def __init__(self, x, y, number, gameDisplay):
        self.x = x
        self.y = y
        self.center_x = x + cell_width/2;
        self.center_y = y + cell_height/2;
        self.number = str(number)

        pygame.draw.rect(gameDisplay, white, (x,y,cell_width,cell_height), 2)
        smallText = pygame.font.SysFont('comicsansms', 30)
        textSurf, textRect = self.text_objects(number, smallText)
        textRect.center = (x + (cell_width/2), (y + (cell_height/2)))
        gameDisplay.blit(textSurf, textRect)


    def text_objects(self, text, font):
        textSurface = font.render(text, True, yellow)
        return textSurface, textSurface.get_rect()
