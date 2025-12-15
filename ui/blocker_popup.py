import tkinter as tk
from tkinter import messagebox

def show_block_popup(url):
    root = tk.Tk()
    root.withdraw()

    messagebox.showerror(
        "⚠️ Phishing Alert",
        f"Blocked unsafe website:\n\n{url}"
    )

    root.destroy()
