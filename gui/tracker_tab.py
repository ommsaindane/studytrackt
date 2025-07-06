# gui/tracker_tab.py
import tkinter as tk
from tkinter import messagebox, ttk
from core.tracker import save_study_session, load_study_sessions

class TrackerTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # --- Entry Form ---
        form_frame = tk.Frame(self)
        form_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(form_frame, text="Subject:").grid(row=0, column=0, sticky="e")
        tk.Label(form_frame, text="Topic:").grid(row=1, column=0, sticky="e")
        tk.Label(form_frame, text="Duration (minutes):").grid(row=2, column=0, sticky="e")
        tk.Label(form_frame, text="Notes:").grid(row=3, column=0, sticky="ne")

        self.subject_entry = tk.Entry(form_frame)
        self.topic_entry = tk.Entry(form_frame)
        self.duration_entry = tk.Entry(form_frame)
        self.notes_text = tk.Text(form_frame, height=4, width=30)

        self.subject_entry.grid(row=0, column=1, padx=5, pady=2, sticky="we")
        self.topic_entry.grid(row=1, column=1, padx=5, pady=2, sticky="we")
        self.duration_entry.grid(row=2, column=1, padx=5, pady=2, sticky="we")
        self.notes_text.grid(row=3, column=1, padx=5, pady=2, sticky="we")

        save_button = tk.Button(form_frame, text="Save Session", command=self.save_session)
        save_button.grid(row=4, column=0, columnspan=2, pady=10)

        # --- Study Log Table ---
        log_frame = tk.Frame(self)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        tk.Label(log_frame, text="Study Log", font=("Arial", 12, "bold")).pack(anchor="w")

        self.tree = ttk.Treeview(log_frame, columns=("subject", "topic", "duration", "timestamp"), show="headings")
        self.tree.heading("subject", text="Subject")
        self.tree.heading("topic", text="Topic")
        self.tree.heading("duration", text="Duration (min)")
        self.tree.heading("timestamp", text="Timestamp")
        self.tree.pack(fill="both", expand=True)

        self.load_logs_into_table()

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
        # Clear existing table entries
        for row in self.tree.get_children():
            self.tree.delete(row)

        logs = load_study_sessions()
        for entry in reversed(logs[-20:]):  # Show last 20 entries
            self.tree.insert("", tk.END, values=(
                entry["subject"],
                entry["topic"],
                entry["duration"],
                entry["timestamp"].split("T")[0] + " " + entry["timestamp"].split("T")[1][:5]
            ))
