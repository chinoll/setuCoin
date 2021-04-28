import ecdsa
from ecdsa import SigningKey
from transaction import to_hex,to_bytearray
import transaction
from typing import List
wallet_path = "./wallet/"
import os

class wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None
    def init_wallet(self):
        sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.private_key = to_hex(sk.to_string())
        self.public_key = to_hex(sk.get_verifying_key().to_string())
        print("private key:",self.private_key)
        if not os.path.exists(wallet_path):
            os.mkdir(wallet_path)
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
    b = to_bytearray(private_key)
    return to_hex(ecdsa.SigningKey.from_string(b,curve=ecdsa.SECP256k1).to_string())

def create_transaction(receiver_address,amount,private_key,unspent_txout_lst,tx_pool):
    public_key = get_public_key(private_key)
    txout_lst = []
    for i in unspent_txout_lst:
        if i.address == public_key:
            txout_lst.append(i)

    include_unspent_txouts,left_over_amount = find_txout_for_amount(amount,txout_lst)
    unsigned_txins = []
    for i in include_unspent_txouts:
        txin = transaction.TxInput()
        txin.txout_id = i.txout_id
        txin.tx_out_index = i.txout_index
    tx = transaction.transaction(unsigned_txins,create_txouts(receiver_address,public_key,amount,left_over_amount))
    for i in range(tx.tx_ins):
        tx.tx_ins[i].signature = tx.sign_txin(i,private_key,unspent_txout_lst)
    return tx

def find_txout_for_amount(amount,unspent_txout_lst: List[transaction.unspent_txout]):
    current_amount = 0

    include_unspent_txouts = []
    for i in unspent_txout_lst:
        include_unspent_txouts.append(i)
        current_amount += i.amount

        if current_amount >= amount:
            left_over_amount = current_amount - amount
            return include_unspent_txouts,left_over_amount
    print("Error: not enough coins to send transaction")

def to_unsigned_txin(unspent_txout):
    return transaction.TxInput(unspent_txout.txout_id,unspent_txout.tx_out_index,"")

def create_txouts(recv_address,my_address,amount,left_over_amount):
    txout = transaction.Txoutput(recv_address,amount)
    if left_over_amount == 0:
        return [txout]
    else:
        left_over_tx = transaction.Txoutput(my_address,left_over_amount)
        return [txout,left_over_tx]
