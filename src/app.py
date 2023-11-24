import json
from time import time
from hashlib import sha256
from flask import Flask, jsonify
import requests


class Blockchain():

    def __init__(self) -> None:

        self.chain = []
        self.new_transactions = []
        self.nodes = []
        self.new_block(1, "0")


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
        block_json = json.dumps(block, sort_keys=True)
        self.chain.append(block)
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

        block_content = json.dumps(block, sort_keys=True).encode()
        return sha256(block_content).hexdigest()
    


    def last_block(self):
        """Finds the last block"""
        return self.chain[-1]
    

    def hash_nonces(self, nonce, previous_nonce):
        """returns the hash of both nonces"""
        sum = str(nonce + previous_nonce)
        noth = sum.encode()
        return sha256(noth).hexdigest()
    


    def proof_of_work(self, previous_nonce):
        """Requires the hash of both nonces to begin with 4 0's"""
        nonce = 0
        difficulty = 3
        while self.hash_nonces(nonce, previous_nonce)[1] != "0":
            nonce += 1
        return nonce
    

    def valid_chain(self, chain):
        """Loop through chain, check validity based on hashes and POW"""
        for i in range(len(chain) - 1, 0, -1):
            if chain[i]["previous_hash"] != sha256(chain[i - 1]).hexdigest():
                return False
            elif self.hash_nonces(chain[i]["nonce"], chain[i - 1]["nonce"])[0:3] != "0000":
                return False
            else:
                return True
            

    def resolve_conflicts(self):
        """Replaces local chain with the longest chain on the network"""
        local_length = len(self.chain)
        for node in self.nodes:
            response = requests.get(f"{node}/chain")
            if response.status_code == "200":
                other_chain_length = response.json()["length"]
                other_chain = response.json()["chain"]
                if int(other_chain_length) > local_length:
                    self.chain = json.loads(other_chain)




# blockchain = Blockchain()

# blockchain.new_transaction("me", "you", "hello")

# blockchain.new_block(blockchain.proof_of_work(1), blockchain.hash_block(blockchain.last_block()))

# blockchain.new_transaction("alice", "bob", "open-secret")

# blockchain.new_block(60, "8a792b3269349f5ffa6d40e3c8a4232ff8282b117432de0eb95df5fb78e60818")

# print(blockchain.chain[1]["previous_hash"])






    




