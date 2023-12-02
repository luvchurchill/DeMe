"""DeMe decenteralized messaging using Blockchain
Copyright (C) 2023  https://github.com/luvchurchill

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>."""

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
        #block_json = json.dumps(block, sort_keys=True)
        self.chain.append(block)
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

    def hash_nonces(self, nonce, previous_nonce, timestamp, previous_hash):
        """returns the hash of all the data"""
        sum = str(nonce + previous_nonce + timestamp) + previous_hash
        encoded = sum.encode()
        return sha256(encoded).hexdigest()

    def proof_of_work(self, previous_nonce, timestamp, previous_hash):
        """Requires the hash of the data to begin with 4 0's"""
        nonce = 0
        while (
            self.hash_nonces(nonce, previous_nonce, timestamp, previous_hash)[0:4]
            != "0000"
        ):
            nonce += 1
        return nonce

    def valid_chain(self, chain):
        """Loop through chain, check validity based on hashes and pow"""
        # Loops from end to beginning
        for i in range(len(chain) - 1, 0, -1):
            block = chain[i]
            previous_block = chain[i - 1]
            if block["previous_hash"] != self.hash_block(previous_block):
                return False
            elif (
                self.hash_nonces(
                    block["nonce"],
                    previous_block["nonce"],
                    previous_block["timestamp"],
                    self.hash_block(previous_block),
                )[0:4]
                != "0000"
            ):
                return False
            else:
                return True

    def resolve_conflicts(self):
        """Replaces local chain with the longest chain on the network"""
        # Will probably need to add a try/except block
        local_length = len(self.chain)
        if not self.nodes:
            return False
        for node in self.nodes:
            response = requests.get(f"http://{node}/chain")
            if response.status_code == "200":
                other_chain_length = response.json()["length"]
                other_chain = response.json()["chain"]
                if int(other_chain_length) > local_length:
                    self.chain = json.loads(other_chain)


app = Flask(__name__)

bc = Blockchain()
this_node = 1


@app.route("/mine")
def mining():
    """Endpoint for mining new blocks"""
    #bc.resolve_conflicts()
    previous_data = bc.last_block()
    previous_nonce, previous_time = previous_data["nonce"], previous_data["timestamp"]
    previous_hash = bc.hash_block(bc.last_block())
    pow = bc.proof_of_work(previous_nonce, previous_time, previous_hash)
    bc.new_transaction(0, this_node, f"block mined by {this_node}")
    bc.new_block(pow, previous_hash)
    mined_block = bc.chain[-1]
    return jsonify(mined_block)


@app.route("/valid")
def validate():
    """Endpoint to validate the chain based on checks in Blockchain.valid_chain"""
    validity = bc.valid_chain(bc.chain)
    return jsonify(validity)


@app.route("/chain")
def get_chain():
    """returns the full chain"""
    return jsonify(bc.chain)


@app.route("/new", methods=["POST"])
def new_transaction():
    """Packages new Tx into new block and appends to chain"""
    submitted = request.get_json()
    content = json.loads(submitted)
    bc.new_transaction(content["sender"], content["recipient"], content["message"])
    previous_data = bc.last_block()
    previous_nonce, previous_time = previous_data["nonce"], previous_data["timestamp"]
    previous_hash = bc.hash_block(bc.last_block())
    pow = bc.proof_of_work(previous_nonce, previous_time, previous_hash)
    bc.new_block(pow, previous_hash)
    return jsonify(bc.chain[-1])


@app.route("/register", methods=["POST"])
def register():
    """Registers new nodes and returns list of known nodes"""
    nodes = request.get_json()
    new_node = nodes["new_node"]
    bc.nodes.append(new_node)
    return bc.nodes


@app.route("/update")
def update_chain():
    """Updates local chain to the longest valid chain on the network"""


app.run("0.0.0.0", debug=True)
