import hashlib
import time
import json
class Block:
    def __init__(self,index,timestamp,sha256,previous_hash,data,difficulty,nonce):
        self.index = index
        self.sha256 = sha256
        self.previous_hash = previous_hash
        self.data = data
        self.timestamp = timestamp
        self.difficulty = difficulty
        self.nonce = nonce

current_milli_time = lambda: int(round(time.time() * 1000))

def calcSHA256(index:int,timestamp:int,previous_hash:str,data:str,difficulty:int,nonce:int) -> str:
    sha = hashlib.sha256()
    sha.update((str(index) + str(timestamp) + previous_hash + data + str(difficulty) + str(nonce)).encode('utf-8'))
    return sha.hexdigest()

#60s出块
BLOCK_GENERATION_INTERVAL = 60

#难易度
DIFFICULTY_ADJUSTMENT_INTERVAL = 10

