#____________________ Import Necessary Libraries and classes _______________________
import pygame as game # Import the pygame module

from Components import Button, Write # Import the components from component class

from BlackJackLogic import BlackJack

#____________________ Initialize The Screen _________________________________________
game.init() # Initialize the pygame module 

game.display.set_caption('Diamond Dealers Casion') # Create the title of the terminal

game.display.set_icon(game.image.load('./Logo.png')) # Create the logo for the terminal

systemInformation = game.display.Info() # Get the system information
systemWidth = systemInformation.current_w # Create a variable with the system width
systemHeight = systemInformation.current_h # Create a variable with the system height

screen = game.display.set_mode((systemWidth - 100,systemHeight - 100))  # Create the screen (width (X), height (Y))

screen.fill((78, 106, 84)) # Set the background color 

#____________________ Initialize Content On Screen _________________________________________
game.draw.rect(screen, (211, 211, 211), game.Rect(0,0,systemWidth * 0.2, systemHeight)) # Create the gray bar on the left side which will contain the options 

hitButton = Button(screen, (85, 86, 99), systemHeight // 16, (systemWidth * 0.2) // 2, systemHeight // 16, (systemWidth * 0.2) // 2) # Initialize and create the hit button
holdButton = Button(screen,(85, 86, 99), systemHeight // 16, (systemWidth * 0.2) // 2, systemHeight // 16, ((systemWidth * 0.2) // 2) * 2) # Initialize and create the stand button
restartButton = Button(screen,(85, 86, 99), systemHeight // 16, (systemWidth * 0.2) // 2, systemHeight // 16, ((systemWidth * 0.2) // 2) * 3) # Initialize and create the stand button
quitButton = Button(screen, (85, 86, 99), systemHeight // 16, (systemWidth * 0.2) // 2, systemHeight // 16, ((systemWidth * 0.2) // 2) * 4) # Initialize and create the quit button

hitButton.write('Hit', 15) # Add text to the hit button
holdButton.write('Hold', 15) # Add text to the stand button
restartButton.write('Restart', 15) # Add text to the restart button
quitButton.write('Quit', 15) # Add text to the quit button

#____________________ Initialize Necessary class logic  _________________________________________
blackJack = BlackJack(screen, systemHeight - 100, systemWidth - 100) # Black jack is used to output the cards on screen and handle all of the calculations behind the sceen
winnerText = Write(screen, 25, systemWidth + (systemWidth * 0.2), systemHeight) # winnerText is used to ouput who won the game to the screen, is used in conjunction with BlackJack
#_____________________ Run the game _________________________________________________
gameRunning = True # Initialize a variable indicating if the game is currently running
while gameRunning:
    hitButton.action(lambda : blackJack.addPlayerCard()) # Initalize the hit buttons ability
    holdButton.action( lambda: blackJack.hold()) # Initialize the stand buttons ability
    restartButton.action(lambda: blackJack.restartGame()) # Initialize the restart buttons ability
    for event in game.event.get(): # Check for events happening on the game terminal
        if event.type == game.QUIT: # Check if the event is quit (clicking the red exit button)
            gameRunning = False # Turn the game off
    if blackJack.winner  == 1 or blackJack.winner == 0 or blackJack.winner  == 2: # Check if someone has won the game
        winnerText.Winner(blackJack.winner) # Output who won the game to the screen
    game.display.update() # update the content that appears on the screen 