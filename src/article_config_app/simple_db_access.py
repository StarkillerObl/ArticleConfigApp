import sqlite3

def main():
    create_table()
    # insert_data('Plate', 5, 5)
    delete('Coffee Cup')
    update('Plate', 5, 6.50)
    print(view())


def create_table():
    connection=sqlite3.connect("sqlite.db")
    cursor=connection.cursor()
    cursor.execute("create table if not exists store (item TEXT, quantity INTEGER, price REAL )")
    connection.commit()
    connection.close()


def insert_data(item, quantity, price):
    connection=sqlite3.connect("sqlite.db")
    cursor=connection.cursor()
    cursor.execute("insert into store values (?,?,?)", (item, quantity, price))
    connection.commit()
    connection.close()


def view():
    connection = sqlite3.connect('sqlite.db')
    cursor = connection.cursor()
    cursor.execute("select * from store")
    rows = cursor.fetchall()
    connection.close()
    return rows


def delete(item):
    connection = sqlite3.connect('sqlite.db')
    cursor = connection.cursor()
    cursor.execute('delete from store where item=?', (item,))
    connection.commit()
    connection.close()

def update(item, new_quantity, new_price):
    connection = sqlite3.connect('sqlite.db')
    cursor = connection.cursor()
    cursor.execute('update store set quantity=?, price=? where item=?', (new_quantity, new_price, item))
    connection.commit()
    connection.close()


if __name__ == '__main__':
    main()
