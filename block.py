import hashlib as hl

class Block():
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hashing()

    def hash(self):
        self.key = hashlib.sha256()
        self.key.update(str(self.index).encode('utf-8'))
        self.key.update(str(self.timestamp).encode('utf-8'))
        self.key.update(str(self.data).encode('utf-8'))
        self.key.update(str(self.previous_hash).encode('utf-8'))
        return self.key.hexdigest()

class Chain():
    def __init__(self):
        self.blocks = []

    def create_gen_block(self):
        return Block(0, datetime.datetime.utcnow(), 'BlockCondom', 'arbitrary')

    def add_block(self, data):
        self.blocks.append( Block(
                            len(self.blocks), 
                            datetime.datetime.utcnow(), 
                            data, 
                            self.blocks[-1].hash) )

    def chain_length(self):
        return self.block - 1 # exclude genesis block

    def verify(self, verbose=True): 
        flag = True
        for i in range(1,len(self.blocks)):
            if self.blocks[i].index != i:
                flag = False
                if verbose:
                    print(f'Wrong block index at block {i}.')
            if self.blocks[i-1].hash != self.blocks[i].previous_hash:
                flag = False
                if verbose:
                    print(f'Wrong previous hash at block {i}.')
            if self.blocks[i].hash != self.blocks[i].hashing():
                flag = False
                if verbose:
                    print(f'Wrong hash at block {i}.')
            if self.blocks[i-1].timestamp >= self.blocks[i].timestamp:
                flag = False
                if verbose:
                    print(f'Backdating at block {i}.')
        return flag

    def search(self, userid):
        for block in self.blocks:
            temp = []
            if block.data.sender-id == userid or block.data.recipient-id == userid:
                temp.append(block)
        return temp