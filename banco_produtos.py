import sqlite3

connection = sqlite3.connect('tutorial.db')
c = connection.cursor()


def create_table():
    c.execute(
        """CREATE TABLE IF NOT EXISTS produtos(codigo text, nome text, 
        quantidade text, preco text)""")


create_table()




