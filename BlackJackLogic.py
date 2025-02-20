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
        self.playerTurn = False # Used to control what actions the player can do
        self.playerCardList = [] # Used to keep track of the cards the player has gotten
        self.playerScore = 0 # Used to keep track of the players score
        self.dealerCardList = [] # Used to keep track of the cards the dealer has gotten
        self.dealerScore = 0 # Used to keep track of the dealers score
        self.playerAceCount = 0 # Used to keep track of the number of aces the player has gotten
        self.dealerAceCount = 0 # Used to keep track of the number of aces the dealer has gotten
        self.winner = None # Used to keep track of who won the game
        self.initial = True # Used to keep track if it is the initial bet (Used for placing items on screen)
        self.reset = False # Used to keep track if the game has been reset
        self.flipped = False # Used to keep track if the second dealer card has been shown
        self.secondDealerCard = None # Used to hold the second dealer card which is not shown at the start of the game
        self.start = True # Used to keep track if the cards being given are part of the initial 4
        self.seenCards = set() # Used to keep track of what cards have been seen 
        self.seenCards.add(1000)
        self.animationDone = True # Used to keep track if the card animation has finished
        self.animatePlayerCard = False # Used to keep track if card is being animated for the player or the dealer
        self.animationX = 200 # Used to keep track of the x coordiante for the animations
        self.animationY = 200 # Used to keep track of the y coordinate for the animations
        self.cardBeingAnimated = None # Used to keep track of which card is being animated
        self.xStartingPoint = self.screenWidth // 2 - 103 # Used by main.py to determine the speed of the animation
        self.animateDealerCard = False # Used to determine if card is animated to dealer or player
        self.secondDealerCardAnimation = False # Used to keep track if the dealers second card, the one you cannot see, has been animated
        self.startingTurn = 0 # Used to keep track of the starting turn, used for the 4 initial moves each game
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

        self.placeDeckImage() # Call placeDecckImage to place the image of the deck
        self.initializeCardDeck() # Call initializeCardDeck to initialize the deck of cards used in the game
    
    def placeChips(self, numberOfTwentyFiveChips, numberOfTenChips, numberOfFiveChips, numberOfOneChips): # Used to place the chips on the screen
        xPosition = self.screenWidth // 2 - 100 # Initialize the starting X position of the chips
        yPosition = self.screenHeight - 300 # Initialize the starting Y position of the chips
        rectangle = game.Rect(0,80, self.screenWidth, self.screenHeight - 300) # Create a rectangle to go over the buttons for confirming and placing the bet, and the starting text
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
            case 'money+bet': 
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
                self.playerScoreText.update(f'Player Score: {self.playerScore}', 25) # Call the update function to update the playerScoreText
            case 'dealer':
                print('updating dealer score')
                self.DealerScoreText.update(f'Dealer Score: {self.dealerScore}', 25) # Call the update function to update the dealerScoreText
            case 'reset':
                self.playerScoreText.update('Player Score: N/A', 25) # Call the update function to update the playerScoreText
                self.DealerScoreText.update('Dealer Score: N/A', 25) # Call the update function to update the dealerScoreText
                self.playerBetText.update('Current Bet: $0', 90) # Call the update function to update the playerBetText
            case 'money':
                self.playerMoneyText.update(f'Money: ${self.playerMoney}', 15) # Call the update function to update the playerMoneyText

    def toggleHelp(self): # Used to toggle the help screen
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

            numberOfCards = 0 # Initialize numberOfCards with a value of 0 (used to determine the x placement of the card)
            for card in self.playerCardList: # Loop through each card that the player has gotten
                xPosition = self.screenWidth // 2 - 100 + (50 * numberOfCards) # Modify the x position based on the number of cards already on the screen for the player
                yPosition = self.screenHeight - 500 # Initialize the Y position
                self.placeCard(card, xPosition, yPosition) # Call place card to place the card on the screen
                numberOfCards += 1 # Increase the number of cards by 1

            numberOfCards = 0 # Reset number of cards to 0
            for card in self.dealerCardList: # Loop through each card that the dealer has gotten
                xPosition = self.screenWidth // 2 - 100 + (50 * numberOfCards) # Modify the x position based on the number of cards already on the screen for the dealer
                yPosition = 100 # Initialize the Y position
                self.placeCard(card, xPosition, yPosition) # Call place cards to palce the card on the screen
                numberOfCards += 1 # Increase the number of cards by 1
            
            if self.winner: # Check if htere is a winner
                self.displayWinner() # Display the winner

        self.placeDeckImage() # Call placeDeckImage to replace the image of the deck

    def placeCard(self, card, xPosition, yPosition): # Function used to place a card on the screen
        self.screen.blit(card,(xPosition, yPosition)) # Place the card on the screen

    def flip(self): # Used to flip the card facing the wrong direction once the dealers turn occurs
        if self.secondDealerCard and len(self.dealerCardList) > 1:
            self.replaceItemsOnScreen()
            print(f'Inside flip, the length of the cards list is {len(self.dealerCardList)}')
            xPosition = self.screenWidth // 2 - 103 + 50  # Initialize the X position of the flipped card
            yPosition = 100 # Initialize the y position of the  flipped card
            self.flipped = True # Set self.flipped to true, signaling the card has already been flipped
            self.dealerCardList[1] = self.secondDealerCard[0] # Change the card in the array from the back svg to the actual card svg
            self.placeCard(self.secondDealerCard[0], xPosition, yPosition) # Call placeCard to place the card
            self.updateInformation('dealer') # Call updateInformation with dealer as a paramater to update the dealers score
    
    def displayWinner(self): # Used to display who won the game
        match self.winner: # Match the winner based on the case in O(1) time
            case 'D': # If dealer won
                self.startText.update('Dealer Won, place another bet to restart', 30,100) # Call update on startText to inform the player that the dealer has won
            case 'P':
                self.startText.update('Player Won, place another bet to restart', 30, 100) # Call update on startText to inform the player that the player has won
                self.playerMoney += self.currentBet * 2 # Increase the players money by the bet * 2 (Winning normally pays 2 to 1)
            case 'T':
                self.startText.update('Tie, place another bet to restart', 30, 100) # Call update on startText to inform the player that it was a tie
                self.playerMoney += self.currentBet # Return the bet as it was a tie
            case 'PBJ':
                self.startText.update('Player won (BlackJack), place another bet to restart', 30, 300) # Call update on startText to inform the player they won with blackjack
                self.playerMoney += self.currentBet * 2.5 # Increase the player money by 2.5 as blackjack pays 3 to 2.
            case 'DBJ':
                self.startText.update('Dealer Won (BlackJack), place another bet to restart', 30, 300) # Call update on startText to inform the player that the dealer has won with blackjack
            case '_':
                self.startText.update('Error please send log to developer', 30, 300) # Used for internal testing
        
        print(self.winner)
        if self.winner: # Check if the winner is not None
            self.resetGameLogic() # Reset the game logic 
    
    def resetScreen(self): # Used to reset the screen
        rectangle = game.Rect(0,100, self.screenWidth, self.screenHeight - 300) # Create a rectangle to go over the buttons for confirming and placing the bet, and the starting text
        game.draw.rect(self.screen, (78, 106, 84), rectangle) # Draw the rectangle to the screen

        self.replaceItemsOnScreen() # call replaceItemsOnScreen to redraw the game onto the screen
    
    def placeDeckImage(self): # Used to place the image of the deck
        cardDeck = game.image.load('./BlackJackAssets/deck.svg') # Loads the image
        self.screen.blit(cardDeck, (200, 200)) # Places the image on the screen

    def animateCard(self, card, x, y, player): # Used to animate the card
        self.replaceItemsOnScreen() # Call replaceItemsOnScreen to re draw everything to the screen, prevents screen tearing from the animation
        if self.secondDealerCardAnimation == False: # Check if the card being animated is the second dealer card
            self.placeCard(card[0], x, y) # Call place card and place the second dealer card
        else:
            self.placeCard(card,x,y) # Call place card and place the ard
        if player: # Check if the card is for the player
            if x >= self.screenWidth // 2 - 103 + (50 * len(self.playerCardList)) or y >= self.screenHeight - 530: # Check if the x and y coordinates are below a certain criteria
                self.replaceItemsOnScreen() # Call replaceItemsOnScreen to re draw everything to the screen, prevents screen tearing from the animation
                self.animationDone = True # Set the animationDone variable to true, indicating the animation has ended
                self.animatePlayerCard = False # Set animatePlayerCard to false
                self.placeCard(card[0], self.screenWidth // 2 - 103 + (50 * len(self.playerCardList)), self.screenHeight - 500) # Place the card one last time in the correct location
                self.animationX = 200 # Reset the animationX to the starting position
                self.animationY = 200 # Reset the animationY to the starting position
                self.playerCardList.append(card[0]) # Append the card to the playerCardList
                self.playerScore = self.increaseScore(card[1], self.playerScore, True) # Call increaseScore to increase the score
                self.playerScore, self.playerAceCount = self.checkScore(self.playerScore, self.playerAceCount, True) # Call checkScore to check if there are any ace values that need to be changed from 11 to 1
                self.updateInformation('player') # Call updateInformation with the parameter player to update the players score
                self.checkGame(self.playerScore, True) # Call checkGame to check the current score
                if self.start: # Check if it is the start of the game
                    self.startingTurn += 1 # Increase starting turn by 1
                    self.startGame(self.startingTurn) # Call startGame with the updating startingTurn to do the next starting move
        else:
            if x >= self.screenWidth // 2 - 103 + (50 * len(self.dealerCardList)) and y <= 115: # Check if the x and y coordinated are within a certain criteria
                if self.secondDealerCardAnimation == True: # Check if the animation is for the secondDealerCard
                    self.dealerScore = self.increaseScore(self.secondDealerCard[1], self.dealerScore, False) # call increaseScore to increase the dealers score 
                    self.secondDealerCardAnimation = False # Set secondDealerCardAnimation to False to indicate the animation has ended
                    self.animateDealerCard = False # Set animateDealerCard to False to inidcate the dealercard is no longer being animated
                    self.animationDone = True # Set animationDone to true, indicating the animation has ended
                    self.animationX = 200 # Reset the animationX to the starting position
                    self.animationY = 200 # Reset the animationY to the starting position
                    self.dealerCardList.append(card) # Append the card to the dealerCardList
                    self.start = False # Change self.start to False, the 4 starting moves have finished
                    self.checkGame(self.playerScore) # Call checkGame with the playerScore to see if player has blackjack
                    self.checkGame(self.dealerScore) # Call checkGame with the dealerScore to see if the dealer has blackjack
                else:
                    self.replaceItemsOnScreen() # Call replaceItemsOnScreen to re draw everything to the screen, prevents screen tearing from the animation
                    self.animationDone = True # Set animationDone to True, indicating the animation has ended
                    self.animateDealerCard = False # Set animateDealerCard to False, Indicating the dealerCard is no longer being animated
                    self.placeCard(card[0], self.screenWidth // 2 - 103 + (50 * len(self.dealerCardList)), 100) # Call place card to place the card in its final position
                    self.animationX = 200 # Reset the animationX to the starting position
                    self.animationY = 200 # Reset the animationY to the starting position
                    self.dealerCardList.append(card[0]) # Append the card to the dealerCardList
                    self.dealerScore = self.increaseScore(card[1], self.dealerScore, False) # Call increaseScore to increase the score
                    self.dealerScore, self.dealerAceCount = self.checkScore(self.dealerScore, self.dealerAceCount, False) # Call checkScore to check if there are any ace values that need to be changed from 11 to 1
                    self.updateInformation('dealer') # Call updateInformation with the parameter dealer to update the dealers score
                    if self.start: # Check if self.start is True
                        self.startingTurn += 1 # increase startingTurn by 1
                        self.startGame(self.startingTurn) # Call startGame with the updating startingTurn to do the next starting move
                    elif self.playerTurn == False: # Check if the playerTurn is False
                        self.stay() # Call stay to give the dealer the next card
                
    # __________________ Functions For Game Logic ____________________________________________

    def initializeCardDeck(self): # Used to intialize the deck of cards
        index = -1 # Initialize index to place into the hashmap
        for _ in range(5):
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
                        index -= 1 # Reduce the index by 1 as there is nothing being added to the deck dictionary
                        val = [] # Set the value to an empty list
                    
                if len(val) > 0: # Check if the length of the value array is greater than 0
                    card = game.transform.scale(card,(170,220)) # scale the card to specified width and height
                    self.deck[index] = (card,val) # Add the card value pair to the deck
        print(len(self.deck))

    def placeSingleBet(self): # Used to increase the current bet by $1
        if self.bettingActive and self.playerMoney - 1 >= 0: # Check if betting is True and the player has money
            if self.initial: # Check if intial is set to true (used to change the screen to the bet screen)
                self.resetScreen() # Call resetScreen to reset the previous game that was on the screen
                self.initial = False # Set initial to false so that the game does not reset the screen again
                self.reset = False # Set self.reset to false to indicate that the game has not been reset again, it is a new game
                self.updateInformation('reset') # Call updateInformation with the parameter reset to reset all of the information displayed to indicate a new game

            self.currentBet += 1 # Increase bet by 1
            self.betList.append(1) # Add 1 to the list of bets (used if wanting to remove a bet)
            self.playerMoney -= 1 # Decrease the playersMoney by 1
            self.updateInformation('money+bet') # Call updateInformation to display the new balance on the screen
        
    def placeFiveBet(self): # Used to increase the current bet by $5
        if self.bettingActive and self.playerMoney - 5 >= 0: # Check if betting is True and player has money
            if self.initial: # Check if intial is set to true (used to change the screen to the bet screen)
                self.resetScreen() # Call resetScreen to reset the previous game that was on the screen
                self.initial = False # Set initial to false so that the game does not reset the screen again
                self.reset = False # Set self.reset to false to indicate that the game has not been reset again, it is a new game
                self.updateInformation('reset') # Call updateInformation with the parameter reset to reset all of the information displayed to indicate a new game

            self.currentBet += 5 # Increase bet by 5
            self.betList.append(5) # Add 5 to the list of bets (used if wanting to remove a bet)
            self.playerMoney -= 5 # Decrease the playersMoney by 5
            self.updateInformation('money+bet') # Call updateInformation to dsiplay the new balance on the screen

    def placeTenBet(self): # Used to increase the current bet by $10
        if self.bettingActive and self.playerMoney - 10 >= 0: # Check if betting is True and player has money
            if self.initial: # Check if intial is set to true (used to change the screen to the bet screen)
                self.resetScreen() # Call resetScreen to reset the previous game that was on the screen
                self.initial = False # Set initial to false so that the game does not reset the screen again
                self.reset = False # Set self.reset to false to indicate that the game has not been reset again, it is a new game
                self.updateInformation('reset') # Call updateInformation with the parameter reset to reset all of the information displayed to indicate a new game

            self.currentBet += 10 # Increase bet by 10
            self.betList.append(10) # Add 10 to the list of bets (used if wanting to remove a bet)
            self.playerMoney -= 10 # Decrease the playersMoney by 10
            self.updateInformation('money+bet') # Call updateInformation to display the new balance on the screen

    def placeTwentyFiveBet(self): # Used to increase the current bet by $25
        if self.bettingActive and self.playerMoney - 25 >= 0: # Check if betting is True and player has money
            if self.initial: # Check if intial is set to true (used to change the screen to the bet screen)
                self.resetScreen() # Call resetScreen to reset the previous game that was on the screen
                self.initial = False # Set initial to false so that the game does not reset the screen again
                self.reset = False # Set self.reset to false to indicate that the game has not been reset again, it is a new game
                self.updateInformation('reset') # Call updateInformation with the parameter reset to reset all of the information displayed to indicate a new game

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
            self.numberOfTwentyFiveChips = self.getChipAmount(25, self.currentBet) # Get the number of 25 chips by calling getChipAmount
            self.numberOfTenChips = self.getChipAmount(10, self.currentBet - (self.numberOfTwentyFiveChips * 25)) # Get the number of Ten Chips by calling getChipAmount
            self.numberOfFiveChips = self.getChipAmount(5, self.currentBet - (self.numberOfTwentyFiveChips * 25 + self.numberOfTenChips * 10)) # Get the number of Five Chips by calling getChipAmount
            self.numberOfOneChips = self.getChipAmount(1, self.currentBet - (self.numberOfTwentyFiveChips * 25 + self.numberOfTenChips * 10 + self.numberOfFiveChips * 5)) # Get the number of 1 chips by calling getChipAmount
            self.placeChips(self.numberOfTwentyFiveChips, self.numberOfTenChips, self.numberOfFiveChips, self.numberOfOneChips) # Send the values to the placeChips function
            self.start = True
            self.startGame(self.startingTurn) # Call start game to start the game and give the initial set of cards
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
        index = 1000 # Initialize index as 1000 (this number is specifically added to the set as it is not a valid index)
        while index in self.seenCards: # Get a random index until it has not been seen in the seenCards set
            index = random.randint(0, len(self.deck) - 1) # Use random.randint to get a random integer from 0 to the length of the deck (inclusive)
        self.seenCards.add(index) # Add the index to the set
        card = self.deck[index] # Get the card at the specified key
        return card # Return the card

    def addCard(self,player): # Used to add a card
        card = self.chooseCard() # Call chooseCard to get a random card
        print(f'Inside Add Card, Card for player: {player}, cards value {card[1]}')
        if player: # Check if the card is for the player
            print(f'Player score before adding card {self.playerScore}')
            print(f'Adding card with value {card[1]} to player')
            self.cardBeingAnimated = card # Set cardBeingAnimated to the card given
            self.animationDone = False # Set animationDone to False, used so the player cannot activate the hit and hold functionality while the card is being given
            self.animatePlayerCard = True # Set animatePlayerCard to True, used to determine where to send the card
        else:
            print(f'Dealer score before adding card {self.dealerScore}')
            print(f'Adding card with value {card[1]} to Dealer')
            self.cardBeingAnimated = card # Set cardBeingAnimated to the card given
            self.animationDone = False # Set animationDone to False, used so the player cannot activate the hit and hold functionality while the card is being given
            self.animateDealerCard = True # Set animateDealerCard to True, used to determine where to send the card
            
    def increaseScore(self,value, currentScore, player): # Used to increase the player of dealers score based on the cards score
        print(f'Inside increase score, the value being added is {value}')
        if len(value) > 1: # Check if the card is an ace
           currentScore = self.addAce(currentScore, value, player) # send the ace to the addAce function
        else:
            currentScore += value[0] # Increase the score by the value of the card
        return currentScore # Return the new score

    def addAce(self,currentScore,value, player): # Used to determine the value of an ace
        if value[0] + currentScore > 21: # Check if the ace being 11 causes the score to go over 21
            currentScore += value[1] # Make the aces value 1
        else:
            currentScore += value[0] # Make the aces value 11
            if player: # Check if it is the player
                self.playerAceCount += 1 # Increase the player ace count by 1
            else:
                self.dealerAceCount += 1 # Increase the dealers ace count by 1
        return currentScore # Return the new score

    def checkScore(self,score,aces, player = False): # Used to modify the aces
        if score > 21 and aces: # Checks if the score is over 21 and to see if there are any aces that are being counted with a value of 11
            score -= 10 # Subtract the score by 10, turning the ace from an 11 to a 1
            aces -= 1 # Subtract the amount of aces by 1
        return score, aces # Return the modified score and the new number of aces
    
    def checkGame(self,score,player = False): # Used to check if score results in 
        print('Inside Check Game with score:', score, player)
        if not self.start: # Check to make sure this is not the starting cards, used to stop unexpected behavior with function calling
            if (score == 21 and player and len(self.playerCardList) == 2): # Check if player has gotten blackjack
                self.checkWinner() # Call checkWinner to see who won the game
            elif (score == 21 and not player and len(self.dealerCardList) == 2):  # Check if dealer has gotten blackjack
                self.checkWinner() # Call checkWinner to see who won the game
            elif (score > 21 and player): # Check if the score is higher than 21
                self.checkWinner() # Call checkWinner to see who won the game
            elif score == 21 and player: # Check if the score is equal to 21
                self.handleStayButton() # Call handleStayButton

    def handleHitButton(self): # Used to handle the logic when the player hits the bet button
        if self.bettingActive == False and self.playerScore < 21 and self.playerTurn and self.animationDone == True: # Check if betting is off and if it is the players turn
            self.addCard(True) # Call addCard to add a card
    
    def startGame(self, turn): # Used to start the game
        if self.start: # Check if self.start is true
            match turn: # Check which turn it is
                    case 0:
                        self.addCard(True) # Call addCard with the parameter True to give the player a card
                    case 1:
                        self.addCard(False) # Call addCard with the parameter False to give the dealer a card
                    case 2:
                        self.addCard(True) # Call addCard with the parameter True to give the player a card
                    case 3:
                        self.addDealerSecondCard() # Call addDealerSecondCard to add the second card to the dealer
                        self.playerTurn = True # Change player turn to true
        else:
            self.checkGame(self.playerScore, True) # Call checkGame with the players score to check for blackjack
            self.checkGame(self.dealerScore, False) # Call checkGame with the dealers score to check for blackjack
    
    def addDealerSecondCard(self): # Used to add the second dealer card
        print('Adding second dealer card')
        card = self.chooseCard() # Call chooseCard to choose a random card
        self.secondDealerCard = card # Set secondDealerCard to the chosen card
        cardBack = game.image.load('./BlackJackAssets/back.svg') # Load the cardBack svg image
        cardBack = game.transform.scale(cardBack, (170,220)) # Scale the cardBack svg image to the correct size
        self.cardBeingAnimated = cardBack # Set the cardBeingAnimated variable to the cardBack
        self.animationDone = False # Set the animationDone to False, used to ensure player cannot click stay or hit and cause unexpected behavior with the animation
        self.animateDealerCard = True # Set the animateDealerCard to True, used to determine where the card goes
        self.secondDealerCardAnimation = True # set secondDealerCardAnimation to true, used for the logic when animating the second dealer card
    
    def handleStayButton(self): # Used to handle the logic for when the player clicks stay
        print(f'Insinde handSletayButton the length of dealer list is{len(self.dealerCardList)}')
        print(self.playerTurn)
        if self.bettingActive == False and self.playerTurn == True and self.animationDone == True: # Check if betting is False and if it is the players turn
            self.playerTurn = False # Change playerTurn to false, used
            self.flip() # Call self.flip to show the card that is hidden
            self.stay() # call stay to trigger the logic for the dealer to begin choosing cards
    
    def stay(self): # Used to handle the stay logic 
        if self.dealerScore < 17: # Check if the dealers score is less than 17 (dealer must hold at 17 or greater)
            self.addCard(False) # Call addCard with the parameter False to add a card to the dealer
        else:
            self.checkWinner() # Call checkWinner to see who won the game
    
    def checkWinner(self): # Used to check who won the game
        self.playerTurn = False # Set the playerTurn to False
        if self.reset == False: # Check if the game has already been reset
            if self.flipped == False: # Check if the card has been flipped
                self.flip() # Call flip to show the hidden card

            print(self.playerScore, self.dealerScore)
            self.playerTurn = False # Set player turn to false
            if self.playerScore > 21 and self.dealerScore <= 21: # Check if the playersScore is greater than 21 and the dealers is less than or equal to 21
                self.winner = 'D' # Assign the winner the value 'D' for dealer win
            elif self.dealerScore > 21 and self.playerScore <= 21: # Check if the dealerScore is greater than 21 and the players is less than or equal to 21
                self.winner = 'P'  # Assign the winner the value 'P' for player win
            elif (self.playerScore == self.dealerScore): # Check if the dealer score is equal to the player score
                self.winner = 'T'  # Assign the winner the value 'T' for tie
            elif (self.playerScore == 21 and len(self.playerCardList) == 2): # Check if the player has 21 and only has 2 cards
                self.winner = 'PBJ'  # Assign the winner the value 'PBJ' for player black jack
            elif (self.dealerScore == 21 and len(self.dealerCardList) == 2): # Check if dealer has 21 and only has 2 cards
                self.winner = 'DBJ'  # Assign the winner the value 'DBJ' for dealer black jack
            elif self.playerScore > self.dealerScore and self.playerScore <= 21: # Check if the player score is higher than the dealers score and if the player score is less than or equal to 21
                self.winner = 'P'  # Assign the winner the value 'P' for player win
            elif self.dealerScore > self.playerScore and self.dealerScore <= 21: # Check if dealer score higher than player score and if dealer score less than or equal to 21
                self.winner = 'D'  # Assign the winner the value 'D' for dealer win

            self.displayWinner() # Call displayWinner to display who won the game
            
    def resetGameLogic(self): # Used to reset the game logic
        print('Resetting logic')
        self.updateInformation('money') # Call updateInformation with the parameter money to update the players money
        self.bettingActive = True # Set bettingActive to true
        self.playerScore = 0 # Set playerScore to 0
        self.playerAceCount = 0 # Set playerAceCount to 0
        self.playerCardList = [] # Set the playerCardList to an empty list
        self.dealerScore = 0 # Set the dealerScore to 0
        self.dealerAceCount = 0 # Set the dealerAceCount to 0
        self.dealerCardList = [] # Set the dealerCardList to 0
        self.currentBet = 0 # Set the currentBet to 0
        self.initial = True # Set initial to True
        self.reset = True # Set reset to True
        self.betList = [] # Set betList to an empty list
        self.winner = None # Set winner to None
        self.flipped = False # Set flipped to false
        self.startingTurn = 0 # Set the startingTurn back to 0
        self.determineDeckShuffle() # Call determineDeckShuffle to see if the seenCards set needs to be reset
        print(f'Player score is now {self.playerScore}')
        print(f'Dealer score is now {self.dealerScore}')
        print('______________________________________________________')

    def determineDeckShuffle(self): # Used to determine when to reset the seenCards set
        print(f'Current set length {len(self.seenCards)}')
        if len(self.seenCards) >= len(self.deck) // 2: # Check if the length of the seenCards set is greater than or half the length of the deck
            self.seenCards.clear() # call the clear function to empty the set
            self.seenCards.add(1000) # Add 1000 to the set 