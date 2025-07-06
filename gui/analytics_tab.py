# gui/analytics_tab.py
import tkinter as tk

class AnalyticsTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text="Analytics Coming Soon!")
        label.pack(pady=20)
