import pygame as game
import random
from Components import WriteText, Button

class BlackJack:
    #____________________ Initializing Function _________________________________________

    def __init__(self, screen, screenHeight, screenWidth): # Function to initialize the blackjack class
        self.screen = screen # Used to populate screen with buttons, text, cards, chips
        self.screenHeight = screenHeight # Used to get the height of the game screen
        self.screenWidth = screenWidth # Used to get the width of the game screen
        self.playerMoney = 200
        self.betList = []
        self.bettingActive = True
        self.currentBet = 0 # Used to keep track of the current bet
        self.open = False


        self.initializeScreen()
    
    def initializeScreen(self): # Function to initialize the game screen

        self.screen.fill((78, 106, 84)) # Set the screen background color to casino green
        bottomBar = game.Rect(0, self.screenHeight - 200, self.screenWidth, 200) # Create the bottom brown bar that will hold all of the options
        game.draw.rect(self.screen, (106,84,78), bottomBar) # Place the bottom bar onto the screen

        self.chip1 = game.image.load('./BlackJackAssets/Chip1.svg') # Create the $1 chip
        self.chip5 = game.image.load('./BlackJackAssets/Chip5.svg') # Create the $5 chip
        self.chip10 = game.image.load('./BlackJackAssets/Chip10.svg') # Create the $10 chip
        self.chip25 = game.image.load('./BlackJackAssets/Chip25.svg') # Create the $25 chip

        self.chip1Button = Button(self.screen, (106,84,78), 105, 105, self.screenWidth - 125, self.screenHeight - 200) # Create a button to give the $1 chip functionality
        self.screen.blit(self.chip1,(self.screenWidth - 125, self.screenHeight - 200)) # Place the $1 chip on the screen ontop of the button

        self.chip5Button = Button(self.screen, (106,84,78), 105, 105, self.screenWidth - 250, self.screenHeight - 200) # Create a button to give the $5 chip functionality
        self.screen.blit(self.chip5,(self.screenWidth - 250, self.screenHeight - 200))  # Place the $5 chip on the screen ontop of the button

        self.chip10Button = Button(self.screen, (106,84,78), 105, 105, self.screenWidth - 375, self.screenHeight - 200) # Create a button to give the $10 chip functionality
        self.screen.blit(self.chip10,(self.screenWidth - 375, self.screenHeight - 200))  # Place the $10 chip on the screen ontop of the button
        
        self.chip25Button = Button(self.screen, (106,84,78), 105, 105, self.screenWidth - 500, self.screenHeight - 200) # Create a button to give the $25 chip functionality
        self.screen.blit(self.chip25,(self.screenWidth - 500, self.screenHeight - 200))  # Place the $25 chip on the screen ontop of the button

        self.playerMoneyText = WriteText(self.screen, 35, f'Money: ${self.playerMoney}', (255,255,255), (106,84,78), self.screenWidth - 350, self.screenHeight - 75) #self.screenHeight - 85, self.screenWidth - 400)
        self.playerBetText = WriteText(self.screen, 35, 'Player Bet: 0', (255,255,255), (106,84,78), 5, self.screenHeight - 175)
        self.playerScoreText =  WriteText(self.screen, 35, 'Player Score: N/A', (255,255,255), (106,84,78), 5, self.screenHeight - 115)
        self.DealerScoreText =  WriteText(self.screen, 35, 'Dealer Score: N/A', (255,255,255), (106,84,78), 5, self.screenHeight - 55)
        self.startText = WriteText(self.screen,50,'Place A Bet To Begin', (255,255,255), (78, 106, 84), self.screenWidth // 2 - 200, self.screenHeight // 2 - 50)

        self.standButton = Button(self.screen, (90,90,90), 100, 150, self.screenWidth // 2 + 50, self.screenHeight - 190) # Create a button to stand
        self.standButton.write('Stand', 35, (255,255,255)) # call write to write text on the button

        self.hitButton = Button(self.screen, (90,90,90), 100, 150, self.screenWidth // 2 - 200, self.screenHeight - 190) # Create a button to hit
        self.hitButton.write('Hit', 35, (255,255,255)) # call write to write text on the button

        self.helpButton = Button(self.screen, (78, 106, 84), 60, 50, 0, 0)
        self.helpButton.write('?', 40, (255,255,255))

        self.confirmBetButton = Button(self.screen, (90,90,90), 100,150, self.screenWidth // 2 - 200, self.screenHeight - 350)
        self.confirmBetButton.write('Confirm', 35, (255,255,255))

        self.removeBetButton = Button(self.screen, (90,90,90), 100, 150, self.screenWidth // 2 + 50, self.screenHeight - 350)
        self.removeBetButton.write('Remove', 35, (255,255,255))

        self.updateInformation('start')

    def placeSingleBet(self): # Used to increase the current bet by $1
        if self.bettingActive and self.playerMoney - 1 >= 0: # Check if betting is True and the player has money
            self.currentBet += 1 # Increase bet by 1
            self.betList.append(1)
            self.playerMoney -= 1 # Decrease the playersMoney by 1
            self.updateInformation('money+bet') # Call updateInformation to display the new balance on the screen
        
    def placeFiveBet(self): # Used to increase the current bet by $5
        if self.bettingActive and self.playerMoney - 5 >= 0: # Check if betting is True and player has money
            self.currentBet += 5 # Increase bet by 5
            self.betList.append(5)
            self.playerMoney -= 5 # Decrease the playersMoney by 5
            self.updateInformation('money+bet') # Call updateInformation to dsiplay the new balance on the screen

    def placeTenBet(self): # Used to increase the current bet by $10
        if self.bettingActive and self.playerMoney - 10 >= 0: # Check if betting is True and player has money
            self.currentBet += 10 # Increase bet by 10
            self.betList.append(10)
            self.playerMoney -= 10 # Decrease the playersMoney by 10
            self.updateInformation('money+bet') # Call updateInformation to display the new balance on the screen

    def placeTwentyFiveBet(self): # Used to increase the current bet by $25
        if self.bettingActive and self.playerMoney - 25 >= 0: # Check if betting is True and player has money
            self.currentBet += 25 # Increase bet by 25
            self.betList.append(25)
            self.playerMoney -= 25 # Decrease the playersMoney by 25
            self.updateInformation('money+bet') # Call updateInformation to display the new balance on the screen
    
    def removeBet(self):
        if len(self.betList) > 0:
            removed = self.betList.pop()
            self.playerMoney += removed
            self.currentBet -= removed
            self.updateInformation('money-bet')
    
    def updateInformation(self, information):

        match(information):
            case 'money+bet':
                self.playerMoneyText.update(f'Money: ${self.playerMoney}')
                self.startText.update(f'Current Bet: ${self.currentBet}', 90)
                self.playerBetText.update(f'Player Bet: ${self.currentBet}')
            case 'money-bet':
                self.playerMoneyText.update(f'Money: ${self.playerMoney}')
                self.playerBetText.update(f'Player Bet: ${self.currentBet}')
                if self.currentBet > 0:
                     self.startText.update(f'Current Bet: ${self.currentBet}', 90)
                else:
                     self.startText.update(f'Place A Bet To Begin', 90)

    def toggleHelp(self):
        self.open = not self.open

        if self.open:
            self.helpRectangle = game.Rect(self.screenWidth // 4, 0 + self.screenHeight // 5, self.screenWidth // 2, self.screenHeight // 2)
            game.draw.rect(self.screen, (255,255,255), self.helpRectangle)
            # self.exitHelpButton = Button(self.screen, (255,255,255), 30, 50, self.screenWidth // 4 + self.screenWidth // 2 - 50, self.screenHeight // 5 )
            # self.exitHelpButton.write('X', 20, (230,24,10))
            textList = ['Card Values: Face cards (jacks, queens, and kings) are worth 10, aces are worth 1 or 11. Other cards are worth their face value.', 'Dealing: The dealer gives the player two cards face up, and then receives two cards of their own one face up one face down.',
                        'Dealer Hold: Dealer hits if score is less than or equal to 16. Dealer holds at score higher than 17.','Play: Players can choose to hit (take another card) or stand (stay with their current hand).', 'Busting: If the players, or dealers, hand goes over 21 they bust (lose)',
                        'Win: Players win if their hand is closer to 21 than the dealer, or if the dealer busts.', 'Tie: If the dealer and player have the same value it is a tie.', 'Blackjack: Black jack occurs when the first two cards equal 21', 'Score: A regular win returns 2 to 1, a blackjack win returns 2.5 to 1' ]
            height =  self.screenHeight // 5
            for text in textList:
                height +=  50
                WriteText(self.screen, 14, text, (0,0,0), (255,255,255), self.screenWidth // 4 + 2, height)
        else:
            rectangle = game.Rect(0,100, self.screenWidth, self.screenHeight - 300)
            game.draw.rect(self.screen, (78, 106, 84), rectangle)



