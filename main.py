# main.py
import tkinter as tk
from gui.dashboard import Dashboard

if __name__ == "__main__":
    root = tk.Tk()
    root.title("MindTrackr")
    root.geometry("800x600")
    
    app = Dashboard(root)
    app.pack(fill="both", expand=True)

    root.mainloop()
