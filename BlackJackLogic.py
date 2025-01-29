import pygame as game
import random
assets = ['./BlackJackAssets/AceDiamond.svg', './BlackJackAssets/TwoDiamond.svg', './BlackJackAssets/ThreeDiamond.svg', './BlackJackAssets/FourDiamond.svg', 
          './BlackJackAssets/FiveDiamond.svg', './BlackJackAssets/SixDiamond.svg', './BlackJackAssets/SevenDiamond.svg', './BlackJackAssets/EightDiamond.svg', 
          './BlackJackAssets/NineDiamond.svg', './BlackJackAssets/TenDiamond.svg', './BlackJackAssets/KingDiamond.svg']

class BlackJack:
    def __init__(self, screenHeight, screenWidth):
        self.deck = {}
        self.playerScore = 0
        self.playerCards = 0
        self.dealerScore = 0
        self.dealerCards = 0
        self.screenHeight = screenHeight
        self.screenWidth = screenWidth
        self.dealerTurn = False
        self.playerTurn = True
        self.gameOver = False
        for index in range(len(assets)):
            card = game.image.load(assets[index])
            size = card.get_size()
            if size != (200,250):
                card = game.transform.scale(card,(200,250))
            if index == 0:
                value = [1,11]
            elif index < 9:
                value = [index + 1]
            else:
                value = [10]
            self.deck[index] = (card, value)
    
    def addPlayerCard(self, screen):
        if self.playerTurn and self.gameOver != True:
            index = random.randint(0, len(assets) - 1)
            card = self.deck[index]
            x, y = self.center(card[0], False)
            x += (50 * self.playerCards)
            screen.blit(card[0], (x,y))

            self.playerCards += 1

            if len(card[1]) > 1:
                if card[1][1] + self.playerScore > 21:
                    self.playerScore += card[1][0]
                else:
                    self.playerScore += card[1][1]
            else:
                self.playerScore += card[1][0]
        


    def center(self, asset, top):
        middleHeight = self.screenHeight // 2
        assetSize = asset.get_size()
        widthBeginning = self.screenWidth * 0.2
        width = ((self.screenWidth - widthBeginning) // 2) + assetSize[0]
        if top:
           heightBeginning = 0
           height = ((middleHeight - heightBeginning)  - assetSize[1])
        else:
           height = (((middleHeight + self.screenHeight) // 2 ) - (assetSize[1] * 0.5))
        return width, height