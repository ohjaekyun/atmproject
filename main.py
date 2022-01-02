import pickle
from account import *
from atm import *
if __name__ == '__main__':
    with open('atm/atm.bin', 'rb') as f4:
        atm0 = pickle.load(f4)
        f4.close()
    atm0.to_home()