from hashlib import sha256


def update_hash(*args):
    hashed_text = ""
    hashing = sha256()

    for arg in args:
        hashed_text += str(arg)

    hashing.update(hashed_text.encode('utf-8'))
    return hashing.hexdigest()


class Block:
    def __init__(self, data=None, previous_hash='0'*64, nonce=0):
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce

    def hash(self):
        return update_hash(self.previous_hash, self.data, self.nonce)

    def __str__(self):
        return str(f"Hash: {self.hash()}\nPrevious hash: {self.previous_hash}\nData: {self.data}\nNonce: {self.nonce}")


class Blockchain:
    difficulty = 5

    def __init__(self):
        self.chain = []

    def add(self, block):
        self.chain.append(block)

    def remove(self, block):
        index = self.chain.index(block)

        if index < len(self.chain) - 1:
            self.chain[index + 1].previous_hash = block.previous_hash

        self.chain.remove(block)

    def mine(self, block):
        try:
            block.previous_hash = self.chain[-1].hash()
        except IndexError:
            pass

        while True:
            if block.hash()[:self.difficulty] == "0" * self.difficulty:
                self.add(block)
                break
            else:
                block.nonce += 1

    def check_valid(self):
        chain_len = len(self.chain)
        difficulty_char = "0" * self.difficulty

        for i in range(1, chain_len):
            _prev = self.chain[i].previous_hash
            _cur = self.chain[i - 1].hash()

            if _prev != _cur or _cur[:self.difficulty] != difficulty_char:
                return False

        return True
