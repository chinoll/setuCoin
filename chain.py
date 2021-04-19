import block
import json

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
            temp.append(block.Block(i["index"],i["timestamp"],i["sha256"],i["previous_hash"],i["data"]))
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
        elif block.calcSHA256(_block.index,_block.timestamp,_block.previous_hash,_block.data) != _block.sha256:
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

    def generateNextBlock(self,data):
        index = len(self.chain)
        timestamp = block.current_milli_time()
        b = self.chain[-1].sha256
        sha = block.calcSHA256(index,timestamp,b,data)
        b = block.Block(index,timestamp,sha,b,data)
        self.chain.append(b)