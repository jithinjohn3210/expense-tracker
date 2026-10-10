import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="expenses.db"):
        self.db_name = db_name
        self.create_table()

    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def create_table(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def add_expense(self, amount, category, description=""):
        conn = self.get_connection()
        cursor = conn.cursor()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO expenses (date, amount, category, description)
            VALUES (?, ?, ?, ?)
        ''', (date, amount, category, description))
        conn.commit()
        conn.close()
        print("✅ Expense added successfully!")

    def view_all_expenses(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def view_by_category(self, category):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses WHERE category = ? ORDER BY date DESC", (category,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_total_spent(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM expenses")
        result = cursor.fetchone()[0]
        conn.close()
        return result if result else 0

    def get_total_by_category(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT category, SUM(amount) as total
            FROM expenses
            GROUP BY category
            ORDER BY total DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return rows

    def delete_expense(self, expense_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        conn.close()
        print("🗑️ Expense deleted successfully!")