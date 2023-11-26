import json
from time import time
from hashlib import sha256
from flask import Flask, jsonify, request
import requests


class Blockchain:
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
            "content": self.new_transactions,
        }
        block_json = json.dumps(block, sort_keys=True)
        self.chain.append(block_json)
        # Clear new transactions list
        self.new_transactions = []

    def new_transaction(self, sender, recipient, message):
        """Structures the transaction data as a dictionary
        and appends to the new_transactions list"""

        transaction = {"sender": sender, "recipient": recipient, "message": message}
        self.new_transactions.append(transaction)

    def hash_block(self, block):
        """Hashes the contents of the block"""

        block_content = json.dumps(block, sort_keys=True).encode()
        return sha256(block_content).hexdigest()

    def last_block(self):
        """Finds the last block"""
        return self.chain[-1]

    def hash_nonces(self, nonce, previous_nonce, timestamp):
        """returns the hash of both nonces"""
        sum = str(nonce + previous_nonce + timestamp)
        encoded = sum.encode()
        return sha256(encoded).hexdigest()

    def proof_of_work(self, previous_nonce, timestamp):
        """Requires the hash of both nonces to begin with 4 0's"""
        nonce = 0
        difficulty = 3
        while self.hash_nonces(nonce, previous_nonce, timestamp)[1] != "0":
            nonce += 1
        return nonce

    def valid_chain(self, chain):
        """Loop through chain, check validity based on hashes and POW"""
        for i in range(len(chain) - 1, 0, -1):
            block = json.loads(chain[i])
            previous_block = chain[i - 1]
            if block["previous_hash"] != self.hash_block(previous_block):
                return False
            elif (
                self.hash_nonces(block["nonce"], json.loads(previous_block)["nonce"], json.loads(previous_block)["timestamp"])[1]
                != "0"
            ):
                return False
            else:
                return True

    def resolve_conflicts(self):
        """Replaces local chain with the longest chain on the network"""
        local_length = len(self.chain)
        if not self.nodes:
            return False
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

# blockchain.new_block(blockchain.proof_of_work(json.loads(blockchain.last_block())["nonce"]), blockchain.hash_block(blockchain.last_block()))

# print(blockchain.valid_chain(blockchain.chain))

# out = True

app = Flask(__name__)

bc = Blockchain()
this_node = 1


@app.route("/mine")
def mining():
    bc.resolve_conflicts()
    previous_nonce = json.loads(bc.last_block())["nonce"]
    previous_hash = bc.hash_block(bc.last_block())
    previous_time = json.loads(bc.last_block())["timestamp"]
    pow = bc.proof_of_work(previous_nonce, previous_time)
    bc.new_transaction(0, this_node, f"block mined by {this_node}")
    bc.new_block(pow, previous_hash)
    mined_block = bc.chain[-1]
    return jsonify(mined_block)


@app.route("/valid")
def validate():
    is_it = bc.valid_chain(bc.chain)
    return jsonify(is_it)

@app.route("/chain")
def get_chain():
    return jsonify(bc.chain)

@app.route("/new", methods = ["POST"])
def new_transaction():
    submitted = request.get_json()
    bc.new_transaction(content["sender"], content["recipient"], content["message"])
    return jsonify(bc.new_transactions)






app.run("0.0.0.0", debug=True)

    
    
