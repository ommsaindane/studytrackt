# gui/dashboard.py
import tkinter as tk
from tkinter import ttk
from gui.tracker_tab import TrackerTab
from gui.analytics_tab import AnalyticsTab
from gui.llm_tab import LLMTab

class Dashboard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        tracker = TrackerTab(notebook)
        analytics = AnalyticsTab(notebook)
        llm = LLMTab(notebook)

        notebook.add(tracker, text="Study Tracker")
        notebook.add(analytics, text="Progress & Analytics")
        notebook.add(llm, text="AI Study Coach")
