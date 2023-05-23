from hashlib import sha256


class Block:
    def __init__(self, data=None, previous_hash='0'*64, nonce=0):
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce

    def hash(self):
        hashed_data = f'{self.previous_hash}{self.data}{self.nonce}'
        sha256().update(hashed_data.encode('utf-8'))

        return sha256().hexdigest()

    def __str__(self):
        return str(f'Data: {self.data}\nHash: {self.hash()}\nPrevious hash: {self.previous_hash}\nNonce: {self.nonce}')


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

    def check_validity(self):
        for i in range(1, len(self.chain)):
            previous = self.chain[i].previous_hash
            current = self.chain[i - 1].hash()

            if previous != current or current[:self.difficulty] != "0" * self.difficulty:
                return False

        return True
