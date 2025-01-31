__author__ = 'Christy_Sze'

from tkinter import *
from slotsgameclasses import *

balance = Balance()
spin = Game()

class Slots(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("~*~ SLOTS MACHINE ~*~")
        self.grid()

        self._results = Label(self, text= "777")
        self._results.grid(row = 0, column = 1)

        self._message = Label(self, text= "")
        self._message.grid(row = 1)

        self._bet = Label(self, text= "Bet:")
        self._bet.grid(row = 2, column = 0)

        self._betVar = DoubleVar()
        self._amount = Entry(self, text= self._betVar)
        self._amount.grid(row = 2, column = 1)

        self._balance = Label(self, text= "Balance:")
        self._balance.grid(row = 3, column = 0)

        self._balanceamount = Label(self, text= str(balance.__str__()))
        self._balanceamount.grid(row = 3, column = 1)

        self._spinbutton = Button(self, text= "Spin", command = self._spin)
        self._spinbutton.grid(row = 4, column = 0)

        self._stopbutton = Button(self, text= "Cash Out", command = self._cashout)
        self._stopbutton.grid(row = 4, column = 1)

    def _spin(self):
        while True:
            bet = self._betVar.get()
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
        self._results["text"] = spin._results
        spin.reset()

    def _cashout(self):
        print("Thank you for playing. Your payout is: $" + str(balance.__str__()))

def main():
    Slots().mainloop()

main()