import pygame as game
# from BlackJackLogic import BlackJack
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

class Write:
    def __init__(self, screen, size, screenWidth, screenHeight, color = False):
        self.font = game.font.SysFont('Calibri', size, True, False)
        self.screen = screen
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.centerWidth = self.screenWidth // 2
        self.centerHeight = self.screenHeight // 2
        self.color = color
    
    def Winner(self, winner):
        match winner:
            case 0:
                text = self.font.render('Player wins',True, (0,0,0)) # Render the text
            case 1:
                text = self.font.render('Dealer wins',True, (0,0,0)) # Render the text
            case 2:
                text = self.font.render('Tie',True, (0,0,0)) # Render the text

        
        self.screen.blit(text,(self.centerWidth - (text.get_width()), self.centerHeight - (text.get_height() * 2)))
    
    def score(self,score, top):
        if top:
            text = self.font.render(f'Dealer Score: {score}', True, (0,0,0))
            self.remove(self.centerWidth - (text.get_width() // 2) + 5, self.centerHeight  // 4 - (text.get_height()), text.get_width(), text.get_height())
            self.screen.blit(text,(self.centerWidth - (text.get_width() // 2), self.centerHeight // 4 - (text.get_height() )))
        else:
            text = self.font.render(f'Player Score: {score}', True, (0,0,0))
            self.remove(self.centerWidth - (text.get_width() // 2) + 5, self.centerHeight * 1.75 + (text.get_height()), text.get_width(), text.get_height())
            self.screen.blit(text,(self.centerWidth - (text.get_width() // 2), self.centerHeight * 1.75 + (text.get_height())))

    def remove(self, xCoordinate, yCoordinate, width, height):
        rectangle =  game.Rect(xCoordinate, yCoordinate, width, height)
        game.draw.rect(self.screen, self.color, rectangle)
