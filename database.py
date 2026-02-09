import sqlite3

class Database:
    def __init__(self, db_name="economy.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Create users table with global balance
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                wallet INTEGER DEFAULT 1000,
                bank INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def get_user(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = self.cursor.fetchone()
        if user is None:
            self.cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
            self.conn.commit()
            return (user_id, 1000, 0)
        return user

    def update_wallet(self, user_id, amount):
        self.get_user(user_id) # Ensure user exists
        self.cursor.execute('UPDATE users SET wallet = wallet + ? WHERE user_id = ?', (amount, user_id))
        self.conn.commit()

db = Database()