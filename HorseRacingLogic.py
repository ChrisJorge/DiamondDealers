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
        self.selectedHorseBet = 0
        self.numberOfHighOdds = 0
        self.numberOfMediumOdds = 0
        self.numberOfLowOdds = 0
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

        self.horse1Frame = HorseFrame(self.screen, (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) / 5, self.screenWidth / 4, horseImage, 1, '0', (217,217,217), 0, self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3) )
        self.horse2Frame = HorseFrame(self.screen, (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) / 5, self.screenWidth / 4, horseImage, 2, '0', (217,217,217), 0, self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3) + ((300 + self.backGroundGrassHeightIndividualLane * 3) // 5) * 1.35)
        self.horse3Frame = HorseFrame(self.screen, (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) / 5, self.screenWidth / 4, horseImage, 3, '0', (217,217,217), 0, self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3) + ((300 + self.backGroundGrassHeightIndividualLane * 3) // 5) * 2.7)
        self.horse4Frame = HorseFrame(self.screen, (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) / 5, self.screenWidth / 4, horseImage, 4, '0', (217,217,217), 0, self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3) + ((300 + self.backGroundGrassHeightIndividualLane * 3) // 5) * 4.05)

        betBar = game.Rect(self.screenWidth - (self.screenWidth / 3), self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3), self.screenWidth / 3, 300 + self.backGroundGrassHeightIndividualLane * 3)
        game.draw.rect(self.screen, (217,217,217), betBar)
        self.currentHorseBeingBetOn = WriteText(self.screen, 30, f'Selected Horse: {self.selectedHorse}', (0,0,0), (217,217,217), self.screenWidth - (self.screenWidth / 4), self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3))
        currentHorseBetBar = game.Rect(self.screenWidth - (self.screenWidth / 4), self.screenHeight - ((300 + self.backGroundGrassHeightIndividualLane * 3) * .85), (self.screenWidth / 3) / 1.81, (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) / 10 )
        game.draw.rect(self.screen, (90, 90, 90), currentHorseBetBar)
        self.currentHorseBet = WriteText(self.screen, 30, f'${self.selectedHorseBet}', (255,255,255), (90,90,90), (self.screenWidth / 3) * 2.3, (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) * 1.16)

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

        self.confirmBet = Button(self.screen, (90,90,90), (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) / 12, (self.screenWidth / 3) / 1.81,  self.screenWidth - (self.screenWidth / 4), (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) * 1.59)
        self.confirmBet.write('Confirm Bet', 30, (255,255,255))
        self.removeBet = Button(self.screen, (90,90,90), (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) / 12, (self.screenWidth / 3) / 1.81,  self.screenWidth - (self.screenWidth / 4), (self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3)) * 1.69)
        self.removeBet.write('Remove Bet', 30, (255,255,255))
        
        moneyBar = game.Rect(self.screenWidth // 2.7, self.screenHeight - self.screenHeight // 25, self.screenWidth /6, self.screenHeight / 25)
        game.draw.rect(self.screen, (217,217,217), moneyBar)
        self.moneyText = WriteText(self.screen, 30, f'Money: ${self.playerMoney}', (0,0,0), (217,217,217), self.screenWidth // 2.7, self.screenHeight - self.screenHeight / 25)

        self.calculateHorseOdds()

    def initializeGrassNumber(self, number):
        blackBox = game.Rect(self.screenWidth - 150,self.backGroundGrassHeightIndividualLane * (number + number) - self.backGroundGrassHeightIndividualLane,self.backGroundGrassHeightIndividualLane, self.backGroundGrassHeightIndividualLane)
        game.draw.rect(self.screen, (0,0,0), blackBox)
        WriteText(self.screen, int(self.backGroundGrassHeightIndividualLane // 2), f'{number}', (255,255,255), (0,0,0), self.screenWidth - 150 + self.backGroundGrassHeightIndividualLane / 3.5, (self.backGroundGrassHeightIndividualLane * (number + number) - self.backGroundGrassHeightIndividualLane) + self.backGroundGrassHeightIndividualLane / 4.5)

    def calculateHorseOdds(self):
        number = random.randint(1,2)
        if number == 1 or number == 2:
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
                print(horse.horseOdds)
        else:
            pass
    
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
    
    def getHorseOdds(self, tier, odds):
        match tier:
            case 1:
                self.horseOdds = self.highOdds[odds]
            case 2:
                self.horseOdds = self.middleOdds[odds]
            case 3:
                self.horseOdds = self.lowOdds[odds]