from app import mysql
from blockchain import Blockchain, Block


def is_new_table(name):
    cur = mysql.connection.cursor()

    try:
        result = cur.execute(f"SELECT * from {name}")
        cur.close()
    except:
        return True
    else:
        return False


class Table:
    def __init__(self, table_name, *args):
        self.table = table_name
        self.columns = f"{','.join(args)}"
        self.columnList = args

    # Base class for table
    def get_all(self):
        cur = mysql.connection.cursor()
        result = cur.execute(f"SELECT * FROM {self.table}")
        data = cur.fetchall()
        return data

    # Base class for table
    def get_one(self, search, value):
        data = {}
        cur = mysql.connection.cursor()
        result = cur.execute(f"SELECT * FROM {self.table} WHERE {search} = \"{value}\"")

        if result > 0:
            data = cur.fetchone()

        cur.close()
        return data

    # Delete function for table
    def delete_one(self, search, value):
        cur = mysql.connection.cursor()
        cur.execute(f"DELETE from {self.table} where {search} = \"{value}\"")
        mysql.connection.commit()
        cur.close()

    # Delete all
    def delete_all(self):
        cur = mysql.connection.cursor()
        cur.execute(f"TRUNCATE TABLE {self.table}")
        mysql.connection.commit()
        cur.close()

    # Drop function for table
    def drop(self):
        cur = mysql.connection.cursor()
        cur.execute(f"DROP TABLE {self.table}")
        cur.close()

    # Insert function for table
    def insert(self, *args):
        data = ""
        for arg in args:
            data += f'\"{arg}\",'

        cur = mysql.connection.cursor()
        cur.execute(f"INSERT INTO `blockchain-id-system`.`{self.table}` ({self.columns}) VALUES({data[:len(data) - 1]})")
        mysql.connection.commit()
        cur.close()


# Function to get blockchain
def get_blockchain():
    blockchain = Blockchain()
    blockchain_sql = Table("blockchain", 'number', 'hash', 'previous', 'data', 'nonce')

    for b in blockchain_sql.get_all():
        blockchain.add(Block(number=int(b.get('number')), previous_hash=b.get('previous'), data=b.get('data'), nonce=b.get('nonce')))

    return blockchain


# Function to sync blockchain to mysql
def sync_blockchain(blockchain):
    blockchain_sql = Table("blockchain", 'number', 'hash', 'previous', 'data', 'nonce')
    blockchain_sql.delete_all()

    for b in blockchain.chain:
        blockchain_sql.insert(str(b.number), b.hash(), b.previous_hash, b.data, b.nonce)