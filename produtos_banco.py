import sqlite3

connection = sqlite3.connect('produtos.db')
c = connection.cursor()


def create_table():
    c.execute(
        """CREATE TABLE IF NOT EXISTS produtos(codigo integer, nome text, 
        quantidade integer, preco real)""")


create_table()
