import hashlib
import time
import json
from numba import jit
class Block:
    def __init__(self,index,timestamp,sha256,previous_hash,data):
        self.index = index
        self.sha256 = sha256
        self.previous_hash = previous_hash
        self.data = data
        self.timestamp = timestamp

current_milli_time = lambda: int(round(time.time() * 1000))

@jit()
def calcSHA256(index:int,timestamp:int,previous_hash:str,data:str) -> str:
    sha = hashlib.sha256()
    sha.update((str(index) + str(timestamp) + previous_hash + data).encode('utf-8'))
    return sha.hexdigest()