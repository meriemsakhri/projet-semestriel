import customtkinter as ctk
from ui import ExpenseApp

if __name__ == "__main__":
    root = ctk.CTk()
    app = ExpenseApp(root)
    root.mainloop()