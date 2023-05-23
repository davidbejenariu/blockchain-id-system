from app import mysql
from blockchain import Blockchain, Block


def get_blockchain():
    blockchain = Blockchain()
    blockchain_table = Table("blockchain", 'data', 'hash', 'previous', 'nonce')

    for block in blockchain_table.get_all():
        blockchain.add(Block(data=block.get('data'), previous_hash=block.get('previous'), nonce=block.get('nonce')))

    return blockchain


def refresh_blockchain(blockchain):
    blockchain_table = Table("blockchain", 'data', 'hash', 'previous', 'nonce')
    blockchain_table.delete_all()

    for block in blockchain.chain:
        blockchain_table.insert(block.data, block.hash(), block.previous_hash, block.nonce)


def save():
    mysql.connection.commit()


class Table:
    def __init__(self, table_name, *args):
        self.table = table_name
        self.columns = f"{','.join(args)}"
        self.column_list = args

    # SELECT
    def get_all(self):
        cursor = mysql.connection.cursor()
        cursor.execute(f'SELECT * FROM {self.table}')

        return cursor.fetchall()

    def get_one(self, field, value):
        cursor = mysql.connection.cursor()
        result = cursor.execute(f'SELECT * FROM {self.table} WHERE {field} = \"{value}\"')

        data = {}
        if result > 0:
            data = cursor.fetchone()

        cursor.close()
        return data

    # INSERT
    def insert(self, *values):
        cursor = mysql.connection.cursor()

        query = ""
        for value in values:
            query += f'\"{value}\",'

        cursor.execute(f'INSERT INTO `id_system`.`{self.table}` ({self.columns}) VALUES({query[:len(query) - 1]})')

        save()
        cursor.close()

    # UPDATE
    def set_one(self, email, field, value):
        cursor = mysql.connection.cursor()
        cursor.execute(f"UPDATE {self.table} SET {field} = {value} WHERE email = \"{email}\"")

        save()
        cursor.close()

    # DELETE
    def delete_all(self):
        cursor = mysql.connection.cursor()
        cursor.execute(f"TRUNCATE TABLE {self.table}")

        save()
        cursor.close()
