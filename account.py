import pickle

with open('data.pkl', 'wb') as file:
    pickle.dump()
class Account:
    def __init__(self, accountnum):
        self.accountnum = accountnum
        self.card = None
        self.__balance = 0

    def get_balance(self):
        print(self.__balance)
        return self.__balance

    def deposit(self, value):
        self.__balance += value

    def withdraw(self, value):
        if value <= self.__balance:
            self.__balance -= value
            return True
        else:
            print('Not enough money.')
            return False

class Card:
    def __init__(self):
        self.__PIN = None
        self.account = None

    