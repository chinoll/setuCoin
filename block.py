import hashlib
import time
import json
class Block:
    def __init__(self,index,timestamp,sha256,previous_hash,data):
        self.index = index
        self.sha256 = sha256
        self.previous_hash = previous_hash
        self.data = data
        self.timestamp = timestamp

current_milli_time = lambda: int(round(time.time() * 1000))
def calcSHA256(index,timestamp,previous_hash,data):
    print(timestamp)
    sha = hashlib.sha256()
    sha.update((str(index) + str(timestamp) + previous_hash + data).encode('utf-8'))
    return sha.hexdigest()
def generateNextBlock(data):
    index = len(block) + 1
    timestamp = current_milli_time()
    b = block[-1].sha256
    sha = calcSHA256(index,timestamp,b,data)
    return Block(index,timestamp,sha,b,data)