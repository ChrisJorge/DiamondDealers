#____________________ Import Necessary Libraries and classes _______________________
import pygame as game # Import the pygame module

from Components import Button # Import the components from component class

from BlackJackLogic import BlackJack

#____________________ Initialize The Screen _________________________________________
game.init() # Initialize the pygame module 

game.display.set_caption('Diamond Dealers Casino') # Create the title of the terminal

game.display.set_icon(game.image.load('./Logo.png')) # Create the logo for the terminal

systemInformation = game.display.Info() # Get the system information
systemWidth = systemInformation.current_w # Create a variable with the system width
systemHeight = systemInformation.current_h # Create a variable with the system height

screen = game.display.set_mode((systemWidth - 100,systemHeight - 100))  # Create the screen (width (X), height (Y))

blackJack = BlackJack(screen, systemHeight - 100, systemWidth - 100, 200)
#_____________________ Run the game _________________________________________________
gameRunning = True # Initialize a variable indicating if the game is currently running
while gameRunning:
    mouse = game.mouse.get_pos()
    for event in game.event.get(): # Check for events happening on the game terminal
        if event.type == game.QUIT: # Check if the event is quit (clicking the red exit button)
            gameRunning = False # Turn the game off
    
    if blackJack.animatePlayerCard:
        XIncrease = (blackJack.xStartingPoint - 200) / 30
        YIncrease = ((systemHeight - 600) - 197) / 30
        blackJack.animationX += XIncrease
        blackJack.animationY += YIncrease
        blackJack.animateCard(blackJack.cardBeingAnimated, blackJack.animationX, blackJack.animationY, True)
    elif blackJack.animateDealerCard:
        XIncrease = (blackJack.xStartingPoint - 200) / 30
        YIncrease = (100 - 180) / 30
        blackJack.animationX += XIncrease
        blackJack.animationY += YIncrease
        blackJack.animateCard(blackJack.cardBeingAnimated, blackJack.animationX, blackJack.animationY, False)

    blackJack.chip1Button.action(lambda: blackJack.placeSingleBet())
    blackJack.chip5Button.action(lambda: blackJack.placeFiveBet())
    blackJack.chip10Button.action(lambda: blackJack.placeTenBet())
    blackJack.chip25Button.action(lambda: blackJack.placeTwentyFiveBet())
    blackJack.helpButton.action(lambda: blackJack.toggleHelp())
    blackJack.removeBetButton.action(lambda: blackJack.removeBet())
    blackJack.confirmBetButton.action(lambda: blackJack.confirmBet())
    blackJack.hitButton.action(lambda: blackJack.handleHitButton())
    blackJack.standButton.action(lambda: blackJack.handleStayButton())
    game.display.update() # update the content that appears on the screen 