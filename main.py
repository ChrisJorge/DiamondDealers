#____________________ Import Necessary Libraries and classes _______________________
import pygame as game # Import the pygame module

from Components import GameSelectionFrame, WriteText # Import the components from component class

from BlackJackLogic import BlackJack

from HorseRacingLogic import HorseRacing

#____________________ Initialize The Screen _________________________________________
game.init() # Initialize the pygame module 

game.display.set_caption('Diamond Dealers Casino') # Create the title of the terminal

game.display.set_icon(game.image.load('./Logo.png')) # Create the logo for the terminal

systemInformation = game.display.Info() # Get the system information
systemWidth = systemInformation.current_w # Create a variable with the system width
systemHeight = systemInformation.current_h # Create a variable with the system height

screen = game.display.set_mode((systemWidth - 100,systemHeight - 100))  # Create the screen (width (X), height (Y))
gameBeingPlayed = 'None'
playerMoney = 200
mainScreen = False
activateSecondGame = False
def returnToMainMenu():
    global gameBeingPlayed
    global playerMoney
    global mainScreen
    global activateSecondGame

    playerMoney = gameBeingPlayed.playerMoney
    gameBeingPlayed = 'None'
    mainScreen = False
    activateSecondGame = False
    game.event.clear()
    clearScreen()

def changeGame(num):
    global gameBeingPlayed
    global playerMoney
    global mainScreen
    

    match num:
        case 0:
            print('Inside 0')
            gameBeingPlayed = 'None'
        case 1:
            print('Inside 1')
            gameBeingPlayed = BlackJack(screen, systemHeight - 100, systemWidth - 100, playerMoney)
            mainScreen = False
        case 2:
            print('Inside 2', mainScreen)
            gameBeingPlayed = HorseRacing(screen, systemHeight - 100, systemWidth - 100, playerMoney)

def clearScreen():
    rectangle = game.Rect(0,0,systemWidth - 100, systemHeight - 100)
    game.draw.rect(screen, (0,0,0), rectangle)


