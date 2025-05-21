# blockchain.py

import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(data="Genesis Block", hash_of_file="N/A")

    def create_block(self, data, hash_of_file):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'data': data,
            'hash_of_file': hash_of_file,
            'previous_hash': self.chain[-1]['hash'] if self.chain else '0'
        }
        block['hash'] = self.hash_block(block)
        self.chain.append(block)
        return block

    def hash_block(self, block):
        block_copy = block.copy()
        block_copy.pop('hash', None)
        encoded = json.dumps(block_copy, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()

    def is_file_registered(self, file_hash):
        return any(block['hash_of_file'] == file_hash for block in self.chain)

    def get_chain(self):
        return self.chain
