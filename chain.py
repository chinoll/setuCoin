import block
import json

class Chain:
    def __init__(self,db_path=None,chain=""):
        db = None
        if db_path is None:
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

    def isValidBlock(self,block,prev_block):
        if block.index + 1 != prev_block.index:
            print("invalid index")
            return False
        elif prev_block.sha256 != block.previous_hash:
            print("invalid previous hash")
            return False
        elif calcSHA256(bloc.index,block.timestamp,block.previous_hash,block.data) != block.sha256:
            print("invalid block!")
            return False
        return True
    def addBlock(self,block):
        if isValidBlock(block,self.chain[-1]):
            self.chain.append(block)

    def isValidBlockStruct(self,block):
        return type(block.index) == int and type(block.sha256) == str and type(block.previous_hash) == str and type(block.data) == str and type(block.timestamp) == int

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