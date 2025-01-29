import pygame as game

game.font.init() # Initialize the pyfame font function, used to put text in buttons

class Button():

    def __init__(self, screen, colorRGB, height, width, xCoordinate, yCoordinate): # Function to initialize the button class
        self.xCoordinate = xCoordinate # Initialize xCoordinate, used to place button on screen 
        self.yCoordinate = yCoordinate # Initialize yCoordinate, used to place button on screen
        self.height = height # Initialize height, used to determine button height
        self.width = width  # Initilaize width, used to determine button width
        self.screen = screen # Initialize the screen, used to put the buttons on the screen
        self.color = colorRGB # Initialize color, used to determine the buttons color
        self.rectangle =  game.Rect(self.xCoordinate, self.yCoordinate, self.width, self.height) # Create the button
        self.clicked = False # Initialize the buttons clicked value, used to determine if button has been clicked
        game.draw.rect(self.screen, self.color, self.rectangle) # Draw the button onto the screen

    def write(self, text, size): # Function to add text to the button
        font = game.font.SysFont('Calibri', size, True, False) # Initialize the type of font
        self.text = font.render(text,True, (0,0,0)) # Render the text
        self.middleWidth = self.width // 2 # Get the middle of the button width wise
        self.middleHeight = self.height // 2 # Get the middle of the button height wise
        # place the text at the center of the button
        self.screen.blit(self.text, [(self.xCoordinate - (self.text.get_width() // 2)) + self.middleWidth, self.yCoordinate - (self.text.get_height() // 2) + self.middleHeight])


    def action(self, func): # Function to add functionality to the button
        mousePosition = game.mouse.get_pos() # Get the mouse position on the screen
        if self.rectangle.collidepoint(mousePosition): # Check if mouse cursor is colliding with the button
            if game.mouse.get_pressed()[0] == 1 and self.clicked == False: # Check if button has been right clicked and the button has not been clicked yet
                self.clicked = True # Set self.clicked to true
                func() # Call the function linked to the button
            if game.mouse.get_pressed()[0] == 0: # Check if button is no longer being clicked
                self.clicked = False # Set self.clicked to false


class CenterBox:
    def __init__(self, screen, screenHeight, screenWidth , colorRGB, winner):
        self.screen = screen
        self.screenHeight = screenHeight
        self.screenWidth = screenWidth
        self.colorRGB = colorRGB
        self.winner = winner
        self.height, self.width, self.yCoordinate, self.xCoordinate = self.center()
        self.rectangle = game.Rect(self.xCoordinate, self.yCoordinate, self.width, self.height)
        game.draw.rect(self.screen, self.colorRGB, self.rectangle)
        self.write(self.screenHeight // 2, self.screenWidth // 2, self.xCoordinate, self.yCoordinate, winner, 25)
        self.button = Button(screen, (85, 86, 99) ,self.height // 2, self.width // 2, self.xCoordinate + self.width // 3.75, self.yCoordinate + self.height // 3.5)
        self.button.write('Replay', 15)
    
    def center(self,):
        self.centerHeight = self.screenHeight // 2
        self.centerWidth = self.screenWidth // 2
        topHeight = (self.centerHeight + (self.centerHeight * 0.15))
        bottomHeight = (self.centerHeight - (self.centerHeight * 0.15))
        height = (topHeight - bottomHeight) + self.centerWidth * 0.15
        yCoordinate = (self.centerHeight - (height * 0.50))
        width = height * 2
        xCoordinate = (self.centerWidth - width // 7.25)
        return height, width, yCoordinate, xCoordinate        

    def write(self, centerHeight, centerWidth, xCoordinate, yCoordinate, winner, size):
        font = game.font.SysFont('Calibri', size, True, False) # Initialize the type of font
        if winner == 0:
            self.text = font.render('Player wins',True, (0,0,0)) # Render the text
        else:
            self.text = font.render('Dealer wins',True, (0,0,0)) # Render the text
        self.screen.blit(self.text, [((self.text.get_width() // 2) + (centerWidth + xCoordinate // 12.5)), ((self.text.get_height() // 2) + ((centerHeight - (yCoordinate // 2.5))))])
