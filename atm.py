import pickle
from account import *

class Atm:
    def __init__(self):
        pass

    def insert_card(self, card):
        with open('cards/num_card.txt', 'r') as f:
            len_cards = int(f.read())
        if not card.pin_check():
            return False
        for i in range(len_cards):
            with open('cards/card_{}.bin'.format(0), 'rb') as f3:
                card0 = pickle.load(f3)
            if card.account.accountnum == card0.account.accountnum:
                return i
        return False

    def verify_account(self, account):
        pass

    def verify_pin(self, card):
        pass

    def verify_admin(self, password):
        pass