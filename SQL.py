import sqlite3


def create_table():
    con = sqlite3.connect('db.db')  # создаем таблицу.
    cursor = con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS db
    (
    user_id INTEGER PRIMARY KEY,
    ENgroup INTEGER,
    lang TEXT
    )
    """)
    con.commit()
    con.close()

def add_user(user_id, engroup, lang):
    con = sqlite3.connect('db.db')
    cursor = con.cursor()
    add = [user_id, engroup, lang]
    cursor.execute("INSERT OR REPLACE INTO db VALUES(?,?,?);", add)
    con.commit()
    con.close()



def search_db(user_id):
    con = sqlite3.connect('db.db')
    cursor = con.cursor()

    cursor.execute("SELECT ENgroup FROM db WHERE user_id = ?""", (user_id,))
    res = cursor.fetchone()

    con.commit()
    con.close()

    return int(res[0])

def search_lang(user_id):
    con = sqlite3.connect('db.db')
    cursor = con.cursor()

    cursor.execute("SELECT lang FROM db WHERE user_id = ?""", (user_id,))
    res = cursor.fetchone()

    con.commit()
    con.close()

    return str(res[0])