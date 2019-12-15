import hashlib as hl
import pickle as pkl
import datetime
import binascii

class Block():
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hashing()


    def hashing(self):
        key = hl.sha256()
        key.update(str(self.index).encode('utf-8'))
        key.update(str(self.timestamp).encode('utf-8'))
        key.update(str(self.data).encode('utf-8'))
        key.update(str(self.previous_hash).encode('utf-8'))
        return key.hexdigest()


class Chain():
    def __init__(self):
        with open('chain.pkl', 'rb') as r:
            try:
                self.blocks = pkl.load(r)
            except EOFError:
                self.blocks = [self.create_gen_block()]
                with open('chain.pkl', 'wb') as w:
                    pkl.dump(self.blocks, w)


    def create_gen_block(self):
        return Block(0, datetime.datetime.utcnow(), {"sender-email": None}, 'arbitrary')


    def add_block(self, d):
        self.blocks.append( Block(
                            len(self.blocks), 
                            datetime.datetime.utcnow(), 
                            d, 
                            self.blocks[-1].hash) )
        with open('chain.pkl', 'wb') as w:                    
            pkl.dump(self.blocks, w)

    
    def prune(self, idx):
        # Chop off all blocks after a fraudulent block.
        self.blocks = self.blocks[:idx]
        with open("chain.pkl", "wb") as w:
            pkl.dump(self.blocks, w)


    def chain_length(self):
        return len(self.blocks) - 1 # exclude genesis block


    def verify(self, verbose=True): 
        flag = True
        idx = None
        for i in range(1,len(self.blocks)):
            if self.blocks[i].index != i:
                flag = False
                idx = i
                if verbose:
                    print(f'Wrong block index at block {i}.')
            if self.blocks[i-1].hash != self.blocks[i].previous_hash:
                flag = False
                idx = i
                if verbose:
                    print(f'Wrong previous hash at block {i}.')
            if self.blocks[i].hash != self.blocks[i].hashing():
                flag = False
                idx = i
                if verbose:
                    print(f'Wrong hash at block {i}.')
            if self.blocks[i-1].timestamp >= self.blocks[i].timestamp:
                flag = False
                idx = i
                if verbose:
                    print(f'Backdating at block {i}.')
        return flag, idx


    def search(self, userid):
        for block in self.blocks:
            temp = []
            if block.data["sender-email"] == userid:
                temp.append(block)
        return temp
    

    def get_last_transaction(self, user_email):
        for i in range(len(self.blocks) - 1, -1, -1):
            if self.blocks[i].data["sender-email"] == user_email:
                return self.blocks[i]
        else:
            return None
