import json
from time import time
from hashlib import sha256


class Blockchain():

    def __init__(self) -> None:

        self.chain = []
        self.new_transactions = []
        self.nodes = []


    def new_block(self, nonce, previous_hash):
        """Structures all the relevant data into a block
        and appends to the chain as a JSON"""

        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "nonce": nonce,
            "previous_hash": previous_hash,
            "content": self.new_transactions

        }
        block_json = json.dumps(block)
        self.chain.append(block_json)
        # Clear new transactions list
        self.new_transactions = []


    
    def new_transaction(self, sender, recipient, message):
        """Structures the transaction data as a dictionary
        and appends to the new_transactions list"""

        transaction = {
            "sender": sender,
            "recipient": recipient,
            "message": message
        }
        self.new_transactions.append(transaction)
    


    def hash_block(self, block):
        """Hashes the contents of the block"""

        block_content = json.loads(block)
        return sha256(block_content).hexdigest()
    


    def last_block(self):
        """Finds the last block"""
        return self.chain[-1]
    

    def hash_nonces(self, nonce, previous_nonce):
        """returns the hash of both nonces"""
        sum = nonce + previous_nonce
        return sha256(sum).hexdigest()
    


    def proof_of_work(self, previous_nonce):
        """Requires the hash of both nonces to begin with 4 0's"""
        nonce = 0
        while self.hash_nonces(nonce, previous_nonce)[0:3] != "0000":
            nonce += 1
        return nonce
    

    def valid_chain(self, chain):
        """Loop through chain, check validity based on hashes and POW"""
        for i in range(len(chain), 0, -1):
            if chain[i]["previous_hash"] != sha256(chain[i - 1]).hexdigest():
                return False
            elif self.hash_nonces(chain[i]["nonce"], chain[i - 1]["nonce"])[0:3] != "0000":
                return False
            else:
                return True
            

    def resolve_conflicts(self):
        """Replaces local chain with the longest chain on the network"""
        #for node in self.nodes:






    




