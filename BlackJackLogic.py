import pygame as game
import random
# Initialzie an array holding the url paths to each of the images
assets = ['./BlackJackAssets/AceDiamond.svg', './BlackJackAssets/TwoDiamond.svg', './BlackJackAssets/ThreeDiamond.svg', './BlackJackAssets/FourDiamond.svg', 
          './BlackJackAssets/FiveDiamond.svg', './BlackJackAssets/SixDiamond.svg', './BlackJackAssets/SevenDiamond.svg', './BlackJackAssets/EightDiamond.svg', 
          './BlackJackAssets/NineDiamond.svg', './BlackJackAssets/TenDiamond.svg', './BlackJackAssets/KingDiamond.svg']

class BlackJack:
    def __init__(self, screenHeight, screenWidth): # Function to initialize the blackjack class
        self.deck = {} # Initialize the deck dictionary
        self.playerScore = 0 # Initialize the playerScore with a value of 0, used to keep track of players current score
        self.playerCards = 0 # Initialize the playerCards with a value of 0, used to aid in positioning player cards on screen
        self.dealerScore = 0 # Initialize the dealerScore with a value of 0, used to keep track of dealers current score
        self.dealerCards = 0 # Initialize the dealerCards with a value of 0, used to aid in positioning dealer cards on screen
        self.screenHeight = screenHeight # Initialize screenHeight, used to help with positioning cards on screen
        self.screenWidth = screenWidth # Initialize screenWidth, used to help with positioning cards on screen
        self.dealerTurn = False # Initialize dealerTurn, keeps track on if it is the dealers turn
        self.playerTurn = True # Initialize playerTurn, keeps track on if it is the players turn
        self.gameOver = False # Initialize gameOver, keeps track on if the game is over

        for index in range(len(assets)): # Loop through every single url path in the assets list
            card = game.image.load(assets[index]) # load the url path to the image in the variable card
            size = card.get_size() # Get the size of the card
            if size != (200,250): # Check to ensure uniformity in size
                card = game.transform.scale(card,(200,250)) # Resize the card if they are not the same
            if index == 0: # If indez is 0 it is the ace card
                value = [1,11] # Put the two ace values
            elif index < 9: # Check if the index is less than 0
                value = [index + 1] # have the value variable be the index + 1 and put that in a list
            else:
                value = [10] # Set the value to 10
            self.deck[index] = (card, value) # Create the key in the dictionary being the index and have its value be (card, [value])
    
    def addPlayerCard(self, screen): # Function to add a card for the player
        if self.playerTurn and self.playerScore < 21: # Check to make sure it is the players turn and that the players score isn't over 21
            index = random.randint(0, len(assets) - 1) # Use random.randint to get a random integer from 0 to the length of the list - 1 (inclusive)
            card = self.deck[index] # Get the card at that key
            x, y = self.center(card[0], False) # Send the first value of the card, the picture, to the, center function
            x += (50 * self.playerCards) # Increase the x axis coordinates by 50 for each card already on screen for the player
            screen.blit(card[0], (x,y)) # Put the card on the screen

            self.playerCards += 1 # Increase the playerCards variable by 1

            if len(card[1]) > 1: # Check if the length of the value list is greater than 1, if so it is the ace card
                if card[1][1] + self.playerScore > 21: # Check if adding the ace cards value of 11 would result in a score higher than 21
                    self.playerScore += card[1][0] # Add the aces value of 1 if the value would be greater than 21 if ace had a value of 11
                else:
                    self.playerScore += card[1][1] # Add the aces value of 11
            else:
                self.playerScore += card[1][0] # Add the value of the card (non ace)


    def center(self, asset, top):
        middleHeight = self.screenHeight // 2 # Get the middle of the screen
        assetSize = asset.get_size() # Get the size of the image
        widthBeginning = self.screenWidth * 0.2 # Get where the playable screen, not including the left gray box, begins.
        width = ((self.screenWidth - widthBeginning) // 2) + assetSize[0] # Get the center width
        if top: # Check if these cards are going to the dealer
           heightBeginning = 0 # Beginning height is set to 0 as 0 is the top 
           height = ((middleHeight - heightBeginning)  - assetSize[1]) # Subtract the middle by the top and subtracts the asset size to get the center of top 
        else:
        # Add middleHeight and screenHeight then divide by 2 and subtract by half the asset size to get center of bottom half
           height = (((middleHeight + self.screenHeight) // 2 ) - (assetSize[1] * 0.5))
        return width, height # return the width and the height