import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="127.0.0.1",
            port="3306",
            user="root",
            password="",
            database="expenses_db"
        )
        self.cursor = self.conn.cursor()

    def add_expense(self, label, amount, date):
        query = "INSERT INTO expenses (label, amount, date) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (label, amount, date))
        self.conn.commit()

    def get_all_expenses(self):
        self.cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
        return self.cursor.fetchall()

    def update_expense(self, expense_id, label, amount, date):
        query = "UPDATE expenses SET label=%s, amount=%s, date=%s WHERE id=%s"
        self.cursor.execute(query, (label, amount, date, expense_id))
        self.conn.commit()

    def delete_expense(self, expense_id):
        self.cursor.execute("DELETE FROM expenses WHERE id=%s", (expense_id,))
        self.conn.commit()

    def get_total(self):
        self.cursor.execute("SELECT SUM(amount) FROM expenses")
        result = self.cursor.fetchone()[0]
        return result if result else 0.0

    def __del__(self):
        self.conn.close()