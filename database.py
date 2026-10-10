import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="expenses.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT
            )
        ''')
        self.conn.commit()

    def add_expense(self, amount, category, description=""):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO expenses (date, amount, category, description)
            VALUES (?, ?, ?, ?)
        ''', (date, amount, category, description))
        self.conn.commit()
        print("✅ Expense added successfully!")

    def view_all_expenses(self):
        self.cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
        rows = self.cursor.fetchall()
        return rows

    def view_by_category(self, category):
        self.cursor.execute("SELECT * FROM expenses WHERE category = ? ORDER BY date DESC", (category,))
        return self.cursor.fetchall()

    def get_total_spent(self):
        self.cursor.execute("SELECT SUM(amount) FROM expenses")
        result = self.cursor.fetchone()[0]
        return result if result else 0

    def get_total_by_category(self):
        self.cursor.execute('''
            SELECT category, SUM(amount) as total
            FROM expenses
            GROUP BY category
            ORDER BY total DESC
        ''')
        return self.cursor.fetchall()

    def delete_expense(self, expense_id):
        self.cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        self.conn.commit()
        print("🗑️ Expense deleted successfully!")

    def close(self):
        self.conn.close()