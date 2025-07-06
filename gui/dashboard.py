# gui/dashboard.py

import tkinter as tk
from tkinter import ttk
from gui.tracker_tab import TrackerTab
from gui.analytics_tab import AnalyticsTab
from gui.assistant_tab import AssistantTab


class Dashboard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#1e1e1e")  # set dashboard bg

        # Apply dark theme to tabs
        self.set_dark_theme()

        # --- Styled Notebook ---
        notebook = ttk.Notebook(self, style="Dark.TNotebook")
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        tracker = TrackerTab(notebook)
        analytics = AnalyticsTab(notebook)
        assistant = AssistantTab(notebook)

        notebook.add(tracker, text="Study Tracker")
        notebook.add(analytics, text="Progress & Analytics")
        notebook.add(assistant, text="AI Study Coach")

    def set_dark_theme(self):
        style = ttk.Style()
        style.theme_use("default")

        # Notebook tabs
        style.configure("Dark.TNotebook",
                        background="#1e1e1e",
                        borderwidth=0)

        style.configure("Dark.TNotebook.Tab",
                        background="#2d2d2d",
                        foreground="white",
                        padding=[10, 5],
                        font=("Segoe UI", 10))

        style.map("Dark.TNotebook.Tab",
                  background=[("selected", "#3c3c3c")],
                  foreground=[("selected", "white")])
