import pygame as game

game.font.init()

class Button():

    def __init__(self, screen, colorRGB, height, width, xCoordinate, yCoordinate):
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
        self.height = height
        self.width = width 
        self.screen = screen
        self.color = colorRGB
        self.rectangle =  game.Rect(self.xCoordinate, self.yCoordinate, self.width, self.height)
        self.clicked = False
        game.draw.rect(self.screen, self.color, self.rectangle)

    def write(self, text, size):
        font = game.font.SysFont('Calibri', size, True, False)
        self.text = font.render(text,True, (0,0,0))
        self.middleWidth = self.width // 2
        self.middleHeight = self.height // 2
        self.screen.blit(self.text, [(self.xCoordinate - (self.text.get_width() // 2)) + self.middleWidth, self.yCoordinate - (self.text.get_height() // 2) + self.middleHeight])


    def action(self, func):
        mousePosition = game.mouse.get_pos()

        if self.rectangle.collidepoint(mousePosition): # Check if mouse cursor is colliding with the button
            if game.mouse.get_pressed()[0] == 1 and self.clicked == False: # Check if button has been right clicked and the button has not been clicked yet
                self.clicked = True
                func(self.screen)
            if game.mouse.get_pressed()[0] == 0:
                self.clicked = False