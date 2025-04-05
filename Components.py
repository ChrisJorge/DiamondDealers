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

    def write(self, text, size, color = (0,0,0)): # Function to add text to the button
        font = game.font.SysFont('Calibri', size, True, False) # Initialize the type of font
        self.text = font.render(text,True, color) # Render the text
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

class WriteText:
    
    def __init__(self, screen, size, text, textColor, backGroundColor, xCoordinate, yCoordinate):
        self.font = game.font.SysFont('Times New Roman', size, True, False)
        self.screen = screen
        self.textColor = textColor
        self.backGroundColor = backGroundColor
        textToPlace = self.font.render(text, True, self.textColor)
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
        
        self.screen.blit(textToPlace,(self.xCoordinate, self.yCoordinate))
    
    def update(self, text, extra = 0, minus = 0):
        textToPlace = self.font.render(text, True, self.textColor)
        self.remove(textToPlace.get_width() + extra, textToPlace.get_height())
        self.screen.blit(textToPlace,(self.xCoordinate - minus, self.yCoordinate))
    

    def remove(self,width, height):
        rectangle =  game.Rect(self.xCoordinate, self.yCoordinate, width + 25, height + 10)
        game.draw.rect(self.screen, self.backGroundColor, rectangle)

class GameSelectionFrame:

    def __init__(self, screen, gameName, height, width, frameColor, textColor, image, xCoordinate, yCoordinate):
        self.screen = screen
        self.gameName = gameName
        self.height = height
        self.width = width
        self.frameColor = frameColor
        self.textColor = textColor 
        self.image = game.image.load(image)
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
        self.rectangle =  game.Rect(self.xCoordinate, self.yCoordinate, self.width, self.height) # Create the Frame
        self.createButton()
        game.draw.rect(self.screen, self.frameColor, self.rectangle) # Draw the button onto the screen
        self.writeTitle()
        self.placeImage()

    def writeTitle(self):
        self.font = game.font.SysFont('Times New Roman', 50, True, False)
        self.titleForFrame = self.font.render(self.gameName,True, self.textColor)
        self.screen.blit(self.titleForFrame, ((self.width // 2) - (self.titleForFrame.get_width() // 2) + self.xCoordinate, self.yCoordinate + self.titleForFrame.get_height() // 2))
    
    def placeImage(self):
        self.image = game.transform.scale(self.image, (self.width, self.height - self.titleForFrame.get_height()))
        self.screen.blit(self.image, (self.xCoordinate, self.yCoordinate + self.titleForFrame.get_height() + 20))
    
    def createButton(self):
        self.frameButton = Button(self.screen, self.frameColor, self.height, self.width, self.xCoordinate, self.yCoordinate)

class HorseFrame:

    def __init__(self, screen, frameHeight, frameWidth, image, horseNumber, odds, color, xCoordinate, yCoordinate):
        self.screen = screen
        self.frameHeight = frameHeight
        self.frameWidth = frameWidth
        self.image = image
        self.horseNumber = horseNumber
        self.odds = odds
        self.color = color
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate

        self.initializeFrame()

    def initializeFrame(self):
        frame = game.Rect(self.xCoordinate, self.yCoordinate, self.frameWidth, self.frameHeight)
        game.draw.rect(self.screen, self.color, frame)
        self.screen.blit(self.image, (0, self.frameHeight // 6.5 + self.yCoordinate))
        WriteText(self.screen, 25, f'Horse {self.horseNumber}', (0,0,0), self.color, self.frameWidth // 2.75, self.frameHeight // 2.5 + self.yCoordinate)
        self.betAmountText = WriteText(self.screen, 17, '$0', (0,0,0), self.color, self.frameWidth - (self.frameWidth // 3), self.yCoordinate)
        self.oddsText = WriteText(self.screen, 17, f'Odds: ${self.odds}', (0,0,0), self.color, self.frameWidth - (self.frameWidth // 3), self.yCoordinate + self.frameHeight * .70)