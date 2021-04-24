import block
import json
import time
import transaction
import wallet
class Chain:
    def __init__(self,db_path=None,chain=""):
        db = None
        if not db_path is None:
            with open(db_path) as e:
                db = json.loads(e.read())
        else:
            db = json.loads(chain)

        temp = []
        for i in db:
            temp.append(block.Block(i["index"],i["timestamp"],i["sha256"],i["previous_hash"],i["data"],i["difficulty"],i["nonce"]))
        if self.isValidChain(temp):
            self.chain = temp
    def __str__(self):
        l = [d.__dict__ for d in self.chain]
        return json.dumps(l,sort_keys=True, indent=4, separators=(',', ':'),ensure_ascii=False)

    def isValidBlock(self,_block,prev_block):
        if _block.index != prev_block.index + 1:
            print("invalid index")
            return False
        elif prev_block.sha256 != _block.previous_hash:
            print("invalid previous hash")
            return False
        elif block.calcSHA256(_block.index,_block.timestamp,_block.previous_hash,_block.data,_block.difficulty,_block.nonce) != _block.sha256 and not self.hashMatchesDifficulty(_block.sha256,_block.difficulty):
            print("invalid block!")
            return False
        return True

    def addBlock(self,_block):
        if isValidBlock(_block,self.chain[-1]):
            self.chain.append(_block)

    def isValidBlockStruct(self,_block):
        return type(_block.index) == int and type(_block.sha256) == str and type(_block.previous_hash) == str and type(_block.data) == str and type(block.timestamp) == int

    def isValidChain(self,chain):
        for i in range(1,len(chain[1:])):
            if not self.isValidBlock(chain[i],chain[i - 1]):
                return False
        return True

    def replaceChain(self,newBlock):
        if self.isValidChain(newBlock) and len(newBlock) > len(self.chain):
            self.chain = newBlock
        else:
            print("Received blockchain invalid")
            return False
        return True

    def generateNextBlock(self):
        #wallet = wallet.wallet()
        #wallet.load_wallet("wallet/private_key.key")
        #coinbase_tx = transaction.get_coinbase_transaction(wallet.public_key,len(self.chain))
        self.generateRawNextBlock("")
    def generatenextBlockWithTransaction(self,address,amount):
        if not transaction.is_valid_address(address):
            print('invalid address')
            return
        if type(amount) != int:
            print("invalid amount")
            return
        coinbaseTx = transaction.get_coinbase_transaction(address,len(self.chain))
        tx = 
    def generateRawNextBlock(self,data):
        index = len(self.chain)
        timestamp = block.current_milli_time()
        latestBlock_hash = self.chain[-1].sha256
        nonce = 0
        difficulty = self.getDifficuly()
        while True:
            hash = block.calcSHA256(index,timestamp,latestBlock_hash,data,difficulty,nonce)
            if not self.hashMatchesDifficulty(hash,difficulty):
                nonce += 1
            else:
                self.chain.append(block.Block(index,timestamp,hash,latestBlock_hash,data,difficulty,nonce))
                return
    def getDifficuly(self):
        latestBlock = self.chain[-1]
        if latestBlock.index % block.DIFFICULTY_ADJUSTMENT_INTERVAL == 0 and latestBlock.index != 0:
            return self.getAdjustedDifficulty(latestBlock)
        else:
            return latestBlock.difficulty

    def getAdjustedDifficulty(self,latestBlock):
        #难易度调整
        prevAdjustmentBlock = self.chain[len(self.chain) - block.DIFFICULTY_ADJUSTMENT_INTERVAL]
        time_excepted = block.BLOCK_GENERATION_INTERVAL * block.DIFFICULTY_ADJUSTMENT_INTERVAL
        time_taken = int(str(latestBlock.timestamp)[:10]) - int(str(prevAdjustmentBlock.timestamp)[:10])
        if time_taken < time_excepted / 2:
            return prevAdjustmentBlock.difficulty + 1
        elif time_taken > time_excepted * 2:
            return prevAdjustmentBlock.difficulty - 1
        else:
            return prevAdjustmentBlock.difficulty
    
    def isValidTimestamp(self,mewblock,prevblock):
        return newblock.timestamp - 60 < int(time.time()) and prevblock.timestamp - 60 < newblock.timestamp

    def hashMatchesDifficulty(self,hash,difficulty):
        x = bin(int(hash,16))[2:]
        zero_prefix = "1"*difficulty
        return x.startswith(zero_prefix)
