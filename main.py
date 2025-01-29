#____________________ Import Necessary Libraries and classes _______________________
import pygame as game # Import the pygame module

from Components import Button # Import the button class

from BlackJackLogic import BlackJack


#____________________ Initialize The Screen ___________________________
game.init() # Initialize the pygame module 

game.display.set_caption('Diamond Dealers Casion') # Create the title of the terminal

game.display.set_icon(game.image.load('./Logo.png')) # Create the logo for the terminal

systemInformation = game.display.Info() # Get the system information
systemWidth = systemInformation.current_w # Create a variable with the system width
systemHeight = systemInformation.current_h # Create a variable with the system height

screen = game.display.set_mode((systemWidth - 100,systemHeight - 100))  # Create the screen (width (X), height (Y))

gameRunning = True # Initialize a variable indicating if the game is currently running

screen.fill((78, 106, 84)) # Set the background color 

game.draw.rect(screen, (211, 211, 211), game.Rect(0,0,systemWidth * 0.2, systemHeight)) # Create the gray bar on the left side which will contain the options 

blackJack = BlackJack(screen, systemHeight - 100, systemWidth - 100)

hitButton = Button(screen, (85, 86, 99), systemHeight // 16, (systemWidth * 0.2) // 2, systemHeight // 16, (systemWidth * 0.2) // 2) # Initialize and create the hit button
standButton = Button(screen,(85, 86, 99), systemHeight // 16, (systemWidth * 0.2) // 2, systemHeight // 16, ((systemWidth * 0.2) // 2) * 2) # Initialize and create the stand button
quitButton = Button(screen, (85, 86, 99), systemHeight // 16, (systemWidth * 0.2) // 2, systemHeight // 16, ((systemWidth * 0.2) // 2) * 3) # Initialize and create the quit button

hitButton.write('Hit', 15) # Add text to the hit button
standButton.write('Stand', 15) # Add text to the stand button
quitButton.write('Quit', 15) # Add text to the quit button

# test = game.image.load('./BlackJackAssets/FiveDiamond.svg')
# w = test.get_width()
# h = test.get_height()
# test = game.transform.scale(test,(150, 200))
# screen.blit(test,(300, 500))


# screen.blit(test,(300, 500))

while gameRunning:
    hitButton.action(lambda : blackJack.addPlayerCard()) # Initalize the hit buttons ability
    standButton.action( lambda: blackJack.addPlayerCard()) # initialize the stand buttons ability
    for event in game.event.get():
        if event.type == game.QUIT:
            gameRunning = False
    
    game.display.update() # update the content that appears on the screen