import pygame as game
from Components import WriteText, HorseFrame, Button
import random

class HorseRacing:

    def __init__(self, screen, screenHeight, screenWidth, playerMoney):
        self.screen = screen 
        self.screenHeight = screenHeight 
        self.screenWidth = screenWidth
        self.playerMoney = playerMoney
        self.backGroundGrassHeightIndividualLane = ((self.screenHeight - 300) / 12)
        self.selectedHorse = 'N/A'
        self.numberOfHighOdds = 0
        self.numberOfMediumOdds = 0
        self.numberOfLowOdds = 0
        self.currentBet = 0
        self.betArray = []
        self.warningWritten = False
        self.raceStarted = False
        self.startTime = 0
        self.currentTime = 0
        self.startingLineFinishCoordinate = self.screenWidth - 300
        self.winnerFound = False
        self.winner = None
        self.gameType = 'horseRacing'
        self.initializeScreen()

    def initializeScreen(self):
        self.backGround = game.image.load('./HorseRaceAssets/BackGround.jpg')
        self.backGround = game.transform.rotate(self.backGround, 90)
        self.backGround = game.transform.scale(self.backGround, (self.screenWidth, self.screenHeight - 300))
        self.screen.blit(self.backGround, (0,0))
        self.finishLine = game.image.load('./HorseRaceAssets/FinishLine.svg')
        self.screen.blit(self.finishLine, (self.screenWidth - 300, 0))
        bottomBar = game.Rect(0, self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3), self.screenWidth, 300 + self.backGroundGrassHeightIndividualLane * 3) # Create the bottom brown bar that will hold all of the options
        game.draw.rect(self.screen, (106,84,78), bottomBar) # Place the bottom bar onto the screen

        for number in range(1,5):
            self.initializeGrassNumber(number)

        horseImage = game.image.load('./HorseRaceAssets/Horse_transparent.png')
        horseImage = game.transform.scale(horseImage, (self.backGroundGrassHeightIndividualLane + 20, self.backGroundGrassHeightIndividualLane + 20))
        self.horse1 = Horse(self.screen, self.backGroundGrassHeightIndividualLane, horseImage, 1)
        self.horse2 = Horse(self.screen, self.backGroundGrassHeightIndividualLane, horseImage, 2)
        self.horse3 = Horse(self.screen, self.backGroundGrassHeightIndividualLane, horseImage, 3)
        self.horse4 = Horse(self.screen, self.backGroundGrassHeightIndividualLane, horseImage, 4)

        self.horseArray = [self.horse1, self.horse2, self.horse3, self.horse4]

        self.frameHeight = (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) / 5
        self.frameWidth = self.screenWidth / 4

        self.horse1Button = Button(self.screen, (217,217,217), self.frameHeight , self.frameWidth, 0, self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3))
        self.horse1Frame = HorseFrame(self.screen, self.frameHeight, self.frameWidth, horseImage, 1, '0', (217,217,217), 0, self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3))

        self.horse2Button = Button(self.screen, (217,217,217), self.frameHeight, self.frameWidth, 0, self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3) + ((300 + self.backGroundGrassHeightIndividualLane * 3) // 5) * 1.35 )
        self.horse2Frame = HorseFrame(self.screen,self.frameHeight, self.frameWidth, horseImage, 2, '0', (217,217,217), 0, self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3) + ((300 + self.backGroundGrassHeightIndividualLane * 3) // 5) * 1.35)

        self.horse3Button = Button(self.screen, (217,217,217), self.frameHeight, self.frameWidth, 0, self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3) + ((300 + self.backGroundGrassHeightIndividualLane * 3) // 5) * 2.7 )
        self.horse3Frame = HorseFrame(self.screen, self.frameHeight, self.frameWidth, horseImage, 3, '0', (217,217,217), 0, self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3) + ((300 + self.backGroundGrassHeightIndividualLane * 3) // 5) * 2.7)

        self.horse4Button = Button(self.screen, (217,217,217), self.frameHeight, self.frameWidth, 0, self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3) + ((300 + self.backGroundGrassHeightIndividualLane * 3) // 5) * 4.05 )
        self.horse4Frame = HorseFrame(self.screen, self.frameHeight, self.frameWidth, horseImage, 4, '0', (217,217,217), 0, self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3) + ((300 + self.backGroundGrassHeightIndividualLane * 3) // 5) * 4.05)

        betBar = game.Rect(self.screenWidth - (self.screenWidth / 3), self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3), self.screenWidth / 3, 300 + self.backGroundGrassHeightIndividualLane * 3)
        game.draw.rect(self.screen, (217,217,217), betBar)
        self.currentHorseBeingBetOnText = WriteText(self.screen, 30, f'Selected Horse: {self.selectedHorse}', (0,0,0), (217,217,217), self.screenWidth - (self.screenWidth / 4), self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3))
        currentHorseBetBar = game.Rect(self.screenWidth - (self.screenWidth / 4), self.screenHeight - ((300 + self.backGroundGrassHeightIndividualLane * 3) * .85), (self.screenWidth / 3) / 1.81, (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) / 10 + 10)
        game.draw.rect(self.screen, (90, 90, 90), currentHorseBetBar)
        self.currentBetText = WriteText(self.screen, 30, f'${self.currentBet}', (255,255,255), (90,90,90), (self.screenWidth / 3) * 2.3, (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) * 1.16)

        self.oneDollarBet = Button(self.screen, (90,90,90), (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) / 15, (self.screenWidth / 3) / 6.5, (self.screenWidth / 3) * 2.25, (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) * 1.29)
        self.oneDollarBet.write('$1', 25, (255,255,255))
        self.fiveDollarBet = Button(self.screen, (90,90,90), (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) / 15, (self.screenWidth / 3) / 6.5, (self.screenWidth / 3) * 2.45, (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) * 1.29)
        self.fiveDollarBet.write('$5', 25, (255,255,255))
        self.tenDollarBet = Button(self.screen, (90,90,90), (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) / 15, (self.screenWidth / 3) / 6.5, (self.screenWidth / 3) * 2.65, (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) * 1.29)
        self.tenDollarBet.write('$10', 25, (255,255,255))

        self.twentyFiveDollarBet = Button(self.screen, (90,90,90), (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) / 15, (self.screenWidth / 3) / 6.5, (self.screenWidth / 3) * 2.25, (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) * 1.39)
        self.twentyFiveDollarBet.write('$25', 25, (255,255,255))
        self.fiftyDollarBet = Button(self.screen, (90,90,90), (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) / 15, (self.screenWidth / 3) / 6.5, (self.screenWidth / 3) * 2.45, (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) * 1.39)
        self.fiftyDollarBet.write('$50', 25, (255,255,255))
        self.oneHundredDollarBet = Button(self.screen, (90,90,90), (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) / 15, (self.screenWidth / 3) / 6.5, (self.screenWidth / 3) * 2.65, (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) * 1.39)
        self.oneHundredDollarBet.write('$100', 25, (255,255,255))

        self.fiveHundredDollarBet = Button(self.screen, (90,90,90), (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) / 15, (self.screenWidth / 3) / 6.5, (self.screenWidth / 3) * 2.25, (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) * 1.49)
        self.fiveHundredDollarBet.write('$500', 25, (255,255,255))
        self.oneThousandDollarBet = Button(self.screen, (90,90,90), (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) / 15, (self.screenWidth / 3) / 6.5, (self.screenWidth / 3) * 2.45, (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) * 1.49)
        self.oneThousandDollarBet.write('$1000', 25, (255,255,255))
        self.fiveThousandDollarBet = Button(self.screen, (90,90,90), (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) / 15, (self.screenWidth / 3) / 6.5, (self.screenWidth / 3) * 2.65, (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) * 1.49)
        self.fiveThousandDollarBet.write('$5000', 25, (255,255,255))

        self.confirmBetButton = Button(self.screen, (90,90,90), (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) / 12, (self.screenWidth / 3) / 1.81,  self.screenWidth - (self.screenWidth / 4), (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) * 1.59)
        self.confirmBetButton.write('Confirm Bet', 30, (255,255,255))
        self.removeBetButton = Button(self.screen, (90,90,90), (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) / 12, (self.screenWidth / 3) / 1.81,  self.screenWidth - (self.screenWidth / 4), (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) * 1.69)
        self.removeBetButton.write('Remove Bet', 30, (255,255,255))
        self.warningText = WriteText(self.screen, 30, '', (255,0,0), (217,217,217), self.screenWidth - (self.screenWidth / 4), (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) * 1.79)
        
        moneyBar = game.Rect(self.screenWidth // 2.7, self.screenHeight - self.screenHeight // 24.5, self.screenWidth /6, self.screenHeight / 24.5)
        game.draw.rect(self.screen, (217,217,217), moneyBar)
        self.playerMoneyText = WriteText(self.screen, 30, f'Money: ${self.playerMoney}', (0,0,0), (217,217,217), self.screenWidth // 2.7, self.screenHeight - self.screenHeight / 25)

        self.timeText = WriteText(self.screen, 30, f'Next Race: {30 - self.currentTime}', (0,0,0),(106,84,78), self.screenWidth // 2.8,  self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3))
        self.lastRaceWinnerText = WriteText(self.screen, 30, 'Previous Race Winner: N/A', (0,0,0), (106,84,78), self.screenWidth // 2.8, self.screenHeight - ((300 + self.backGroundGrassHeightIndividualLane * 3) * .75))

        self.exitButton = Button(self.screen, (90,90,90), self.screenHeight // 20, self.screenWidth // 20, self.screenWidth - (self.screenWidth // 20), 0 )
        self.exitButton.write('Exit', 35, (255,255,255))
        self.calculateHorseOdds()

    def initializeGrassNumber(self, number):
        blackBox = game.Rect(self.screenWidth - 150,self.backGroundGrassHeightIndividualLane * (number + number) - self.backGroundGrassHeightIndividualLane,self.backGroundGrassHeightIndividualLane, self.backGroundGrassHeightIndividualLane)
        game.draw.rect(self.screen, (0,0,0), blackBox)
        WriteText(self.screen, int(self.backGroundGrassHeightIndividualLane // 2), f'{number}', (255,255,255), (0,0,0), self.screenWidth - 150 + self.backGroundGrassHeightIndividualLane / 3.5, (self.backGroundGrassHeightIndividualLane * (number + number) - self.backGroundGrassHeightIndividualLane) + self.backGroundGrassHeightIndividualLane / 4.5)

    def calculateHorseOdds(self):
        self.numberOfHighOdds = 0
        self.numberOfMediumOdds = 0
        self.numberOfLowOdds = 0
        for horse in self.horseArray:
            tierAccepted = False
            while not tierAccepted:
                tier = random.randint(1,3)
                match tier:
                    case 1:
                        if self.numberOfHighOdds < 2:
                            self.numberOfHighOdds += 1
                            tierAccepted = True
                    case 2:
                        if self.numberOfMediumOdds < 2:
                            self.numberOfMediumOdds += 1
                            tierAccepted = True
                    case 3:
                        if self.numberOfLowOdds < 2:
                            self.numberOfLowOdds += 1
                            tierAccepted = True
                odds = random.randint(0,2)
                horse.getHorseOdds(tier, odds)
                self.updateOdds(horse.horseNumber)
    
    def updateOdds(self, number):
        match number:
            case 1:
                self.horse1Frame.oddsText.update(f'Odds: {self.horse1.horseOdds}')
            case 2:
                self.horse2Frame.oddsText.update(f'Odds: {self.horse2.horseOdds}')
            case 3:
                self.horse3Frame.oddsText.update(f'Odds: {self.horse3.horseOdds}')
            case 4:
                self.horse4Frame.oddsText.update(f'Odds: {self.horse4.horseOdds}')

    def selectHorse(self, number):
        match number:
            case 1:
                self.selectedHorse = self.horse1
            case 2:
                self.selectedHorse = self.horse2
            case 3:
                self.selectedHorse = self.horse3
            case 4:
                self.selectedHorse = self.horse4
        self.currentHorseBeingBetOnText.update(f'Selected Horse: Horse {self.selectedHorse.horseNumber}')
    
    def placeBet(self, value):
        if self.playerMoney >= value:
            self.currentBet += value
            self.playerMoney -= value
            self.betArray.append(value)
            self.updateInformation('bet + playerMoney')
            self.removeWarning()
        else:
            self.warningText.update('Not enough money', self.frameWidth)
            self.warningWritten = True
    
    def removeBet(self):
        if len(self.betArray) > 0:
            val = self.betArray.pop()
            self.currentBet -= val 
            self.playerMoney += val
            self.updateInformation('bet + playerMoney')
        else:
            self.warningText.update('No bet to remove', self.frameWidth)
            self.warningWritten = True
    
    def confirmBet(self):
        if self.raceStarted == False:
            if self.currentBet > 0:
                if self.selectedHorse != 'N/A':
                    self.selectedHorse.betAmount += self.currentBet
                    self.currentBet = 0
                    self.betArray = []
                    self.updateInformation(self.selectedHorse.horseNumber)
                    self.updateInformation('bet')
                    self.removeWarning()
                else:
                    self.warningText.update('A horse must be selected', self.frameWidth)
                    self.warningWritten = True
            else:
                self.warningText.update('Bet cannot be zero', self.frameWidth)
                self.warningWritten = True
        else:
            self.warningText.update('Cannot bet during the race', self.frameWidth)
            self.warningWritten = True

    def removeWarning(self):
        if self.warningWritten:
            self.warningWritten = False
            self.warningText.update('', self.frameWidth)

    def updateTime(self):
        if self.currentTime == 30:
            self.raceStarted = True
            self.timeText.update('Next Race: Now', 30)
        else:
            self.timeText.update(f'Next Race: {30 - self.currentTime}', 30)
    
    def moveHorses(self):
        self.replaceItemsOnScreen()
        self.screen.blit(self.horse1.horseImage, (self.horse1.horseX, self.horse1.horseY))
        self.screen.blit(self.horse2.horseImage, (self.horse2.horseX, self.horse2.horseY))
        self.screen.blit(self.horse3.horseImage, (self.horse3.horseX, self.horse3.horseY))
        self.screen.blit(self.horse4.horseImage, (self.horse4.horseX, self.horse4.horseY))
        self.checkForWinner()

    def checkForWinner(self):
        if self.winnerFound == False:
            self.checkCoordinates(self.horse1)
            self.checkCoordinates(self.horse2)
            self.checkCoordinates(self.horse3)
            self.checkCoordinates(self.horse4)

    def checkCoordinates(self, horse):
        if horse.horseX >= self.startingLineFinishCoordinate and self.winnerFound == False:
            self.winnerFound = True
            self.winner = horse
            self.lastRaceWinnerText.update(f'Previous Race Winner: Horse {self.winner.horseNumber}')
            self.resetRace()

    def replaceItemsOnScreen(self):
        self.screen.blit(self.backGround, (0,-170))
        self.screen.blit(self.finishLine, (self.screenWidth - 300, -17))
        for number in range(1,5):
            self.initializeGrassNumber(number)

    def resetRace(self):
        self.givePlayerMoney()
        self.raceStarted = False
        self.calculateHorseOdds()
        self.replaceItemsOnScreen()
        for horse in self.horseArray:
            horse.placeHorse()
            horse.horseX = 10
            horse.betAmount = 0
            self.updateInformation(horse.horseNumber)
        self.winnerFound = False
        self.winner = None
        self.startTime = game.time.get_ticks()
        self.calculateHorseOdds()

    def givePlayerMoney(self):
        self.playerMoney += (self.winner.betAmount * self.winner.multiplyAmount)
        self.updateInformation('money') 

    def updateInformation(self, info):
        match info:
            case 'bet + playerMoney':
                self.currentBetText.update(f'${self.currentBet}', 50)
                self.playerMoneyText.update(f'Money: ${self.playerMoney}', 50)
            case 'bet':
                self.currentBetText.update(f'${self.currentBet}', 50)
            case 1:
                self.horse1Frame.betAmountText.update(f'${self.horse1.betAmount}', 50)
            case 2:
                self.horse2Frame.betAmountText.update(f'${self.horse2.betAmount}', 50)
            case 3:
                self.horse3Frame.betAmountText.update(f'${self.horse3.betAmount}', 50)
            case 4:
                self.horse4Frame.betAmountText.update(f'${self.horse4.betAmount}', 50)
            case 'money':
                self.playerMoneyText.update(f'Money: ${self.playerMoney}', 50)

class Horse:
    def __init__(self, screen, heightOfLane, horseImage, horseNumber):
        self.screen = screen
        self.heightOfLane = heightOfLane
        self.horseImage = horseImage
        self.horseNumber = horseNumber
        self.screen.blit(horseImage, (10, self.heightOfLane * (self.horseNumber + self.horseNumber) - (self.heightOfLane + 15)))
        self.wonLastGame = False
        self.highOdds = ['2/1', '5/1', '3/1']
        self.middleOdds = ['10/1', '15/1', '12/1']
        self.lowOdds = ['26/1', '24/1', '30/1']
        self.horseOdds = None
        self.betAmount = 0
        self.speed = 0
        self.horseX = 10
        self.horseY = self.heightOfLane * (self.horseNumber + self.horseNumber) - (self.heightOfLane + 15)
    
    def placeHorse(self):
        self.screen.blit(self.horseImage, (10, self.heightOfLane * (self.horseNumber + self.horseNumber) - (self.heightOfLane + 15)))

    def getHorseOdds(self, tier, odds):
        match tier:
            case 1:
                self.horseOdds = self.highOdds[odds]
            case 2:
                self.horseOdds = self.middleOdds[odds]
            case 3:
                self.horseOdds = self.lowOdds[odds]
        self.determineSpeed()
    
    def determineSpeed(self):
        numerator = ''
        denominator = ''
        firstHalf = True
        for character in self.horseOdds:
            if character == '/':
                firstHalf = False
                
            if firstHalf and character != '/':
                numerator += character
            elif character != '/':
                denominator += character
        
        self.multiplyAmount = int(numerator)
        additionalSpeed = int(denominator) / int(numerator)
        number = random.random()
        self.speed = additionalSpeed + number
        