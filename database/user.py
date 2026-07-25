from database.scan import get_connection

def create_user_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE,

        password TEXT,

        role TEXT

    )
    """)

    conn.commit()
    conn.close()

def create_default_admin():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        INSERT OR IGNORE INTO users(

            username,

            password,

            role

        )

        VALUES(

            'admin',

            'admin123',

            'Admin'

        )

    """)

    conn.commit()

    conn.close() 