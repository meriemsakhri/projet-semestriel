import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import csv
from validation import validate_fields
from database import Database


class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Dépenses")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        self.bg_color = "#f0f4f8"
        self.accent_color = "#4a90e2"
        self.secondary_color = "#50c878"
        self.text_color = "#2d3436"
        self.error_color = "#d63031"
        self.green_color = "#27ae60"
        self.yellow_color = "#f1c40f"
        self.red_color = "#e74c3c"

        self.root.configure(bg=self.bg_color)

        self.label_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.date_var = tk.StringVar(value=datetime.today().strftime("%Y-%m-%d"))

        self.db = Database()

        self.setup_ui()
        self.fetch_expenses()

    def setup_ui(self):
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Green.TButton",
            padding=8,
            font=("Segoe UI", 10, "bold"),
            background=self.green_color,
            foreground="white",
            bordercolor=self.green_color,
        )
        style.map("Green.TButton", background=[("active", "#219150")])

        style.configure(
            "Yellow.TButton",
            padding=8,
            font=("Segoe UI", 10, "bold"),
            background=self.yellow_color,
            foreground="black",
            bordercolor=self.yellow_color,
        )
        style.map("Yellow.TButton", background=[("active", "#d4ac0d")])

        style.configure(
            "Red.TButton",
            padding=8,
            font=("Segoe UI", 10, "bold"),
            background=self.red_color,
            foreground="white",
            bordercolor=self.red_color,
        )
        style.map("Red.TButton", background=[("active", "#c0392b")])

        style.configure(
            "Neutral.TButton",
            padding=8,
            font=("Segoe UI", 10, "bold"),
            background="#95a5a6",
            foreground="white",
            bordercolor="#95a5a6",
        )
        style.map("Neutral.TButton", background=[("active", "#7f8c8d")])

        style.configure(
            "TButton",
            padding=8,
            font=("Segoe UI", 10, "bold"),
            background=self.accent_color,
            foreground="white",
            bordercolor=self.accent_color,
        )
        style.map("TButton", background=[("active", "#3b7ed0")])
        style.configure(
            "TLabel",
            font=("Segoe UI", 10),
            background=self.bg_color,
            foreground=self.text_color,
        )
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background=self.accent_color,
            foreground="white",
        )
        style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            background="white",
            foreground=self.text_color,
            rowheight=25,
            fieldbackground="white",
        )
        style.map("Treeview", background=[("selected", self.secondary_color)])

        form_frame = ttk.LabelFrame(
            self.root,
            text="Nouvelle Dépense",
            padding=(20, 10),
            style="Custom.TLabelframe",
        )
        style.configure(
            "Custom.TLabelframe", background=self.bg_color, foreground=self.text_color
        )
        style.configure(
            "Custom.TLabelframe.Label",
            font=("Segoe UI", 12, "bold"),
            foreground=self.text_color,
        )
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        form_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(form_frame, text="Étiquette:").grid(
            row=0, column=0, sticky="w", pady=5, padx=10
        )
        ttk.Entry(form_frame, textvariable=self.label_var, width=30).grid(
            row=0, column=1, pady=5, padx=10, sticky="ew"
        )

        ttk.Label(form_frame, text="Montant (TND):").grid(
            row=1, column=0, sticky="w", pady=5, padx=10
        )
        ttk.Entry(form_frame, textvariable=self.amount_var, width=30).grid(
            row=1, column=1, pady=5, padx=10, sticky="ew"
        )

        ttk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(
            row=2, column=0, sticky="w", pady=5, padx=10
        )
        ttk.Entry(form_frame, textvariable=self.date_var, width=30).grid(
            row=2, column=1, pady=5, padx=10, sticky="ew"
        )

        btn_frame = ttk.Frame(form_frame, style="Custom.TFrame")
        style.configure("Custom.TFrame", background=self.bg_color)
        btn_frame.grid(row=0, column=2, rowspan=3, padx=15, sticky="n")

        ttk.Button(
            btn_frame, text="Ajouter", style="Green.TButton", command=self.add_expense
        ).grid(row=0, column=0, pady=5, sticky="ew")
        ttk.Button(
            btn_frame,
            text="Modifier",
            style="Yellow.TButton",
            command=self.update_expense,
        ).grid(row=1, column=0, pady=5, sticky="ew")
        ttk.Button(
            btn_frame,
            text="Supprimer",
            style="Red.TButton",
            command=self.delete_expense,
        ).grid(row=2, column=0, pady=5, sticky="ew")
        ttk.Button(
            btn_frame,
            text="Effacer",
            style="Neutral.TButton",
            command=self.clear_fields,
        ).grid(row=3, column=0, pady=5, sticky="ew")

        self.tree = ttk.Treeview(
            self.root, columns=("id", "label", "amount", "date"), show="headings"
        )
        for col, label in zip(
            ("id", "label", "amount", "date"),
            ("ID", "Étiquette", "Montant (TND)", "Date"),
        ):
            self.tree.heading(col, text=label)
            self.tree.column(col, anchor="center", width=150 if col != "id" else 80)
        self.tree.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        bottom_frame = ttk.Frame(self.root, style="Custom.TFrame")
        bottom_frame.grid(row=2, column=0, pady=10, padx=10, sticky="ew")
        bottom_frame.grid_columnconfigure(0, weight=1)

        self.total_label = ttk.Label(
            bottom_frame,
            text="Total : 0.00 TND",
            font=("Segoe UI", 12, "bold"),
            foreground=self.secondary_color,
            background=self.bg_color,
        )
        self.total_label.pack(side="left", padx=10)

        ttk.Button(bottom_frame, text="Exporter CSV", command=self.export_to_csv).pack(
            side="right", padx=10
        )

    def add_expense(self):
        errors = validate_fields(
            self.label_var.get(), self.amount_var.get(), self.date_var.get()
        )
        if errors:
            messagebox.showerror(
                "Erreur de validation", "\n".join(errors), icon="error"
            )
            return
        self.db.add_expense(
            self.label_var.get(), float(self.amount_var.get()), self.date_var.get()
        )
        self.clear_fields()
        self.fetch_expenses()

    def fetch_expenses(self):
        self.tree.delete(*self.tree.get_children())
        total = self.db.get_total()
        for row in self.db.get_all_expenses():
            self.tree.insert("", tk.END, values=row)
        self.total_label.config(text=f"Total : {total:.2f} TND")

    def update_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo(
                "Sélection requise", "Veuillez sélectionner une ligne.", icon="info"
            )
            return
        errors = validate_fields(
            self.label_var.get(), self.amount_var.get(), self.date_var.get()
        )
        if errors:
            messagebox.showerror(
                "Erreur de validation", "\n".join(errors), icon="error"
            )
            return
        expense_id = self.tree.item(selected)["values"][0]
        self.db.update_expense(
            expense_id,
            self.label_var.get(),
            float(self.amount_var.get()),
            self.date_var.get(),
        )
        self.clear_fields()
        self.fetch_expenses()

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo(
                "Sélection requise", "Veuillez sélectionner une ligne.", icon="info"
            )
            return
        if messagebox.askyesno(
            "Confirmation", "Voulez-vous vraiment supprimer cette dépense ?"
        ):
            expense_id = self.tree.item(selected)["values"][0]
            self.db.delete_expense(expense_id)
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
        self.date_var.set(datetime.today().strftime("%Y-%m-%d"))

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("Fichiers CSV", "*.csv")]
        )
        if not file_path:
            return
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Étiquette", "Montant (TND)", "Date"])
            for row_id in self.tree.get_children():
                writer.writerow(self.tree.item(row_id)["values"])
        messagebox.showinfo(
            "Exportation", "Les dépenses ont été exportées avec succès.", icon="info"
        )