#_____________________ Run the game _________________________________________________
gameRunning = True # Initialize a variable indicating if the game is currently running
while gameRunning:
    mouse = game.mouse.get_pos()
    for event in game.event.get(): # Check for events happening on the game terminal
        if event.type == game.QUIT: # Check if the event is quit (clicking the red exit button)
            gameRunning = False # Turn the game off
    if gameBeingPlayed == 'None':
            WriteText(screen, 40, 'Select A Game', (255,255,255), (0,0,0), systemWidth / 2.33, 0)
            blackJackOption = GameSelectionFrame(screen, 'Black Jack', (systemHeight / 2) - (systemHeight / 15), systemWidth / 2, (140,68,78), (0,0,0), './StartingScreenAssets/BlackJackGameImage.png', 0, systemHeight / 15)
            horseRaceOption = GameSelectionFrame(screen, 'Horse Racing',  (systemHeight / 2) - (systemHeight / 15), systemWidth / 2, (100,60,99), (0,0,0), './StartingScreenAssets/HorseRacingGameImage.png', systemWidth / 2, systemHeight / 15)
            blackJackOption.frameButton.action(lambda: changeGame(1))
            horseRaceOption.frameButton.action(lambda: changeGame(2))
    if gameBeingPlayed != 'None' and gameBeingPlayed.gameType == 'blackJack':
        if gameBeingPlayed.animatePlayerCard:
            XIncrease = (gameBeingPlayed.xStartingPoint - 200) / 30
            YIncrease = ((systemHeight - 600) - 197) / 30
            gameBeingPlayed.animationX += XIncrease
            gameBeingPlayed.animationY += YIncrease
            gameBeingPlayed.animateCard(gameBeingPlayed.cardBeingAnimated, gameBeingPlayed.animationX, gameBeingPlayed.animationY, True)
        elif gameBeingPlayed.animateDealerCard:
            XIncrease = (gameBeingPlayed.xStartingPoint - 200) / 30
            YIncrease = (100 - 180) / 30
            gameBeingPlayed.animationX += XIncrease
            gameBeingPlayed.animationY += YIncrease
            gameBeingPlayed.animateCard(gameBeingPlayed.cardBeingAnimated, gameBeingPlayed.animationX, gameBeingPlayed.animationY, False)

        if gameBeingPlayed.betOption == 1:
            gameBeingPlayed.chip1Button.action(lambda: gameBeingPlayed.placeSingleBet())
            gameBeingPlayed.chip5Button.action(lambda: gameBeingPlayed.placeFiveBet())
            gameBeingPlayed.chip10Button.action(lambda: gameBeingPlayed.placeTenBet())
            gameBeingPlayed.chip25Button.action(lambda: gameBeingPlayed.placeTwentyFiveBet())
        else:
            gameBeingPlayed.chip50Button.action(lambda: gameBeingPlayed.placeFiftyBet())
            gameBeingPlayed.chip100Button.action(lambda: gameBeingPlayed.placeHundredBet())
            gameBeingPlayed.chip500Button.action(lambda: gameBeingPlayed.placeFiveHundredBet())
            gameBeingPlayed.chip1000Button.action(lambda: gameBeingPlayed.placeThousandBet())
        
        gameBeingPlayed.changeChipsLeftButton.action(lambda: gameBeingPlayed.handleChangeChipsOnLeft())
        gameBeingPlayed.changeChipsRightButton.action(lambda: gameBeingPlayed.handleChangeChipsOnRight())
        gameBeingPlayed.helpButton.action(lambda: gameBeingPlayed.toggleHelp())
        gameBeingPlayed.removeBetButton.action(lambda: gameBeingPlayed.removeBet())
        gameBeingPlayed.confirmBetButton.action(lambda: gameBeingPlayed.confirmBet())
        gameBeingPlayed.hitButton.action(lambda: gameBeingPlayed.handleHitButton())
        gameBeingPlayed.standButton.action(lambda: gameBeingPlayed.handleStayButton())
        gameBeingPlayed.exitButton.action(lambda: returnToMainMenu())

    elif gameBeingPlayed != 'None' and gameBeingPlayed.gameType == 'horseRacing':
        gameBeingPlayed.horse1Button.action(lambda: gameBeingPlayed.selectHorse(1))
        gameBeingPlayed.horse2Button.action(lambda: gameBeingPlayed.selectHorse(2))
        gameBeingPlayed.horse3Button.action(lambda: gameBeingPlayed.selectHorse(3))
        gameBeingPlayed.horse4Button.action(lambda: gameBeingPlayed.selectHorse(4))
        gameBeingPlayed.oneDollarBet.action(lambda: gameBeingPlayed.placeBet(1))
        gameBeingPlayed.fiveDollarBet.action(lambda: gameBeingPlayed.placeBet(5))
        gameBeingPlayed.tenDollarBet.action(lambda: gameBeingPlayed.placeBet(10))
        gameBeingPlayed.twentyFiveDollarBet.action(lambda: gameBeingPlayed.placeBet(25))
        gameBeingPlayed.fiftyDollarBet.action(lambda: gameBeingPlayed.placeBet(50))
        gameBeingPlayed.oneHundredDollarBet.action(lambda: gameBeingPlayed.placeBet(100))
        gameBeingPlayed.fiveHundredDollarBet.action(lambda: gameBeingPlayed.placeBet(500))
        gameBeingPlayed.oneThousandDollarBet.action(lambda: gameBeingPlayed.placeBet(1000))
        gameBeingPlayed.fiveThousandDollarBet.action(lambda: gameBeingPlayed.placeBet(5000))
        gameBeingPlayed.removeBetButton.action(lambda: gameBeingPlayed.removeBet())  
        gameBeingPlayed.confirmBetButton.action(lambda: gameBeingPlayed.confirmBet())
        if gameBeingPlayed.raceStarted == False and gameBeingPlayed.winnerFound == False:
            gameBeingPlayed.currentTime = int((game.time.get_ticks() - gameBeingPlayed.startTime) / 1000)
            gameBeingPlayed.updateTime()
        elif gameBeingPlayed.raceStarted == True and gameBeingPlayed.winnerFound == False:
            gameBeingPlayed.horse1.horseX += gameBeingPlayed.horse1.speed
            gameBeingPlayed.horse2.horseX += gameBeingPlayed.horse2.speed
            gameBeingPlayed.horse3.horseX += gameBeingPlayed.horse3.speed
            gameBeingPlayed.horse4.horseX += gameBeingPlayed.horse4.speed
            gameBeingPlayed.moveHorses()
        gameBeingPlayed.exitButton.action(lambda: returnToMainMenu())
    game.display.update() # update the content that appears on the screen 