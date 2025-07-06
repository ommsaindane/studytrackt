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


class AnalyticsTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Load logs once
        self.logs = load_study_sessions()

        # ---- Control Bar ----
        control_frame = tk.Frame(self)
        control_frame.pack(pady=5)

        # Subject filter
        tk.Label(control_frame, text="Filter by Subject:").pack(side="left", padx=(5, 2))
        self.subject_var = tk.StringVar(value="All")
        self.subject_menu = ttk.Combobox(
            control_frame,
            textvariable=self.subject_var,
            state="readonly",
            width=12
        )
        self.subject_menu.pack(side="left")

        # Time range toggle
        tk.Label(control_frame, text=" | View Trend By:").pack(side="left", padx=(10, 2))
        self.time_option = tk.StringVar(value="Weekly")
        self.time_menu = ttk.Combobox(
            control_frame,
            textvariable=self.time_option,
            values=["Weekly", "Monthly"],
            state="readonly",
            width=10
        )
        self.time_menu.pack(side="left")

        # Refresh button
        refresh_btn = tk.Button(control_frame, text="Refresh Charts", command=self.plot_charts)
        refresh_btn.pack(side="left", padx=10)

        # Chart area
        self.chart_frame = tk.Frame(self)
        self.chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.setup_subject_options()
        self.plot_charts()

    def setup_subject_options(self):
        subjects = sorted(set(entry.get("subject", "Unknown") for entry in self.logs))
        self.subject_menu["values"] = ["All"] + subjects
        self.subject_var.set("All")

    def plot_charts(self):
        # Clear previous plots
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Reload logs
        self.logs = load_study_sessions()
        self.setup_subject_options()

        selected_subject = self.subject_var.get()
        filtered_logs = [
            entry for entry in self.logs
            if selected_subject == "All" or entry.get("subject") == selected_subject
        ]

        # Show subject bar chart only if "All" selected
        if selected_subject == "All":
            self.draw_bar_chart(
                title="Total Study Time per Subject",
                data=get_study_time_by_subject(filtered_logs),
                color="skyblue"
            )

        # Weekly or monthly time trend
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
            tk.Label(self.chart_frame, text=f"No data for '{title}'").pack(pady=5)
            return

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6, 3))
        keys = list(data.keys())
        values = list(data.values())

        ax.bar(keys, values, color=color)
        ax.set_title(title)
        ax.set_ylabel("Minutes")
        ax.set_xticks(range(len(keys)))
        ax.set_xticklabels(keys, rotation=45, ha="right")
        ax.grid(True, axis="y")

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=10)

    def draw_dual_line_chart(self, title, data, cumulative):
        if not data:
            tk.Label(self.chart_frame, text=f"No data for '{title}'").pack(pady=5)
            return

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6, 3))

        keys = list(data.keys())
        values = list(data.values())
        cum_values = [cumulative[k] for k in keys]

        # Plot main line
        ax.plot(keys, values, marker='o', linestyle='-', color="tomato", label="This Period")
        # Plot cumulative line
        ax.plot(keys, cum_values, marker='o', linestyle='--', color="green", label="Cumulative Total")

        ax.set_title(title)
        ax.set_ylabel("Minutes")
        ax.set_xlabel("Time")
        ax.set_xticks(range(len(keys)))
        ax.set_xticklabels(keys, rotation=45, ha="right")
        ax.grid(True)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=10)
