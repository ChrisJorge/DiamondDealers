import pygame as game
import random
from Components import Write 
# Initialize an array holding the url paths to each of the images
assets = ['./BlackJackAssets/AceDiamond.svg', './BlackJackAssets/TwoDiamond.svg', './BlackJackAssets/ThreeDiamond.svg', './BlackJackAssets/FourDiamond.svg', 
          './BlackJackAssets/FiveDiamond.svg', './BlackJackAssets/SixDiamond.svg', './BlackJackAssets/SevenDiamond.svg', './BlackJackAssets/EightDiamond.svg', 
          './BlackJackAssets/NineDiamond.svg', './BlackJackAssets/TenDiamond.svg', './BlackJackAssets/KingDiamond.svg']

class BlackJack:
    def __init__(self, screen, screenHeight, screenWidth): # Function to initialize the blackjack class
        self.deck = {} # Initialize the deck dictionary
        self.playerScore = 0 # Initialize the playerScore with a value of 0, used to keep track of players current score
        self.playerCards = 0 # Initialize the playerCards with a value of 0, used to aid in positioning player cards on screen
        self.dealerScore = 0 # Initialize the dealerScore with a value of 0, used to keep track of dealers current score
        self.dealerCards = 0 # Initialize the dealerCards with a value of 0, used to aid in positioning dealer cards on screen
        self.screen = screen # Initialize screen, used to place objects on the screen
        self.screenHeight = screenHeight # Initialize screenHeight, used to help with positioning cards on screen
        self.screenWidth = screenWidth # Initialize screenWidth, used to help with positioning cards on screen
        self.dealerTurn = False # Initialize dealerTurn, keeps track on if it is the dealers turn
        self.playerTurn = True # Initialize playerTurn, keeps track on if it is the players turn
        self.secondDealerCard = None # Initialize secondDealerCard, used to keep track of what the seconc card the dealer has is.
        self.secondDealerCardX = None # Initialize secondDealerCardx, used to change the flipped over card
        self.secondDealerCardY = None # Initialize secondDealercardy, used to change the flipped over card
        self.secondDealerCardFlip = False # Initialize secondDealerCardFlip, used to make sure card is flipped over
        self.start = True # Initialize start, used to keep track of opening actions at each new game
        self.playerAceCount = 0 # Initialize playerAceCount, used to determine if player has gotten an Ace
        self.dealerAceCount = 0 # Initialize dealerAceCount, used to determine if dealer has gotten an Ace
        self.winner = None # Initialize winner, used to determine which winning text is output
        self.write = Write(self.screen, 25, self.screenWidth + (self.screenWidth * 0.2), self.screenHeight, (78, 106, 84))

        for index in range(len(assets)): # Loop through every single url path in the assets list
            card = game.image.load(assets[index]) # load the url path to the image in the variable card
            size = card.get_size() # Get the size of the card
            if size != (200,250): # Check to ensure uniformity in size
                card = game.transform.scale(card,(200,250)) # Resize the card if they are not the same
            if index == 0: # If index is 0 it is the ace card
                value = [1,11] # Put the two ace values
            elif index < 9: # Check if the index is less than 0
                value = [index + 1] # have the value variable be the index + 1 and put that in a list
            else:
                value = [10] # Set the value to 10
            self.deck[index] = (card, value) # Create the key in the dictionary being the index and have its value be (card, [value])
    
        self.startGame() # Call startGame function to start the game

    def getCard(self):
        index = random.randint(0, len(assets) - 1) # Use random.randint to get a random integer from 0 to the length of the list - 1 (inclusive)
        card = self.deck[index] # Get the card at that key
        return card # Return the card

    def checkScore(self, score, aces, player = False):
        if score > 21 and aces > 0: # Check if the score is greater than 21 and see if any aces are in the hand
            score -= 10 # Subtract the score by 10 turning the ace from an 11 to a 1
            aces -= 1 # Subtract the amount of aces by 1
        elif score > 21: # Check if score is greater than or equal to 21
            self.determineWinner() # Call determineWinner function
        elif score == 21 and player: # Check if the score is 21 for the player
            self.hold() # Call hold as player has 21
        elif score == 21 and player and self.start: # Check if player has 21 and it is the first 2 given cards
            self.determineWinner() # Call determineWinner function
        elif score == 21: # Check if the score is 21 for the dealer
            self.determineWinner() # Call determineWinner function
        return score, aces # Return the score and the number of aces

    
    def addPlayerCard(self): # Function to add a card for the player
        if (self.playerTurn and self.playerScore < 21) or self.start: # Check to make sure it is the players turn and that the players score isn't over 21
            card = self.getCard() # Call the get card function to get a card
            x, y = self.center(card[0], False) # Send the first value of the card, the picture, to the center function
            x += (50 * self.playerCards) # Increase the x axis coordinates by 50 for each card already on screen for the player
            self.screen.blit(card[0], (x,y)) # Put the card on the screen

            self.playerCards += 1 # Increase the playerCards variable by 1

            if len(card[1]) > 1: # Check if the length of the value list is greater than 1, if so it is the ace card
                if card[1][1] + self.playerScore > 21: # Check if adding the ace cards value of 11 would result in a score higher than 21
                    self.playerScore += card[1][0] # Add the aces value of 1 if the value would be greater than 21 if ace had a value of 11
                else:
                    self.playerScore += card[1][1] # Add the aces value of 11
                    self.playerAceCount += 1 # Increase ace count by 1
            else:
                self.playerScore += card[1][0] # Add the value of the card (non ace)

            self.write.score(self.playerScore, False)
            self.playerScore, self.playerAceCount = self.checkScore(self.playerScore, self.playerAceCount, True) # Send the score and aces to checkScore to see if game is over

    def addDealerCard(self, secondCard = False):
        if ((self.dealerTurn and self.dealerScore <= 16) or self.start): # Check to make sure it is the dealers turn and that dealers score isnt over 17
            card = self.getCard() # Call the get card function to get a card
            x,y = self.center(card[0], True) # Send the first value of the card, the picture, to the center function
            x += (50 * self.dealerCards) # Increase the x axis coordinates by 50 for each card already on screen for the dealer
            if secondCard: # Check if this is the second card given to the dealer
                self.secondDealerCard = card # set secondDealerCard to the current card
                cardBack = game.image.load('./BlackJackAssets/CardBack.svg') # Load the image with the back of a playing card
                cardBack = game.transform.scale(cardBack,(200,250)) # Scale the image to the correct size
                self.screen.blit(cardBack, (x,y)) # Put the card on the screen
                self.secondDealerCardX = x # Save the x coordinate value of the card
                self.secondDealerCardY = y # Save the y coordinate value of the card
            else:    
                self.screen.blit(card[0], (x,y)) # Put the card on the screen

            self.dealerCards += 1 # Increase the playerCards variable by 1

            if len(card[1]) > 1: # Check if the length of the value list is greater than 1, if so it is the ace card
                if card[1][1] + self.dealerScore > 21: # Check if adding the ace cards value of 11 would result in a score higher than 21
                    self.dealerScore += card[1][0] # Add the aces value of 1 if the value would be greater than 21 if ace had a value of 11
                else:
                    self.dealerScore += card[1][1] # Add the aces value of 11
                    self.dealerAceCount += 1 # Increase ace count by 1
            else:
                self.dealerScore += card[1][0] # Add the value of the card (non ace)    

            self.write.score(self.dealerScore, True)
            self.dealerScore, self.dealerAceCount = self.checkScore(self.dealerScore, self.dealerAceCount) # Send the score and aces to checkScore to see if game is over
        else:
            self.dealerTurn = False # Set dealerTurn to false if dealer hand is over 17
            

    def center(self, asset, top):
        middleHeight = self.screenHeight // 2 # Get the middle of the screen
        assetSize = asset.get_size() # Get the size of the image
        widthBeginning = self.screenWidth * 0.2 # Get where the playable screen, not including the left gray box, begins.
        width = ((self.screenWidth - widthBeginning) // 2) + assetSize[0] # Get the center width
        if top: # Check if these cards are going to the dealer
           heightBeginning = 0 # Beginning height is set to 0 as 0 is the top 
           height = ((middleHeight - heightBeginning)  - ((assetSize[1] * 0.5) + (assetSize[1] * 0.85))) # Subtract the middle by the top and subtracts the asset size to get the center of top 
        else:
        # Add middleHeight and screenHeight then divide by 2 and subtract by half the asset size to get center of bottom half
           height = (((middleHeight + self.screenHeight) // 2 ) - (assetSize[1] * 0.5))
        return width, height # Return the width and the height
    
    def hold(self):
        if self.playerTurn: # Check if it is the players turn
            self.playerTurn = False # Change playersTurn to false
            self.dealerTurn = True # Change dealersTurn to true
            self.flip() # Call flip to flip over the card
            while self.dealerTurn: # While it is the dealers turn
                self.addDealerCard() # Call addDealerCard function to give dealer a card
            self.determineWinner() # Call self.determineWinner to determine who won the game


    def startGame(self):
        for turn in range(4): # Loop through 4 turns, 2 for player 2 for dealer
            if turn % 2 == 0: # Check if the turn is even
                self.addPlayerCard() # Call the addPlayerCard function
            else:
                if turn == 3: # Check if the turn is the last turn for the dealer
                    self.addDealerCard(True) # Call addDealerCard with True makes the card back show 
                else:
                    self.addDealerCard() # Call addDealerCard function
            self.write.score(self.playerScore, False)
            self.write.score('??', True)
            self.playerScore, self.playerAceCount = self.checkScore(self.playerScore, self.playerAceCount) # Check if player has blackjack after initial cards
            self.dealerScore, self.dealerAceCount = self.checkScore(self.dealerScore, self.dealerAceCount) # Check if dealer has blackjack after initial cards
        self.start = False # Change start to false

       
    def determineWinner(self):
        # Playerwin = 0
        # Dealerwin = 1
        self.dealerTurn = False # Ensure dealer turn is false
        self.playerTurn = False # Ensure player turn is false
        if not self.secondDealerCardFlip: # Check if the card has not been flipped
            self.flip() # Call flip to flip the card

        self.write.score(self.playerScore, False)
        self.write.score(self.dealerScore, True)

        if self.playerScore == self.dealerScore: # Check if both players have the same score
            self.winner = 2 # Set winner to tie
        elif self.playerScore > 21: # Check if player score is over 21
            self.winner = 1 # Set winner to dealer
        elif self.dealerScore > 21: # Check if dealer score is over 21
            self.winner = 0 # Set winner to player
        else:
            if self.playerScore > self.dealerScore: # Check if player has higher score than dealer
                self.winner = 0 # Set winner to player
            else:
                self.winner = 1 # Set winner to dealer
        return self.winner # Return self.winner
    
    def restartGame(self):
        self.playerScore = 0 # Reset the playerScore with a value of 0, used to keep track of players current score
        self.playerCards = 0 # Reset the playerCards with a value of 0, used to aid in positioning player cards on screen
        self.dealerScore = 0 # Reset the dealerScore with a value of 0, used to keep track of dealers current score
        self.dealerCards = 0 # Reset the dealerCards with a value of 0, used to aid in positioning dealer cards on screen
        self.dealerTurn = False # Reset dealerTurn, keeps track on if it is the dealers turn
        self.playerTurn = True # Reset playerTurn, keeps track on if it is the players turn
        self.secondDealerCard = None # Reset secondDealerCard, used to keep track of what the seconc card the dealer has is.
        self.secondDealerCardX = None # Reset secondDealerCardx, used to change the flipped over card
        self.secondDealerCardY = None # Reset secondDealercardy, used to change the flipped over card
        self.secondDealerCardFlip = False # Reset secondDealerCardFlip, used to make sure card is flipped over
        self.start = True # Reset start, used to keep track of opening actions at each new game
        self.playerAceCount = 0 # Reset playerAceCount, used to determine if player has gotten any aces
        self.dealerAceCount = 0 # Reset dealerAceCount, used to determine if dealer has gotten any aces
        self.winner = None # Reset winner, used to determine if game is over
        game.draw.rect(self.screen, (78, 106, 84), game.Rect(self.screenWidth * 0.2,0, self.screenWidth, self.screenHeight)) # Create the gray bar on the left side which will contain the options 
        self.startGame() # call startGame function to restart game

    def flip(self):
        if not self.secondDealerCardFlip and self.secondDealerCard is not None: # Check if the second card has not been flipped and if the second card exists
             self.screen.blit(self.secondDealerCard[0], (self.secondDealerCardX,self.secondDealerCardY)) # Flip over the card
             self.secondDealerCardFlip = True # Change flipped to true