import hashlib
import json


class Ledger(object):
    def __init__(self, blockchain_file=None, func=None):
        self.values = {}
        self.blockchain = []
        self.blockchain_file = blockchain_file
        self.func = flow if func is None else func
        if self.blockchain_file is not None:
            self.load_blockchain_file(blockchain_file)


    def load_blockchain(self, blockchain):
        """
        Validate the existing blockchain, then load it
        """
        for new_block in blockchain:
            block = Block(self.current_block,
                         new_block["key"],
                         new_block["input"],
                         new_block["value"])

            if new_block["hash"] != block.hash:
                raise ChainException("The bloackchain hash is bad or corrupt: \
                        \nblock hash: {}".format(new_block["hash"]))

            self.blockchain.append(block)

            self.values[block.key] = block.value

        print "Blockchain loaded and validated"


    def load_blockchain_file(self, filename):
        """
        Loads a saved ledger from a given filename
        """
        try:
            with open(filename, "r") as fi:
                json_blockchain = fi.read()

            blockchain = json.loads(json_blockchain)
            self.load_blockchain(blockchain)
        except Exception as excep:
            print str(excep)
            print "Now clearing blockchain".format(filename)
            self.blockchain = []
            self.ledger = {}


    def write_blockchain(self, filename):
        """
        Coverts the blockchain into a json object to then
        be loaded file into the given file
        """
        ledger = self.blockchain_to_json()
        with open(filename, "w") as f:
            f.write(ledger)
            f.close()


    def update(self, key, data):
        """
        Runs the key and data into the func function, and
        sets the ledger key to the value

        Also updates the blockchain and persists to the file

        Returns the newly added block
        """
        block = self.make_block(key, data)
        self.add_block(block)
        return block


    def add_block(self, block):
        """
        Given a block, write its key/value to the ledger, add to the
        blockchain, and persist to disk
        """
        self.values[block.key] = block.value
        self.blockchain.append(block)
        if self.blockchain_file is not None:
            self.write_blockchain(self.blockchain_file)


    def make_block(self, key, data):
        """
        Creates a new block based on the key/value pair
        """
        value = self.exec_func(key, data)
        block = Block(self.current_block, key, data, value)
        return block


    def exec_func(self, key, data):
        value = self.func(key, data)
        return value


    def add_dict_block(self, new_block):
        """
        Given a block, validate and add it to the blockchain
        """
        block = self.make_block(new_block["key"], new_block["input"])
        assert block.hash == new_block["hash"], "Invalid block. Cannot add to blockchain."
        self.add_block(block)

    def blockchain_to_json(self):
        blocks = [block.make_dict() for block in self.blockchain]
        return json.dumps(blocks, indent=4)

    @property
    def current_block(self):
        return self.blockchain[-1] if len(self.blockchain) else None


class Block(object):
    def __init__(self, root_block, key, data, value):
        self.json_dump = {}
        self.root_block = root_block
        self.root_hash = root_block.hash if root_block is not None else "0"
        self.key = key
        self.input = data
        self.value = value
        self.hash = self.create_hash(self.root_hash, data, self.value)

    def create_hash(self, root_hash, input, value):
        hash_func = hashlib.sha256()
        hash_func.update(root_hash)
        hash_func.update(input)
        hash_func.update(value)
        return hash_func.hexdigest()

    def update_dict(self):
        self.json_dump = {
            "root_hash": self.root_hash,
            "hash": self.hash,
            "input": self.input,
            "key": self.key,
            "value": self.value
            }

    def to_json(self):
        self.update_dict()
        return json.dumps(self.json_dump)

    def __repr__(self):
        self.update_dict()
        return str(self.json_dump)


class ChainException(Exception):
    pass


def flow(key, data):
    return data
