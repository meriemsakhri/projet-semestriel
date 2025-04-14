import tkinter as tk
from ui import ExpenseApp

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()