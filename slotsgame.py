__author__ = 'Christy_Sze'

from slotsgameclasses import *

balance = Balance()
spin = Game()

print("~*~ SLOTS MACHINE ~*~")
print("The maximum bet is $5.00, and the minimum is $1.00.")
print("Balance: $" + balance.__str__())

play = "y"
while play == "y":
    if float(balance.__str__()) < 1.00:
        print("Sorry! Not enough funds to play.")
        print("Thank you for playing. Your payout is: $" + str(balance.__str__()))
        quit()
    else:
        while True:
            bet = float(input("Enter bet: $"))
            if bet <= 5.00 and bet >= 1.00:
                if bet <= float(balance.__str__()):
                    balance.setBalance(bet)
                    print("$" + str(bet), "bet placed.")
                    break
                else:
                    print("Insufficient funds. Try Again.")
            elif bet > 5.00:
                print("Bet amount too high. Try again.")
            else:
                print("Bet amount too low. Try again.")
        spin.spin()
        symbols = spin.__str__()
        print("\n" + symbols)
        balance.reset()
        balance.win(bet, symbols)
        print("Balance: $" + balance.__str__())
        spin.reset()
        play = input("Enter \"y\" to spin again and \"n\" to stop: ")

print("Thank you for playing. Your payout is: $" + str(balance.__str__()))