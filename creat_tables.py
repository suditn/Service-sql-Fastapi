import sqlite3


def init_db():
    conn = sqlite3.connect('traffic_db.sqlite')
    cursor = conn.cursor()

    # Создание таблицы клиентов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )''')

    # Создание таблицы трафика
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS traffic (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        ip TEXT NOT NULL,
        date TEXT NOT NULL,
        received_traffic REAL NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    )''')

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()