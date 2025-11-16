import sqlite3


def create_table():
    con = sqlite3.connect('db.db')  # создаем таблицу.
    cursor = con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS db
    (
    user_id INTEGER PRIMARY KEY,
    time INTEGER,
    ENgroup INTEGER
    )
    """)
    con.commit()
    con.close()

def add_user(user_id, time, engroup):
    con = sqlite3.connect('db.db')
    cursor = con.cursor()
    add = [user_id, time, engroup]
    cursor.execute("INSERT INTO db VALUES(?,?,?);", add)
    con.commit()
    con.close()



def update_time(user_id, time):
    con = sqlite3.connect('db.db')
    cursor = con.cursor()

    cursor.execute("UPDATE db SET time = ? WHERE user_id = ?", (time, user_id))

    con.commit()
    con.close()

def search_db(user_id):
    con = sqlite3.connect('db.db')
    cursor = con.cursor()

    cursor.execute("SELECT * FROM db WHERE user_id = ?", (user_id,))
    res = cursor.fetchall()

    con.commit()
    con.close()

    return res