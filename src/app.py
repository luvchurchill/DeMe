import hashlib
import time



class Block():

    def __init__(self, index, data_in, nonce, hash, prev_hash="ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb"):
        self.prev_hash = prev_hash
        self.index = index
        self.data_in = data_in
        self.nonce = nonce
        self.hash = hash
        self.time = time.time()

    
    def curr_block(self, index, data_in):
        pass

    
    def get_hash(self):
        return shash

    
    
    def mine(self, difficulty):
        """Will increment nonce untill it finds a hash that begins with (1 * difficulty) zeros"""
        first_digits = "0" * difficulty

        shash = 0
        
        while True:
            hashstr = str(shash)
            if hashstr[0:difficulty] == first_digits:
                break
            else:
                self.nonce += 1
                shash = self.calc_hash()

        print(f"Block Mined {shash} ")


    def calc_hash(self):
        """ Returns hash of all the values added together"""
        strung = str(self.index + self.time + self.data_in + self.nonce) + self.prev_hash
        the_hash = hashlib.sha256()
        encoded = strung.encode()
        the_hash.update(encoded)
        hashed = the_hash.hexdigest()
        return hashed



myblock = Block(2, 5, 1, 3)

mined = myblock.mine(2)

print(mined)