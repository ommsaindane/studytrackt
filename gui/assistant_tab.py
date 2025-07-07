# gui/assistant_tab.py

import tkinter as tk
from tkinter import scrolledtext
from core.tracker import load_study_sessions
from core.ai import generate_study_summary, answer_custom_question
from core.recommender import recommend_subjects


class AssistantTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#1e1e1e")

        # Title label
        tk.Label(
            self,
            text="AI Study Coach",
            font=("Helvetica", 16, "bold"),
            fg="white",
            bg="#1e1e1e"
        ).pack(pady=(15, 10))

        # Output display box
        self.output_box = scrolledtext.ScrolledText(
            self, wrap=tk.WORD, height=12,
            bg="#2d2d2d", fg="white", insertbackground="white",
            font=("Segoe UI", 10)
        )
        self.output_box.pack(padx=20, pady=10, fill="both", expand=True)

        # Generate Summary Button
        generate_btn = tk.Button(
            self, text="Generate Study Summary", command=self.generate_summary,
            bg="#333", fg="white", relief="flat"
        )
        generate_btn.pack(pady=(0, 10))

        # Custom Question Entry
        self.question_entry = tk.Entry(
            self, width=50, bg="#2d2d2d", fg="white", insertbackground="white"
        )
        self.question_entry.pack(padx=20, pady=(5, 5))

        ask_btn = tk.Button(
            self, text="Ask Question", command=self.ask_question,
            bg="#444", fg="white", relief="flat"
        )
        ask_btn.pack(pady=(0, 10))

        recommend_btn = tk.Button(
            self, text="📚 What Should I Study Next?", command=self.show_recommendations,
            bg="#555", fg="white", relief="flat"
        )
        recommend_btn.pack(pady=(0, 10))

    def generate_summary(self):
        logs = load_study_sessions()
        summary = generate_study_summary(logs[-7:])
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, summary)

    def ask_question(self):
        question = self.question_entry.get().strip()
        if not question:
            return

        logs = load_study_sessions()
        response = answer_custom_question(logs, question)
        self.output_box.insert(tk.END, f"\n\n🧠 Q: {question}\n➡️ {response}\n")
        self.output_box.see(tk.END)

    def show_recommendations(self):
        logs = load_study_sessions()
        subjects = recommend_subjects(logs)

        self.output_box.insert(tk.END, "\n\n🎯 Recommended Subjects:\n")
        for sub in subjects:
            self.output_box.insert(tk.END, f"• {sub}\n")

        self.output_box.see(tk.END)