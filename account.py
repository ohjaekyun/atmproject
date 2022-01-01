import random
from datetime import date, datetime, timedelta
from config import hashs
import hashlib
import pickle

def get_hash(nums, keys, mod):
    num_sum = 0
    for num, key in zip(nums, keys):
        num_sum += num * key
    return num_sum % mod

def get_account_num():
    base = '89'
    nums = []
    for i in range(8):
        num = random.randint(0, 9)
        nums.append(num)
        base = ''.join([base, str(num)])
    hash1 = get_hash(nums, hashs['account'][0], 10)
    hash2 = get_hash(nums, hashs['account'][1], 10)
    hash3 = get_hash(nums, hashs['account'][2], 10)
    base = ''.join([base, str(hash1), str(hash2), str(hash3)])
    return base

def get_pin_num():
    first_num = random.randint(1, 9)
    base = str(first_num)
    nums = [first_num]
    for i in range(11):
        num = random.randint(0, 9)
        nums.append(num)
        base = ''.join([base, str(num)])
    hash1 = get_hash(nums, hashs['card'][0], 10)
    hash2 = get_hash(nums, hashs['card'][1], 10)
    base = ''.join([base, str(hash1), str(hash2)])
    for i in range(2):
        num = random.randint(0, 9)
        base = ''.join([base, str(num)])
    return base

class Account:
    def __init__(self, accountnum, password, money = 0):
        self.accountnum = accountnum
        #self.card = None
        self.__balance = 0
        self.history = []
        self.__password = None
        self.init_deposit(money)

    def init_deposit(self, value):
        self.__balance += value
        now = datetime.now().strftime("%y%m%d %H:%M:%S")
        self.history.append(['Deposit', now, value, self.__balance])
        print("[Init] Time : {}, Change : {}, Balance : {}".format(now, value, self.__balance))

    def set_password(self, password):
        encoded = str(password).encode()
        self.__password = hashlib.sha256(encoded).hexdigest()

    def verify_password(self, password):
        if self.__password == hashlib.sha256(str(password).encode()).hexdigest():
            return True
        else:
            print('Wrong password!')
            return False

    def get_balance(self):
        print(self.__balance)
        return self.__balance

    def get_history(self):
        for trans in self.history:
            print("[{}] Time : {}, Change : {}, Balance : {}".format(trans[0], trans[1], trans[2], trans[3]))
        return self.history

    def deposit(self, value):
        self.__balance += value
        now = datetime.now().strftime("%y%m%d %H:%M:%S")
        self.history.append(['Deposit', now, value, self.__balance])
        print("[Deposit] Time : {}, Change : {}, Balance : {}".format(now, value, self.__balance))

    def withdraw(self, value, password):
        if value <= self.__balance:
            if self.verify_password(password):
                self.__balance -= value
                now = datetime.now().strftime("%y%m%d %H:%M:%S")
                self.history.append(['Withdraw', now, -value, self.__balance])
                print("[Withdraw] Time : {}, Change : {}, Balance : {}".format(now, -value, self.__balance))
                return True
            else:
                return False
        else:
            print('Not enough money.')
            return False

class Card:
    def __init__(self):
        self.__PIN = None
        self.account = None

    def set_pin(self, value):
        self.__PIN = value

    def pin_check(self):
        nums = []
        for i, char in enumerate(self.__PIN):
            if i == 12:
                num1 = int(char)
            elif i == 13:
                num2 = int(char)
                break
            nums.append(int(char))
        if num1 == get_hash(nums, hashs['card'][0], 10) and num2== get_hash(nums, hashs['card'][1], 10):
            return True
        print("Invalid PIN number!")
        return False

    def pin_equal(self, value):
        if self.__PIN == value:
            return True
        else:
            return False
            
def make_account_with_card(password, money):
    account = Account(get_account_num(), password, money = money)
    card = Card()
    card.set_pin(get_pin_num())
    #account.card = card
    card.account = account
    with open('cards/num_card.txt', 'r') as f:
        len_cards = int(f.read())
    with open('cards/num_card.txt', 'w') as f2:
        f2.write(str(len_cards + 1))
    with open('cards/card_{}.bin'.format(len_cards), 'wb') as f3:
        pickle.dump(card, f3)

def verify_account(account):
    accountnum = account.accountnum
    if accountnum[0] == '8' and accountnum[1] == '9':
        nums = []
        for char in accountnum[2:10]:
            nums.append(int(char))
        if int(accountnum[10]) == get_hash(nums, hashs['account'][0], 10) and int(accountnum[11]) == get_hash(nums, hashs['account'][1], 10) and int(accountnum[12]) == get_hash(nums, hashs['account'][2], 10):
            return True
        else:
            print("Invalid account number!")
            return False
    else:
        print("Invalid account number!")
        return False

if __name__ == '__main__':
    with open('cards/card_{}.bin'.format(0), 'rb') as f3:
        car = pickle.load(f3)
    print(car.account.accountnum)
    print(verify_account(car.account))
    print(car.pin_check())
    #make_account_with_card(1234, 1000)
