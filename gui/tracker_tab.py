# gui/tracker_tab.py

import tkinter as tk
from tkinter import messagebox, ttk
from core.tracker import save_study_session, load_study_sessions


class TrackerTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#1e1e1e")  # dark background

        # Apply dark theme styling
        self.set_dark_theme()

        # --- Title ---
        title = tk.Label(self, text="Study Tracker", font=("Helvetica", 16, "bold"), fg="white", bg="#1e1e1e")
        title.pack(pady=(10, 5))

        # --- Entry Form ---
        form_frame = tk.Frame(self, bg="#1e1e1e")
        form_frame.pack(padx=15, pady=10, anchor="center")

        labels = ["Subject:", "Topic:", "Duration (minutes):", "Notes:"]
        for i, text in enumerate(labels):
            anchor = "ne" if i == 3 else "e"
            tk.Label(form_frame, text=text, fg="white", bg="#1e1e1e", font=("Segoe UI", 10)).grid(row=i, column=0, sticky=anchor, pady=3, padx=(0, 5))

        self.subject_entry = tk.Entry(form_frame, bg="#2d2d2d", fg="white", insertbackground="white")
        self.topic_entry = tk.Entry(form_frame, bg="#2d2d2d", fg="white", insertbackground="white")
        self.duration_entry = tk.Entry(form_frame, bg="#2d2d2d", fg="white", insertbackground="white")
        self.notes_text = tk.Text(form_frame, height=4, width=30, bg="#2d2d2d", fg="white", insertbackground="white")

        self.subject_entry.grid(row=0, column=1, pady=3, sticky="ew")
        self.topic_entry.grid(row=1, column=1, pady=3, sticky="ew")
        self.duration_entry.grid(row=2, column=1, pady=3, sticky="ew")
        self.notes_text.grid(row=3, column=1, pady=3, sticky="ew")

        # Expand entry column
        form_frame.columnconfigure(1, weight=1)

        save_button = tk.Button(form_frame, text="Save Session", command=self.save_session, bg="#333", fg="white", relief="flat")
        save_button.grid(row=4, column=0, columnspan=2, pady=12)

        # --- Study Log Table ---
        log_frame = tk.Frame(self, bg="#1e1e1e")
        log_frame.pack(fill="both", expand=True, padx=15, pady=(5, 10))

        tk.Label(log_frame, text="Recent Study Sessions", font=("Arial", 12, "bold"), fg="white", bg="#1e1e1e").pack(anchor="w", pady=5)

        self.tree = ttk.Treeview(
            log_frame,
            columns=("subject", "topic", "duration", "timestamp"),
            show="headings",
            style="Dark.Treeview"
        )
        self.tree.heading("subject", text="Subject")
        self.tree.heading("topic", text="Topic")
        self.tree.heading("duration", text="Duration (min)")
        self.tree.heading("timestamp", text="Timestamp")
        self.tree.pack(fill="both", expand=True)

        self.load_logs_into_table()

    def set_dark_theme(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview",
                        background="#2d2d2d",
                        foreground="white",
                        fieldbackground="#2d2d2d",
                        rowheight=24,
                        font=("Segoe UI", 9))
        style.map("Treeview", background=[("selected", "#444")])

        style.configure("Treeview.Heading",
                        background="#1e1e1e",
                        foreground="white",
                        font=("Segoe UI", 10, "bold"))

    def save_session(self):
        subject = self.subject_entry.get()
        topic = self.topic_entry.get()
        duration = self.duration_entry.get()
        notes = self.notes_text.get("1.0", tk.END).strip()

        if not subject or not topic or not duration:
            messagebox.showwarning("Missing Data", "Please fill in all fields.")
            return

        try:
            duration = int(duration)
        except ValueError:
            messagebox.showerror("Invalid Input", "Duration must be a number.")
            return

        save_study_session(subject, topic, duration, notes)
        messagebox.showinfo("Saved", "Study session saved!")

        self.subject_entry.delete(0, tk.END)
        self.topic_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.notes_text.delete("1.0", tk.END)

        self.load_logs_into_table()

    def load_logs_into_table(self):
        self.tree.delete(*self.tree.get_children())

        logs = load_study_sessions()
        for entry in reversed(logs[-20:]):  # Last 20 entries
            self.tree.insert("", tk.END, values=(
                entry["subject"],
                entry["topic"],
                entry["duration"],
                entry["timestamp"].split("T")[0] + " " + entry["timestamp"].split("T")[1][:5]
            ))
