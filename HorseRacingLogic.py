import pygame as game
from Components import WriteText

class HorseRacing:

    def __init__(self, screen, screenHeight, screenWidth, playerMoney):
        self.screen = screen 
        self.screenHeight = screenHeight 
        self.screenWidth = screenWidth
        self.playerMoney = playerMoney
        self.backGroundGrassHeightIndividualLane = ((self.screenHeight - 300) / 12)
        print(self.backGroundGrassHeightIndividualLane)
        self.initializeScreen()

    def initializeScreen(self):
        self.backGround = game.image.load('./HorseRaceAssets/BackGround.jpg')
        self.backGround = game.transform.rotate(self.backGround, 90)
        self.backGround = game.transform.scale(self.backGround, (self.screenWidth, self.screenHeight - 300))
        self.screen.blit(self.backGround, (0,0))
        print(self.screenHeight)
        self.finishLine = game.image.load('./HorseRaceAssets/FinishLine.svg')
        self.screen.blit(self.finishLine, (self.screenWidth - 300, 0))
        bottomBar = game.Rect(0, self.screenHeight - (300 + self.backGroundGrassHeightIndividualLane * 3), self.screenWidth, 300 + self.backGroundGrassHeightIndividualLane * 3) # Create the bottom brown bar that will hold all of the options
        game.draw.rect(self.screen, (106,84,78), bottomBar) # Place the bottom bar onto the screen

        for number in range(1,5):
            self.initializeNumber(number)

        horseImage = game.image.load('./HorseRaceAssets/Horse_transparent.png')
        horseImage = game.transform.scale(horseImage, (self.backGroundGrassHeightIndividualLane + 20, self.backGroundGrassHeightIndividualLane + 20))
        self.horse1 = Horse(self.screen,self.backGroundGrassHeightIndividualLane, horseImage, 1)
        self.horse2 = Horse(self.screen,self.backGroundGrassHeightIndividualLane, horseImage, 2)
        self.horse3 = Horse(self.screen,self.backGroundGrassHeightIndividualLane, horseImage, 3)
        self.horse4 = Horse(self.screen,self.backGroundGrassHeightIndividualLane, horseImage, 4)

    def initializeNumber(self, number):
        blackBox = game.Rect(self.screenWidth - 150,self.backGroundGrassHeightIndividualLane * (number + number) - self.backGroundGrassHeightIndividualLane,self.backGroundGrassHeightIndividualLane, self.backGroundGrassHeightIndividualLane)
        game.draw.rect(self.screen, (0,0,0), blackBox)
        WriteText(self.screen, int(self.backGroundGrassHeightIndividualLane // 2), f'{number}', (255,255,255), (0,0,0), self.screenWidth - 150 + self.backGroundGrassHeightIndividualLane / 3.5, (self.backGroundGrassHeightIndividualLane * (number + number) - self.backGroundGrassHeightIndividualLane) + self.backGroundGrassHeightIndividualLane / 4.5)

    

class Horse:
    def __init__(self, screen, heightOfLane, horseImage, horseNumber):
        self.screen = screen
        self.heightOfLane = heightOfLane
        self.horseImage = horseImage
        self.horseNumber = horseNumber
        self.screen.blit(horseImage, (50, self.heightOfLane * (self.horseNumber + self.horseNumber) - (self.heightOfLane + 15)))
        