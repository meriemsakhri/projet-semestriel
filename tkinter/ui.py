import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime
import csv
from validation import validate_fields
from database import Database


class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Expense Manager")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)

        # Set appearance and theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Modern color scheme
        self.primary_color = "#1e293b"    # Dark slate blue
        self.secondary_color = "#334155"   # Lighter slate blue
        self.accent_color = "#3b82f6"      # Bright blue
        self.success_color = "#10b981"     # Emerald
        self.warning_color = "#f59e0b"     # Amber
        self.danger_color = "#ef4444"      # Red
        self.text_color = "#f1f5f9"        # Slate gray
        self.muted_text = "#94a3b8"        # Muted text
        self.border_color = "#475569"      # Border color

        # Variables
        self.label_var = ctk.StringVar()
        self.amount_var = ctk.StringVar()
        self.date_var = ctk.StringVar(value=datetime.today().strftime("%Y-%m-%d"))
        self.search_var = ctk.StringVar()
        self.search_var.trace('w', self.on_search)

        # Database
        self.db = Database()
        self.selected_id = None

        # Setup UI
        self.setup_ui()
        self.fetch_expenses()

    def setup_ui(self):
        self.root.configure(fg_color=self.primary_color)
        
        # Create main container
        self.main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Create sidebar
        self.setup_sidebar()
        
        # Create content area
        self.setup_content_area()

    def setup_sidebar(self):
        sidebar = ctk.CTkFrame(
            self.main_container,
            fg_color=self.secondary_color,
            corner_radius=15,
            width=300
        )
        sidebar.pack(side="left", fill="y", padx=(0, 20))

        # App title
        title_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=30)
        
        ctk.CTkLabel(
            title_frame,
            text="Smart Expense",
            font=("Roboto", 24, "bold"),
            text_color=self.accent_color
        ).pack()
        
        ctk.CTkLabel(
            title_frame,
            text="Manager",
            font=("Roboto", 16),
            text_color=self.muted_text
        ).pack()

        # Form
        form_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        form_frame.pack(fill="x", padx=20, pady=20)

        # Input fields
        fields = [
            ("Étiquette", self.label_var),
            ("Montant (TND)", self.amount_var),
            ("Date", self.date_var)
        ]

        for label, var in fields:
            field_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=10)
            
            ctk.CTkLabel(
                field_frame,
                text=label,
                font=("Roboto", 12),
                text_color=self.muted_text
            ).pack(anchor="w")
            
            ctk.CTkEntry(
                field_frame,
                textvariable=var,
                height=40,
                fg_color=self.primary_color,
                border_color=self.border_color,
                text_color=self.text_color,
                placeholder_text=f"Entrer {label.lower()}...",
                font=("Roboto", 13),
                corner_radius=8
            ).pack(fill="x", pady=(5, 0))

        # Buttons
        button_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=20)

        buttons = [
            ("Ajouter", self.success_color, self.add_expense),
            ("Modifier", self.warning_color, self.update_expense),
            ("Supprimer", self.danger_color, self.delete_expense),
            ("Effacer", self.secondary_color, self.clear_fields)
        ]

        for text, color, command in buttons:
            ctk.CTkButton(
                button_frame,
                text=text,
                font=("Roboto", 13, "bold"),
                fg_color=color,
                hover_color=self.accent_color,
                height=40,
                corner_radius=8,
                command=command
            ).pack(fill="x", pady=5)

    def setup_content_area(self):
        content = ctk.CTkFrame(
            self.main_container,
            fg_color=self.secondary_color,
            corner_radius=15
        )
        content.pack(side="left", fill="both", expand=True)

        # Header with search and export
        header = ctk.CTkFrame(content, fg_color="transparent", height=80)
        header.pack(fill="x", padx=20, pady=20)
        header.pack_propagate(False)

        # Search box
        search_frame = ctk.CTkFrame(header, fg_color="transparent")
        search_frame.pack(side="left", fill="both", expand=True)
        
        ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Rechercher des dépenses...",
            font=("Roboto", 13),
            height=45,
            fg_color=self.primary_color,
            border_color=self.border_color,
            corner_radius=8
        ).pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Export button
        ctk.CTkButton(
            header,
            text="Exporter CSV",
            font=("Roboto", 13, "bold"),
            fg_color=self.accent_color,
            hover_color=self.success_color,
            width=130,
            height=45,
            corner_radius=8,
            command=self.export_to_csv
        ).pack(side="right")

        # Table
        self.setup_table(content)

        # Footer with total
        footer = ctk.CTkFrame(content, fg_color=self.primary_color, height=60, corner_radius=10)
        footer.pack(fill="x", padx=20, pady=20)
        footer.pack_propagate(False)

        self.total_label = ctk.CTkLabel(
            footer,
            text="Total: 0.00 TND",
            font=("Roboto", 16, "bold"),
            text_color=self.accent_color
        )
        self.total_label.pack(side="right", padx=20, pady=10)

    def setup_table(self, parent):
        # Table container
        table_container = ctk.CTkFrame(parent, fg_color=self.primary_color, corner_radius=10)
        table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Headers
        headers = ["ID", "Étiquette", "Montant (TND)", "Date"]
        header_frame = ctk.CTkFrame(table_container, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=15)
        
        for idx, header in enumerate(headers):
            weight = 3 if idx == 1 else 1
            header_frame.grid_columnconfigure(idx, weight=weight)
            ctk.CTkLabel(
                header_frame,
                text=header,
                font=("Roboto", 13, "bold"),
                text_color=self.muted_text
            ).grid(row=0, column=idx, sticky="w")

        # Scrollable frame for expenses
        self.scrollable_table = ctk.CTkScrollableFrame(
            table_container,
            fg_color="transparent"
        )
        self.scrollable_table.pack(fill="both", expand=True, padx=5, pady=(0, 10))

        for i in range(4):
            weight = 3 if i == 1 else 1
            self.scrollable_table.grid_columnconfigure(i, weight=weight)

    def on_search(self, *args):
        self.fetch_expenses()

    def fetch_expenses(self):
        # Clear existing table
        for widget in self.scrollable_table.winfo_children():
            widget.destroy()

        # Fetch and filter expenses
        expenses = self.db.get_all_expenses()
        search_term = self.search_var.get().lower()
        filtered_expenses = [
            exp for exp in expenses
            if search_term in str(exp[0]).lower() or
            search_term in exp[1].lower() or
            search_term in str(exp[2]).lower() or
            search_term in str(exp[3]).lower()
        ]

        # Populate table
        for row_idx, expense in enumerate(filtered_expenses):
            expense_id, label, amount, date = expense
            row_data = [str(expense_id), label, f"{amount:.2f}", date]
            
            row_frame = ctk.CTkFrame(
                self.scrollable_table,
                fg_color=self.secondary_color if row_idx % 2 == 0 else "transparent",
                corner_radius=6
            )
            row_frame.grid(row=row_idx, column=0, columnspan=4, sticky="ew", pady=2)
            row_frame.bind("<Button-1>", lambda e, id=expense_id: self.on_row_select(id))

            for col_idx, value in enumerate(row_data):
                weight = 3 if col_idx == 1 else 1
                row_frame.grid_columnconfigure(col_idx, weight=weight)
                ctk.CTkLabel(
                    row_frame,
                    text=value,
                    font=("Roboto", 13),
                    text_color=self.text_color,
                    anchor="w",
                    padx=15,
                    pady=12
                ).grid(row=0, column=col_idx, sticky="w")

        # Update total
        total = self.db.get_total()
        self.total_label.configure(text=f"Total: {total:.2f} TND")

    def add_expense(self):
        errors = validate_fields(
            self.label_var.get(), self.amount_var.get(), self.date_var.get()
        )
        if errors:
            messagebox.showerror("Erreur", "\n".join(errors))
            return
        self.db.add_expense(
            self.label_var.get(), float(self.amount_var.get()), self.date_var.get()
        )
        self.clear_fields()
        self.fetch_expenses()

    def update_expense(self):
        if not self.selected_id:
            messagebox.showinfo("Sélection", "Veuillez sélectionner une dépense.")
            return
        errors = validate_fields(
            self.label_var.get(), self.amount_var.get(), self.date_var.get()
        )
        if errors:
            messagebox.showerror("Erreur", "\n".join(errors))
            return
        self.db.update_expense(
            self.selected_id,
            self.label_var.get(),
            float(self.amount_var.get()),
            self.date_var.get(),
        )
        self.clear_fields()
        self.fetch_expenses()

    def delete_expense(self):
        if not self.selected_id:
            messagebox.showinfo("Sélection", "Veuillez sélectionner une dépense.")
            return
        if messagebox.askyesno("Confirmation", "Supprimer cette dépense ?"):
            self.db.delete_expense(self.selected_id)
            self.clear_fields()
            self.fetch_expenses()

    def on_row_select(self, expense_id):
        self.selected_id = expense_id
        for expense in self.db.get_all_expenses():
            if expense[0] == expense_id:
                self.label_var.set(expense[1])
                self.amount_var.set(str(expense[2]))
                self.date_var.set(expense[3])
                break

    def clear_fields(self):
        self.label_var.set("")
        self.amount_var.set("")
        self.date_var.set(datetime.today().strftime("%Y-%m-%d"))
        self.selected_id = None

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Fichiers CSV", "*.csv")]
        )
        if not file_path:
            return
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Étiquette", "Montant (TND)", "Date"])
            for expense in self.db.get_all_expenses():
                writer.writerow(expense)
        messagebox.showinfo("Succès", "Exportation réussie.")


if __name__ == "__main__":
    root = ctk.CTk()
    app = ExpenseApp(root)
    root.mainloop()