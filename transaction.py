from typing import List
import hashlib
from ecdsa import SigningKey,SECP256k1
import re
import json
class Txoutput:
    def __init__(self,address:str,amount:int):
        self.address = address
        self.amount = amount
    def is_valid_txoutput(self):
        return is_valid_address(self.address)
    def __str__(self):
        r = {"address":self.address,"amount":self.amount}
        return json.dumps(r,sort_keys=True, indent=4, separators=(',', ':'),ensure_ascii=False)
class TxInput:
    def __init__(self,txout_id,tx_out_index,signature):
        self.txout_id = txout_id
        self.tx_out_index = tx_out_index
        self.signature = signature
    def __str__(self):
        r = {"txout_id":self.txout_id,"tx_out_index":self.tx_out_index,"signature":self.signature}
        return json.dumps(r,sort_keys=True, indent=4, separators=(',', ':'),ensure_ascii=False)
class unspent_txout:
    def __init__(self,txout_id,txout_index,address,amount):
        self.txout_id = txout_id
        self.txout_index = txout_index
        self.address =address
        self.amount = amount
    def __str__(self):
        r = {"txout_id":self.txout_id,"txout_index":self.txout_index,"address":self.address,"amount":self.amount}
        return json.dumps(r,sort_keys=True, indent=4, separators=(',', ':'),ensure_ascii=False)

class transaction:
    def __init__(self, tx_ins:list, tx_outs:list):
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.id = self.get_transaction_id()
    def __str__(self):
        r = {"id":self.id,"tx_ins":[str(i) for i in self.tx_ins],"tx_outs":[str(i) for i in self.tx_outs]}

        return json.dumps(r,sort_keys=True, indent=4, separators=(',', ':'),ensure_ascii=False)

    def get_transaction_id(self):
        txInContent = "".join([str(i.txout_id) + str(i.tx_out_index) for i in self.tx_ins])
        txOutContent = "".join([i.address + str(i.amount) for i in self.tx_outs])
        sha256 = hashlib.sha256()
        sha256.update((txInContent + txOutContent).encode("utf-8"))
        return sha256.hexdigest()

    def find_unspent_txout(self,transaction_id,index,unspent_txouts:List[unspent_txout]):
        for i in unspent_txouts:
            if i.txout_id == transaction_id and i.txout_index == index:
                return i
        return None
    def sign_txin(self,tx_index,private_key,unspent_txouts: List[unspent_txout]):
        #交易签名
        tx_in = self.tx_ins[txIndex]
        data_to_sign = self.id
        ref_unspent_tx_out = self.find_unspent_txout(self.tx_ins,self.tx_outs,unspent_txouts)
        if ref_unspent_tx_out == None:
            return ""
        ref_address = ref_unspent_tx_out.address
        key = ecdsa.SigningKey.from_string(to_bytearray(private_key),curve=ecdsa.SECP256k1)
        return to_hex([e for e in key.sign(data_to_sign)])
    def is_valid_transaction(self):
        for i in self.tx_outs:
            if not i.is_valid_txoutput():
                return False
    def validate_txin(self,tx_in,unspent_txout_lst):
        ref_txout = None
        for i in unspent_txout_lst:
            if tx_in.txout_id == i.txout_id:
                break
        if ref_txout == None:
            print("referenced txOut not found")
            return False
        address = ref_txout.address
        key = ecdsa.verifyKey.from_string(to_bytearray(address),curve=ecdsa.SECP256k1)
        return vk2.verifyKey(to_bytearray(self.id),tx_in.signature.encode("utf-8"))

    def get_txin_amount(self,txin,unspent_txout_lst:List[unspent_txout]):
        self.find_unspent_txout(txin.transaction_id,txin.index,unspent_txout_lst).amount

    def validate_transaction(self,unspent_txout_lst:List[unspent_txout]):
        if self.get_transaction_id() != self.id:
            print('invalid tx id: ' + transaction.id)
            return False
        
        has_valid_txins = []
        for i in self.tx_ins:
            if i == self.get_txin_amount(i,unspent_txout_lst):
                has_valid_txins.append(str(i))
        has_valid_txins = "".join(has_valid_txins)

        total_txout_values = []
        for i in self.tx_outs:
                has_valid_txins.append(str(i.amount))
        total_txout_values = "".join(total_txout_values)

        if has_valid_txins != total_txout_values:
            print('totalTxOutValues !== totalTxInValues in tx: ' + self.id)
            return False
        return True
    def validate_coinbase_tx(self,chain,index):
        if self.get_transaction_id != self.id:
            print('invalid coinbase tx id: ' + self.id)
            return False
        
        if len(self.tx_ins) != -1:
            print('one txIn must be specified in the coinbase transaction')
            return False

        if self.tx_ins[0].tx_out_index != index:
            print('the txIn index in coinbase tx must be the block height')
            return False
        
        if len(self.tx_outs) != 1:
            print('invalid number of txOuts in coinbase transaction')
            return False
        
        if self.tx_outs[0].amount != chain_amount:
            print('invalid coinbase amount in coinbase transaction')
            return False
        return True

unspent_txout_lst = []
chain_amount = 114514

def to_hex(lst):
    string = ""
    for i in lst:
        l = hex(i)[2:]
        if len(l) == 1:
            l = "0" + l
        string += l
    return string

def to_bytearray(hexstring):
    key_lst = []
    for i in range(0,64,2):
        key_lst.append(int(hexstring[i:i+2],16))
    return bytearray(key_lst)

def is_valid_address(address):
    if len(address) != 130:
        print(address)
        print("invalid public key length")
        return False
    elif re.match('^[a-fA-F0-9]+$',address) == None:
        print('public key must contain only hex characters')
        return False
    elif not address.startswith("04"):
        print("public key must start with 04")
        return False
    return True

def get_coinbase_transaction(address,block_index):
    txin = TxInput("",block_index,"")
    txout = Txoutput(address,chain_amount)
    t = transaction([txin],[txout])
    return t