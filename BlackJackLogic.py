import pygame as game
import random, os
from Components import WriteText, Button

class BlackJack:
    #____________________ Initializing Function _________________________________________

    def __init__(self, screen, screenHeight, screenWidth, playerMoney): # Function to initialize the blackjack class
        self.screen = screen # Used to populate screen with buttons, text, cards, chips
        self.screenHeight = screenHeight # Used to get the height of the game screen
        self.screenWidth = screenWidth # Used to get the width of the game screen
        self.playerMoney = playerMoney # Used to keep track of how much money the player has 
        self.betList = [] # Used to keep track of which bets were clicked (1,5,10,25) for removing bets
        self.bettingActive = True # Used to keep track if the player is allowed to place a bet
        self.currentBet = 0 # Used to keep track of the current bet
        self.open = False # Used to keep track if the help menu is open
        self.deck = {} # Used to create the deck of cards
        self.playerTurn = False
        self.playerCardList = []
        self.playerScore = 0
        self.dealerCardList = []
        self.dealerScore = 0
        self.playerAceCount = 0
        self.dealerAceCount = 0
        self.winner = None
        self.initial = True
        self.reset = False
        self.flipped = False
        self.secondDealerCard = None
        self.start = True

        self.initializeScreen() # Call initialize screen to display the user interface
    
    # __________________ Functions To Display Information And Visuals On Screen ____________
    
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

        self.playerMoneyText = WriteText(self.screen, 35, f'Money: ${self.playerMoney}', (255,255,255), (106,84,78), self.screenWidth - 350, self.screenHeight - 75) # Display the amount of money the player has on the screen
        self.playerBetText = WriteText(self.screen, 35, 'Player Bet: 0', (255,255,255), (106,84,78), 5, self.screenHeight - 175) # Display how much the player is betting for the round on the screen
        self.playerScoreText =  WriteText(self.screen, 35, 'Player Score: N/A', (255,255,255), (106,84,78), 5, self.screenHeight - 115) # Display the current score of the players cards
        self.DealerScoreText =  WriteText(self.screen, 35, 'Dealer Score: N/A', (255,255,255), (106,84,78), 5, self.screenHeight - 55) # Display the current score of the dealers cards
        self.startText = WriteText(self.screen,50,'Place A Bet To Begin', (255,255,255), (78, 106, 84), self.screenWidth // 2 - 200, self.screenHeight // 2 - 150) # Display the starting text to the player

        self.standButton = Button(self.screen, (90,90,90), 100, 150, self.screenWidth // 2 + 50, self.screenHeight - 190) # Create a button to stand
        self.standButton.write('Stand', 35, (255,255,255)) # Call write to write text on the button

        self.hitButton = Button(self.screen, (90,90,90), 100, 150, self.screenWidth // 2 - 200, self.screenHeight - 190) # Create a button to hit
        self.hitButton.write('Hit', 35, (255,255,255)) # Call write to write text on the button

        self.helpButton = Button(self.screen, (78, 106, 84), 60, 50, 0, 0) # Create a button to act as the help button
        self.helpButton.write('?', 40, (255,255,255)) # Call write to write text on the button

        self.confirmBetButton = Button(self.screen, (90,90,90), 100,150, self.screenWidth // 2 - 200, self.screenHeight - 350) # Create a button to act as the confirm bet button
        self.confirmBetButton.write('Confirm', 35, (255,255,255)) # Call write to write text on the button

        self.removeBetButton = Button(self.screen, (90,90,90), 100, 150, self.screenWidth // 2 + 50, self.screenHeight - 350) # Create a button to act as the remove bet button
        self.removeBetButton.write('Remove', 35, (255,255,255)) # Call write to write text on the button

        self.initializeCardDeck() # Call initializeCardDeck to initialize the deck of cards used in the game
    
    def placeChips(self, numberOfTwentyFiveChips, numberOfTenChips, numberOfFiveChips, numberOfOneChips): # Used to place the chips on the screen
        xPosition = self.screenWidth // 2 - 100 # Initialize the starting X position of the chips
        yPosition = self.screenHeight - 300 # Initialize the starting Y position of the chips
        rectangle = game.Rect(0,100, self.screenWidth, self.screenHeight - 300) # Create a rectangle to go over the buttons for confirming and placing the bet, and the starting text
        game.draw.rect(self.screen, (78, 106, 84), rectangle) # Draw the rectangle to the screen
        for _ in range(numberOfTwentyFiveChips): # Loop through the number of 25 chips
            xPosition += 15 # Increase the xPosition variable by 15
            self.screen.blit(self.chip25, (xPosition, yPosition)) # Place the 25 chip on the screen
        for _ in range(numberOfTenChips): # Loop through the number of 10 chips
            xPosition += 15 # Increase the xPosition variable by 15
            self.screen.blit(self.chip10, (xPosition, yPosition)) # Place the 10 chip on the screen
        for _ in range(numberOfFiveChips): # Loop through the number of 5 chips
            xPosition += 15 # Increase the xPosition variable by 15
            self.screen.blit(self.chip5, (xPosition, yPosition)) # Place the 5 chip on the screen
        for _ in range(numberOfOneChips): # Loop through the number of 1 chips
            xPosition += 15 # Increase the xPosition variable by 15
            self.screen.blit(self.chip1, (xPosition, yPosition)) # Place the 1 chip on the screen

    def updateInformation(self, information): # Used to update the information on the screen
        match(information): # Get the type of information to know what to update
            case 'money+bet': # If the case is 'money+bet'
                self.playerMoneyText.update(f'Money: ${self.playerMoney}') # Call the update function to update the playerMoneyText
                self.startText.update(f'Current Bet: ${self.currentBet}', 90) # Call the update function to update the startText
                self.playerBetText.update(f'Player Bet: ${self.currentBet}', 15) # Call the update function to update the playerBetText
            case 'money-bet':
                self.playerMoneyText.update(f'Money: ${self.playerMoney}', 15) # Call the update function to update the playerMoneyText
                self.playerBetText.update(f'Player Bet: ${self.currentBet}', 15) # Call the update function to update the playerBetText
                if self.currentBet > 0: # Check if the current bet is higher than 0
                     self.startText.update(f'Current Bet: ${self.currentBet}', 90) # Call the update function to update the startText
                else:
                     self.startText.update(f'Place A Bet To Begin', 90) # Call the update function to update the startText
            case 'player':
                print('updating player score')
                self.playerScoreText.update(f'Player Score: {self.playerScore}', 25)
            case 'dealer':
                print('updating dealer score')
                self.DealerScoreText.update(f'Dealer Score: {self.dealerScore}', 25)
            case 'reset':
                self.playerScoreText.update('Player Score: N/A', 25)
                self.DealerScoreText.update('Dealer Score: N/A', 25)
                self.playerBetText.update('Current Bet: $0', 90)
            case 'money':
                self.playerMoneyText.update(f'Money: ${self.playerMoney}', 15)


    def toggleHelp(self): # Used to /toggle the help screen
        self.open = not self.open # Change the self.open variable to its opposite (True to False, False to True)
        if self.open: # If open is true
            self.helpRectangle = game.Rect(self.screenWidth // 4, 0 + self.screenHeight // 5, self.screenWidth // 2, self.screenHeight // 2) # Create the rectangle for the help screen
            game.draw.rect(self.screen, (255,255,255), self.helpRectangle) # Place the rectangle on the screen
            textList = ['Card Values: Face cards (jacks, queens, and kings) are worth 10, aces are worth 1 or 11. Other cards are worth their face value.', 'Dealing: The dealer gives the player two cards face up, and then receives two cards of their own one face up one face down.',
                        'Dealer Stay: Dealer hits if score is less than or equal to 16. Dealer holds at score higher than 17.','Play: Players can choose to hit (take another card) or stay (stay with their current hand).', 'Busting: If the players, or dealers, hand goes over 21 they bust (lose)',
                        'Win: Players win if their hand is closer to 21 than the dealer, or if the dealer busts.', 'Tie: If the dealer and player have the same value it is a tie.', 'Blackjack: Black jack occurs when the first two cards equal 21', 'Score: A regular win returns 2 to 1, a blackjack win returns 2.5 to 1' ]
            height =  self.screenHeight // 5 # Initialize height, used to control the y axis of the text
            for text in textList: # Loop through the textlist
                height +=  50 # Increase the height by 50
                WriteText(self.screen, 14, text, (0,0,0), (255,255,255), self.screenWidth // 4 + 2, height) # Place the text on the screen
        else:
            rectangle = game.Rect(0,100, self.screenWidth, self.screenHeight - 300) # Create a rectangle to cover the help screen
            game.draw.rect(self.screen, (78, 106, 84), rectangle) # Draw the rectangle on the screen
            self.replaceItemsOnScreen() # Call replaceItemsOnScreen 


    def replaceItemsOnScreen(self): # Used to replace the items that were on the screen before the help button was pressed
        if self.bettingActive: # Check if betting is active
            self.confirmBetButton = Button(self.screen, (90,90,90), 100,150, self.screenWidth // 2 - 200, self.screenHeight - 350) # Create a button to act as the confirm bet button
            self.confirmBetButton.write('Confirm', 35, (255,255,255)) # Call write to write text on the button

            self.removeBetButton = Button(self.screen, (90,90,90), 100, 150, self.screenWidth // 2 + 50, self.screenHeight - 350) # Create a button to act as the remove bet button
            self.removeBetButton.write('Remove', 35, (255,255,255)) # Call write to write text on the button
            if self.currentBet > 0: # Check if the current bet is greater than 0
                self.startText.update(f'Current Bet: ${self.currentBet}', 90) # Call the update function to update the startText
            else:
                self.startText.update(f'Place A Bet To Begin', 90) # Call the update function to update the startText
        elif not self.bettingActive: # Check if betting is not active

            self.placeChips(self.numberOfTwentyFiveChips, self.numberOfTenChips, self.numberOfFiveChips, self.numberOfOneChips) # Place the chips on the screen again

            numberOfCards = 0
            for card in self.playerCardList:
                xPosition = self.screenWidth // 2 - 100 + (50 * numberOfCards)
                yPosition = self.screenHeight - 500
                self.placeCard(card, xPosition, yPosition)
                numberOfCards += 1

            numberOfCards = 0
            for card in self.dealerCardList:
                xPosition = self.screenWidth // 2 - 100 + (50 * numberOfCards)
                yPosition = 100
                self.placeCard(card, xPosition, yPosition)
                numberOfCards += 1
            
            if self.winner:
                self.displayWinner()

    # __________________ Functions For Game Logic ____________________________________________

    def initializeCardDeck(self): # Used to intialize the deck of cards
        index = -1 # Initialize index to place into the hashmap
        for filename in os.listdir('./BlackJackAssets'): # Loop through each file in the BlackJackAssets folder
            index += 1 # Increase the index by 11
            cardPath = f'./BlackJackAssets/{filename}' # Get the card path 
            card = game.image.load(cardPath) # Load the card
            match filename[0]: # Check the first letter in the filename in O(1) time
                case 'A': # Check if first letter is A, if so then the card is an Ace
                    val = [11,1] # Give the val variable its two values (1 or 11)
                case '2': # Check if the first letter is 2
                    val = [2] # Give the val variable the value of 2
                case '3': # Check if the first letter is 3
                    val = [3] # Give the val variable the value of 3
                case '4': # Check if the first letter is 4
                    val = [4] # Give the val variable the value of 4
                case '5': # Check if the first letter is 5
                    val = [5] # Give the val variable the value of 5
                case '6': # Check if the first letter is 6
                    val = [6] # Give the val variable the value of 6
                case '7': # Check if the first letter is 7
                    val = [7] # Give the val variable the value of 7
                case '8': # Check if the first letter is 8
                    val = [8] # Give the val variable the value of 8
                case '9': # Check if the first letter is 9
                    val = [9] # Give the val variable the value of 9
                case '1': # Check if the first letter is 1
                    val = [10] # Give the val variable the value of 10
                case 'j': # Check if the first letter is j
                    val = [10] # Give the val variable the value of 10
                case 'k': # Check if the first letter is k
                    val = [10] # Give the val variable the value of 10
                case 'q': # Check if the first letter is q
                    val = [10] # Give the val variable the value of 10
                case _: # Default case
                    index -= 1
                    val = []
            
            if len(val) > 0:
                card = game.transform.scale(card,(170,220))
                self.deck[index] = (card,val) # Add the card value pair to the deck

    def placeSingleBet(self): # Used to increase the current bet by $1
        if self.bettingActive and self.playerMoney - 1 >= 0: # Check if betting is True and the player has money
            if self.initial:
                self.resetScreen()
                self.initial = False
                self.reset = False
                self.updateInformation('reset')

            self.currentBet += 1 # Increase bet by 1
            self.betList.append(1) # Add 1 to the list of bets (used if wanting to remove a bet)
            self.playerMoney -= 1 # Decrease the playersMoney by 1
            self.updateInformation('money+bet') # Call updateInformation to display the new balance on the screen
        
    def placeFiveBet(self): # Used to increase the current bet by $5
        if self.bettingActive and self.playerMoney - 5 >= 0: # Check if betting is True and player has money
            if self.initial:
                self.resetScreen()
                self.initial = False
                self.reset = False
                self.updateInformation('reset')

            self.currentBet += 5 # Increase bet by 5
            self.betList.append(5) # Add 5 to the list of bets (used if wanting to remove a bet)
            self.playerMoney -= 5 # Decrease the playersMoney by 5
            self.updateInformation('money+bet') # Call updateInformation to dsiplay the new balance on the screen

    def placeTenBet(self): # Used to increase the current bet by $10
        if self.bettingActive and self.playerMoney - 10 >= 0: # Check if betting is True and player has money
            if self.initial:
                self.resetScreen()
                self.initial = False
                self.reset = False
                self.updateInformation('reset')

            self.currentBet += 10 # Increase bet by 10
            self.betList.append(10) # Add 10 to the list of bets (used if wanting to remove a bet)
            self.playerMoney -= 10 # Decrease the playersMoney by 10
            self.updateInformation('money+bet') # Call updateInformation to display the new balance on the screen

    def placeTwentyFiveBet(self): # Used to increase the current bet by $25
        if self.bettingActive and self.playerMoney - 25 >= 0: # Check if betting is True and player has money
            if self.initial:
                self.resetScreen()
                self.initial = False
                self.reset = False
                self.updateInformation('reset')

            self.currentBet += 25 # Increase bet by 25
            self.betList.append(25) # Add 15 to the list of bets (used if wanting to remove a bet)
            self.playerMoney -= 25 # Decrease the playersMoney by 25
            self.updateInformation('money+bet') # Call updateInformation to display the new balance on the screen
    
    def removeBet(self): # Used to remove the last bet
        if len(self.betList) > 0 and self.bettingActive: # Check if betting is active and if there are bets in the bet list
            removed = self.betList.pop() # Remove the last bet
            self.playerMoney += removed # Give the player back the bet
            self.currentBet -= removed # Remove the bet amount from the currentBet
            self.updateInformation('money-bet') # Call updateInformation to display the new bet and player money amounts on screen

    
    def confirmBet(self): # Used to confirm the bet
        if self.currentBet > 0: # Check to make sure the current bet is greater than -
            self.bettingActive = False # Turn betting off
            self.playerTurn = True
            self.numberOfTwentyFiveChips = self.getChipAmount(25, self.currentBet) # Get the number of 25 chips by calling getChipAmount
            self.numberOfTenChips = self.getChipAmount(10, self.currentBet - (self.numberOfTwentyFiveChips * 25)) # Get the number of Ten Chips by calling getChipAmount
            self.numberOfFiveChips = self.getChipAmount(5, self.currentBet - (self.numberOfTwentyFiveChips * 25 + self.numberOfTenChips * 10)) # Get the number of Five Chips by calling getChipAmount
            self.numberOfOneChips = self.getChipAmount(1, self.currentBet - (self.numberOfTwentyFiveChips * 25 + self.numberOfTenChips * 10 + self.numberOfFiveChips * 5)) # Get the number of 1 chips by calling getChipAmount
            self.placeChips(self.numberOfTwentyFiveChips, self.numberOfTenChips, self.numberOfFiveChips, self.numberOfOneChips) # Send the values to the placeChips function
            self.startGame()
            # print('25', self.numberOfTwentyFiveChips)
            # print('10', self.numberOfTenChips)
            # print('5', self.numberOfFiveChips)
            # print('1', self.numberOfOneChips)
        else:
            self.startText.update('Bet Cannot Be Zero', 45) # Display Bet Cannot Be Zero on screen if the player has not placed a bet

    def getChipAmount(self, chipType, bet): # Used to determine how many of each chip
        temp = bet % chipType # See the remained if using modulo chip value on the current bet 
        tempBet = bet - temp # Subtract the bet by the modula remainder to make sure the remaining number goes equally into the amount of chips
        amount = tempBet // chipType # Floor divide the temp bet by the chip value
        return amount # Return the amount of that particular chip

    def chooseCard(self): # Used to choose a random card
        index = random.randint(0, len(self.deck) - 1) # Use random.randint to get a random integer from 0 to the length of the deck (inclusive)
        card = self.deck[index] # Get the card at the specified key
        return card # Return the card

    def addCard(self,player): # Used to add a card
        card = self.chooseCard()
        if player:
            print(f'Player score before adding card {self.playerScore}')
            print(f'Adding card with value {card[1]} to player')
            xPosition = self.screenWidth // 2 - 100 + (50 * len(self.playerCardList))
            yPosition = self.screenHeight - 500
            self.playerCardList.append(card[0])
            self.placeCard(card[0], xPosition, yPosition)
            self.playerScore = self.increaseScore(card[1], self.playerScore, True)
            self.playerScore, self.playerAceCount = self.checkScore(self.playerScore, self.playerAceCount, True)
            print(f'Player score after adding value {self.playerScore}')
            self.updateInformation('player')
            self.checkGame(self.playerScore, True)
        else:
            print(f'Dealer score before adding card {self.dealerScore}')
            print(f'Adding card with value {card[1]} to Dealer')
            xPosition = self.screenWidth // 2 - 100 + (50 * len(self.dealerCardList))
            yPosition = 100
            self.dealerCardList.append(card[0])
            self.placeCard(card[0], xPosition, yPosition)
            self.dealerScore = self.increaseScore(card[1], self.dealerScore, False)
            self.dealerScore, self.dealerAceCount = self.checkScore(self.dealerScore, self.dealerAceCount, False)
            print(f'Dealer score after adding value {self.dealerScore}')
            self.updateInformation('dealer')
            self.checkGame(self.dealerScore, False)
            
    def increaseScore(self,value, currentScore, player): # Used to increase the player of dealers score based on the cards score
        print(f'Inside increase score, the value being added is {value}')
        if len(value) > 1: # Check if the card is an ace
           currentScore = self.addAce(currentScore, value, player)
        else:
            currentScore += value[0]
        return currentScore

    def addAce(self,currentScore,value, player): # Used to determine the value of an ace
        if value[0] + currentScore > 21: # Check if the ace being 11 causes the score to go over 21
            currentScore += value[1] # Make the aces value 1
        else:
            currentScore += value[0] # Make the aces value 11
            if player: # Check if it is the player
                self.playerAceCount += 1 # Increase the player ace count by 1
            else:
                self.dealerAceCount += 1 # Increase the dealers ace count by 1
        return currentScore

    def placeCard(self, card, xPosition, yPosition):
        self.screen.blit(card,(xPosition, yPosition))

    def checkScore(self,score,aces, player = False):
        if score > 21 and aces:
            score -= 10
            aces -= 1
        return score, aces
    
    def checkGame(self,score,player = False):
        print('Inside Check Game with score:', score, player)
        if not self.start:
            if (score == 21 and player):
                self.checkWinner() 
            elif (score > 21 and player):
                self.checkWinner()
            elif score >= 21 or score == 21:
                self.checkWinner()

    def handleHitButton(self):
        if self.bettingActive == False and self.playerScore < 21 and self.playerTurn:
            self.addCard(True)
    
    def startGame(self):
        print('Starting Game')
        self.start = True
        for turn in range(3):
            if turn % 2 == 0:
                self.addCard(True)
            else:
                self.addCard(False)
        self.start = False
        self.addDealerSecondCard()
        self.checkGame(self.playerScore, True)
        self.checkGame(self.dealerScore, False)
    
    def flip(self):
        if self.secondDealerCard and len(self.dealerCardList) > 1:
            print(f'Inside flip, the length of the cards list is {len(self.dealerCardList)}')
            xPosition = self.screenWidth // 2 - 100 + 50 
            yPosition = 100
            self.flipped = True
            self.dealerCardList[1] = self.secondDealerCard
            self.placeCard(self.secondDealerCard, xPosition, yPosition)
            self.updateInformation('dealer')

    def addDealerSecondCard(self):
        print('Adding second dealer card')
        card = self.chooseCard()
        self.secondDealerCard = card[0]
        self.dealerScore = self.increaseScore(card[1], self.dealerScore, False)
        cardBack = game.image.load('./BlackJackAssets/back.svg')
        cardBack = game.transform.scale(cardBack, (170,220))
        self.dealerCardList.append(cardBack)
        xPosition = self.screenWidth // 2 - 100 + 50 
        yPosition = 100
        self.placeCard(cardBack, xPosition, yPosition)
    
    def handleStayButton(self):
        print(f'Insinde handStayButton the length of dealer list is{len(self.dealerCardList)}')
        if self.bettingActive == False and self.playerTurn == True:
            self.stay()
    
    def stay(self):
        self.playerTurn == False
        self.flip()
        while self.dealerScore < 17 and self.bettingActive == False:
            self.addCard(False)
        if self.winner == None:
            self.checkWinner()
    
    def checkWinner(self):
        
        if self.reset == False:
            if self.flipped == False:
                self.flip()

            print(self.playerScore, self.dealerScore)
            self.playerTurn = False
            if self.playerScore > 21 and self.dealerScore <= 21:
                self.winner = 'D'
            elif self.dealerScore > 21 and self.playerScore <= 21:
                self.winner = 'P'
            elif (self.playerScore == self.dealerScore):
                self.winner = 'T'
            elif (self.playerScore == 21 and len(self.playerCardList) == 2):
                self.winner = 'PBJ'
            elif (self.dealerScore == 21 and len(self.dealerCardList) == 2):
                self.winner = 'DBJ'
            elif self.playerScore > self.dealerScore and self.playerScore <= 21:
                self.winner = 'P'
            elif self.dealerScore > self.playerScore and self.dealerScore <= 21:
                self.winner = 'D'
            elif self.dealerScore > 21 and self.playerScore > 21:
                self.winner = 'N'

            self.displayWinner()
    
    def displayWinner(self):
        match self.winner:
            case 'D':
                self.startText.update('Dealer Won, place another bet to restart', 30,100)
            case 'P':
                self.startText.update('Player Won, place another bet to restart', 30, 100)
                self.playerMoney += self.currentBet * 2
            case 'T':
                self.startText.update('Tie, place another bet to restart', 30, 100)
                self.playerMoney += self.currentBet
            case 'PBJ':
                self.startText.update('Player won (BlackJack), place another bet to restart', 30, 300)
                self.playerMoney += self.currentBet * 2.5
            case 'DBJ':
                self.startText.update('Dealer Won (BlackJack), place another bet to restart', 30, 300)
            case 'N':
                self.startText.update('Both player and dealer over 21, no one wins', 30, 300)
        
        print(self.winner)
        if self.winner:
            self.resetGameLogic()
        

    def resetGameLogic(self):
        print('Resetting logic')
        self.updateInformation('money')
        self.bettingActive = True
        self.playerScore = 0
        self.playerAceCount = 0
        self.playerCardList = []
        self.dealerScore = 0
        self.dealerAceCount = 0
        self.dealerCardList = []
        self.currentBet = 0
        self.initial = True
        self.reset = True
        self.betList = []
        self.winner = None
        self.flipped = False
        print(f'Player score is now {self.playerScore}')
        print(f'Dealer score is now {self.dealerScore}')
        print('______________________________________________________')

    def resetScreen(self):
        rectangle = game.Rect(0,100, self.screenWidth, self.screenHeight - 300) # Create a rectangle to go over the buttons for confirming and placing the bet, and the starting text
        game.draw.rect(self.screen, (78, 106, 84), rectangle) # Draw the rectangle to the screen

        self.replaceItemsOnScreen()
    
    # def reDrawButtons(self):
    #     self.standButton = Button(self.screen, (90,90,90), 100, 150, self.screenWidth // 2 + 50, self.screenHeight - 190) # Create a button to stand
    #     self.standButton.write('Stand', 35, (255,255,255)) # Call write to write text on the button

    #     self.hitButton = Button(self.screen, (90,90,90), 100, 150, self.screenWidth // 2 - 200, self.screenHeight - 190) # Create a button to hit
    #     self.hitButton.write('Hit', 35, (255,255,255)) # Call write to write text on the button

    #     self.helpButton = Button(self.screen, (78, 106, 84), 60, 50, 0, 0) # Create a button to act as the help button
    #     self.helpButton.write('?', 40, (255,255,255)) # Call write to write text on the button