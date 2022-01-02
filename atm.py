import pickle
from account import *
from config import admins
class Atm:
    def __init__(self):
        self.__password = admins['password']
        self.__balance = 0
        with open('atm/atm.bin', 'wb') as f4:
            pickle.dump(self, f4)
            f4.close()

    def insert_card(self, card):
        with open('cards/num_card.txt', 'r') as f:
            len_cards = int(f.read())
        if not card.pin_check():
            return False
        for i in range(len_cards):
            with open('cards/card_{}.bin'.format(i), 'rb') as f3:
                card0 = pickle.load(f3)
                f3.close()
            if card.get_hashed_pin() == card0.get_hashed_pin():
                return i
        return False

    def start_trade(self, card):
        idx = self.insert_card(card)
        with open('cards/card_{}.bin'.format(idx), 'rb') as f3:
            card0 = pickle.load(f3)
            f3.close()
        account = card0.account
        while True:
            print(""" 
            ********
            Now you can start trade with your account.
            =============================================================
            1. See balance
            2. See history of transaction
            3. Deposit
            4. Withdraw
            5. End trade
            =============================================================
            """)
            selectnum = (input())
            if selectnum not in '12345':
                print("You input wrong character!")
                continue
            elif selectnum == '1':
                account.get_balance()
                continue
            elif selectnum == '2':
                account.get_history()
                continue
            elif selectnum == '3':
                print('How much do you want to deposit? :')
                try:
                    value = int(input())
                except:
                    print("You input wrong!")
                    continue
                if self.__balance >= value:
                    account.deposit(value)
                    with open('atm/atm.bin', 'wb') as f4:
                        pickle.dump(self, f4)
                        f4.close()
                    with open('cards/card_{}.bin'.format(idx), 'wb') as f3:
                        pickle.dump(card0, f3)
                        f3.close()
                    with open('user_card/card.bin', 'wb') as f2:
                        pickle.dump(card0, f2)
                        f2.close()
                else:
                    print("Sorry. We are not ready to deposit such amount.")
                continue
            elif selectnum == '4':
                print('How much do you want to withdraw? :')
                try:
                    value = int(input())
                except:
                    print("You input wrong!")
                    continue
                print('Input your password :')
                try:
                    password = int(input())
                except:
                    print("You input wrong!")
                    continue
                result = account.withdraw(value, password)
                if result:
                    self.__balance += value
                    with open('atm/atm.bin', 'wb') as f4:
                        pickle.dump(self, f4)
                        f4.close()
                    with open('cards/card_{}.bin'.format(idx), 'wb') as f3:
                        pickle.dump(card0, f3)
                        f3.close()
                    with open('user_card/card.bin', 'wb') as f2:
                        pickle.dump(card0, f2)
                        f2.close()
                continue
            else:
                idx = None
                card = card0 = None
                print("You should take your card!")
                break
            
    def verify_admin(self, password):
        if password == self.__password:
            return True
        return False

    def to_home(self):
        while True:
            print("""
            ********
            Hi.
            It is an ATM which helps you trade with your card.
            What do you want to do?
            =======================================================
            1. Start trade. (You need to prepare your own card.)
            2. Power off.
            3. Admin page.
            =======================================================
            """)
            select = input()
            if select not in '123':
                print("You input wrong!")
                continue
            elif select == '2':
                "See you later~"
                break
            elif select == '3':
                print("You need to input your password : ")
                try:
                    password = int(input())
                except:
                    print("You input wrong!")
                    continue
                if self.verify_admin(password):
                    self.to_admin()
                continue
            else:
                try:
                    with open('user_card/card.bin', 'rb') as f2:
                        card0 = pickle.load(f2)
                        f2.close()
                    self.start_trade(card0)
                except:
                    print("You did not take your card? Retry please.")
                    continue

    def to_admin(self):
        while True:
            print("""
            !!!!!!!!
            ADMIN PAGE.
            =======================================================
            1. See balance.
            2. Add money.
            3. Transfer money into inner safe.
            4. Exit.
            =======================================================
            """)
            select = input()
            if select not in '1234':
                print("You input wrong!")
                continue
            elif select == '1':
                print("Balance : ", self.__balance)
                continue
            elif select == '2':
                print("How much do you want to add? : ")
                try:
                    value = int(input())
                except:
                    print("You input wrong!")
                    continue
                self.add_balance(value)
                with open('atm/atm.bin', 'wb') as f4:
                    pickle.dump(self, f4)
                    f4.close()
                continue
            elif select == '3':
                print("How much do you want to transfer? : ")
                try:
                    value = int(input())
                except:
                    print("You input wrong!")
                    continue
                if self.__balance >= value:
                    self.minus_balance(value)
                    with open('atm/atm.bin', 'wb') as f4:
                        pickle.dump(self, f4)
                        f4.close()
                    continue
                print("Not enough money.")
                continue
            else:
                break

    def add_balance(self, value):
        self.__balance += value
    
    def minus_balance(self, value):
        self.__balance -= value

if __name__ == '__main__':
    atm0 = Atm()
    #with open('atm/atm.bin', 'rb') as f4:
    #    atm0 = pickle.load(f4)
    #    f4.close()
    atm0.add_balance(9999999999)
    with open('atm/atm.bin', 'wb') as f4:
        pickle.dump(atm0, f4)
        f4.close()