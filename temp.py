import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        port="3307",
        user="root",
        password="",  # Remplace par ton mot de passe
        database="expenses_db"
    )

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Dépenses")
        self.root.geometry("750x550")

        self.label_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.date_var = tk.StringVar()

        self.setup_ui()
        self.fetch_expenses()

    def setup_ui(self):
        ttk.Label(self.root, text="Étiquette").place(x=30, y=30)
        ttk.Entry(self.root, textvariable=self.label_var, width=30).place(x=130, y=30)

        ttk.Label(self.root, text="Montant (€)").place(x=30, y=70)
        ttk.Entry(self.root, textvariable=self.amount_var, width=30).place(x=130, y=70)

        ttk.Label(self.root, text="Date (YYYY-MM-DD)").place(x=30, y=110)
        ttk.Entry(self.root, textvariable=self.date_var, width=30).place(x=130, y=110)

        ttk.Button(self.root, text="Ajouter", command=self.add_expense).place(x=450, y=30, width=100)
        ttk.Button(self.root, text="Modifier", command=self.update_expense).place(x=450, y=70, width=100)
        ttk.Button(self.root, text="Supprimer", command=self.delete_expense).place(x=450, y=110, width=100)

        # Treeview
        columns = ("id", "label", "amount", "date")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("label", text="Étiquette")
        self.tree.heading("amount", text="Montant (€)")
        self.tree.heading("date", text="Date")

        self.tree.column("id", width=40)
        self.tree.column("label", width=200)
        self.tree.column("amount", width=100)
        self.tree.column("date", width=100)

        self.tree.place(x=30, y=170, width=680, height=300)
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        # Label de somme
        self.total_label = ttk.Label(self.root, text="Total : 0.00 €", font=('Segoe UI', 12, 'bold'))
        self.total_label.place(x=30, y=480)

    def validate_fields(self):
        label = self.label_var.get()
        amount = self.amount_var.get()
        date_str = self.date_var.get()

        if not label or not amount or not date_str:
            messagebox.showwarning("Champs requis", "Tous les champs doivent être remplis.")
            return False

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Montant invalide", "Le montant doit être un nombre positif.")
            return False

        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Date invalide", "La date doit être au format YYYY-MM-DD.")
            return False

        return True

    def add_expense(self):
        if not self.validate_fields():
            return
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (label, amount, date) VALUES (%s, %s, %s)",
                       (self.label_var.get(), float(self.amount_var.get()), self.date_var.get()))
        conn.commit()
        conn.close()
        self.clear_fields()
        self.fetch_expenses()

    def fetch_expenses(self):
        self.tree.delete(*self.tree.get_children())
        total = 0
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses")
        for row in cursor.fetchall():
            self.tree.insert("", tk.END, values=row)
            total += row[2]
        conn.close()
        self.total_label.config(text=f"Total : {total:.2f} €")

    def update_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Sélection requise", "Sélectionnez une ligne à modifier.")
            return
        if not self.validate_fields():
            return
        expense_id = self.tree.item(selected)["values"][0]
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE expenses SET label=%s, amount=%s, date=%s WHERE id=%s",
                       (self.label_var.get(), float(self.amount_var.get()), self.date_var.get(), expense_id))
        conn.commit()
        conn.close()
        self.clear_fields()
        self.fetch_expenses()

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Sélection requise", "Sélectionnez une ligne à supprimer.")
            return
        expense_id = self.tree.item(selected)["values"][0]
        confirm = messagebox.askyesno("Confirmation", "Supprimer cette dépense ?")
        if confirm:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM expenses WHERE id=%s", (expense_id,))
            conn.commit()
            conn.close()
            self.clear_fields()
            self.fetch_expenses()

    def on_row_select(self, event):
        selected = self.tree.selection()
        if selected:
            row = self.tree.item(selected)["values"]
            self.label_var.set(row[1])
            self.amount_var.set(str(row[2]))
            self.date_var.set(row[3])

    def clear_fields(self):
        self.label_var.set("")
        self.amount_var.set("")
        self.date_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()
