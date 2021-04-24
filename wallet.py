import ecdsa
from transaction import to_hex,to_bytearray
import transaction
from typing import List
wallet_path = "./wallet/"

class wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None
    def init_wallet(self):
        sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.private_key = to_hex(sk.to_string())
        self.public_key = to_hex(sk.get_verifying_key())
        print("private key:"self.private_key)
        with open(wallet_path + "private_key.key","w") as f:
            f.write(self.private_key)
    def load_wallet(self,wallet_file):
        with open(wallet_file,"r") as f:
            h = f.read()
            self.private_key = h
            self.public_key = get_public_key(h)
    
    def get_balance(self,address,unspent_txout_lst:List[transaction.unspent_txout]):
        balance = 0
        for i in unspent_txout_lst:
            if i.address == address:
                balance += i.amount
        return balance
def get_public_key(private_key):
    return to_hex(ecdsa.SigningKey.from_string(to_bytearray(self.private_key)).to_string())
def create_transaction(receiver_address,amount,private_key,unspent_txout_lst,tx_pool):
    public_key = get_public_key(private_key)
    txout_lst = []
    for i in unspent_txout_lst:
        if i.address == public_key:
            txout_lst.append(i)

def filter_txpool(unspentTxOuts,transactionPool):
    txin_lst = 
