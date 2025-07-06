# gui/analytics_tab.py

import tkinter as tk
from tkinter import ttk
from core.tracker import load_study_sessions
from core.analytics import (
    get_study_time_by_subject,
    get_study_time_by_week,
    get_study_time_by_month
)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class AnalyticsTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#1e1e1e")  # dark background

        # Apply dark style
        self.set_dark_theme()

        self.logs = load_study_sessions()

        # --- Container Frame (Center aligned) ---
        container = tk.Frame(self, bg="#1e1e1e")
        container.pack(pady=20)
        container.columnconfigure(0, weight=1)

        # --- Title ---
        tk.Label(
            container,
            text="Study Analytics",
            font=("Helvetica", 16, "bold"),
            fg="#ffffff",
            bg="#1e1e1e"
        ).grid(row=0, column=0, pady=(0, 15))

        # --- Controls (Subject + Time + Refresh) ---
        control_frame = tk.Frame(container, bg="#1e1e1e")
        control_frame.grid(row=1, column=0, pady=5)

        tk.Label(control_frame, text="Subject:", font=("Segoe UI", 10), fg="white", bg="#1e1e1e").grid(row=0, column=0, padx=5)
        self.subject_var = tk.StringVar(value="All")
        self.subject_menu = ttk.Combobox(control_frame, textvariable=self.subject_var, state="readonly", width=14)
        self.subject_menu.grid(row=0, column=1, padx=5)

        tk.Label(control_frame, text="View:", font=("Segoe UI", 10), fg="white", bg="#1e1e1e").grid(row=0, column=2, padx=5)
        self.time_option = tk.StringVar(value="Weekly")
        self.time_menu = ttk.Combobox(control_frame, textvariable=self.time_option, values=["Weekly", "Monthly"], state="readonly", width=10)
        self.time_menu.grid(row=0, column=3, padx=5)

        refresh_btn = tk.Button(control_frame, text="🔄 Refresh", command=self.plot_charts, bg="#333", fg="white", relief="flat")
        refresh_btn.grid(row=0, column=4, padx=10)

        # --- Chart display area ---
        self.chart_frame = tk.Frame(self, bg="#1e1e1e")
        self.chart_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.setup_subject_options()
        self.plot_charts()

    def set_dark_theme(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TCombobox",
                        fieldbackground="#2d2d2d",
                        background="#2d2d2d",
                        foreground="white",
                        arrowcolor="white")
        style.map("TCombobox",
                  fieldbackground=[("readonly", "#2d2d2d")],
                  foreground=[("readonly", "white")])

    def setup_subject_options(self):
        subjects = sorted(set(entry.get("subject", "Unknown") for entry in self.logs))
        self.subject_menu["values"] = ["All"] + subjects
        self.subject_var.set("All")

    def plot_charts(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        self.logs = load_study_sessions()
        self.setup_subject_options()

        selected_subject = self.subject_var.get()
        filtered_logs = [
            entry for entry in self.logs
            if selected_subject == "All" or entry.get("subject") == selected_subject
        ]

        if selected_subject == "All":
            self.draw_bar_chart(
                title="Total Study Time per Subject",
                data=get_study_time_by_subject(filtered_logs),
                color="#4da6ff"
            )

        view = self.time_option.get()
        if view == "Weekly":
            trend_data, cum_data = get_study_time_by_week(filtered_logs)
        else:
            trend_data, cum_data = get_study_time_by_month(filtered_logs)

        self.draw_dual_line_chart(
            title=f"{view} Study Trend ({selected_subject})",
            data=trend_data,
            cumulative=cum_data
        )

    def draw_bar_chart(self, title, data, color):
        if not data:
            tk.Label(self.chart_frame, text=f"No data for '{title}'", fg="white", bg="#1e1e1e").pack(pady=5)
            return

        fig, ax = plt.subplots(figsize=(6, 3))
        fig.patch.set_facecolor("#1e1e1e")
        ax.set_facecolor("#2d2d2d")

        keys = list(data.keys())
        values = list(data.values())

        ax.bar(keys, values, color=color)
        ax.set_title(title, color="white")
        ax.set_ylabel("Minutes", color="white")
        ax.set_xticks(range(len(keys)))
        ax.set_xticklabels(keys, rotation=45, ha="right", color="white")
        ax.tick_params(colors='white')
        ax.grid(True, axis="y", color="#444")

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=10)

    def draw_dual_line_chart(self, title, data, cumulative):
        if not data:
            tk.Label(self.chart_frame, text=f"No data for '{title}'", fg="white", bg="#1e1e1e").pack(pady=5)
            return

        fig, ax = plt.subplots(figsize=(6, 3))
        fig.patch.set_facecolor("#1e1e1e")
        ax.set_facecolor("#2d2d2d")

        keys = list(data.keys())
        values = list(data.values())
        cum_values = [cumulative[k] for k in keys]

        ax.plot(keys, values, marker='o', linestyle='-', color="#ff6666", label="This Period")
        ax.plot(keys, cum_values, marker='o', linestyle='--', color="#00cc99", label="Cumulative Total")

        ax.set_title(title, color="white")
        ax.set_ylabel("Minutes", color="white")
        ax.set_xlabel("Time", color="white")
        ax.set_xticks(range(len(keys)))
        ax.set_xticklabels(keys, rotation=45, ha="right", color="white")
        ax.tick_params(colors='white')
        ax.grid(True, color="#444")
        ax.legend(facecolor="#2d2d2d", edgecolor="white", labelcolor="white")

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=10)
