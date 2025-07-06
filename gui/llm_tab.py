# gui/llm_tab.py
import tkinter as tk

class LLMTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text="LLM Coach Coming Soon!")
        label.pack(pady=20)
