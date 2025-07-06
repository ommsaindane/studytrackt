# core/analytics.py
import pandas as pd
from datetime import datetime


def get_study_time_by_subject(logs):
    subject_totals = {}

    for entry in logs:
        subject = entry.get("subject", "Unknown")
        duration = entry.get("duration", 0)

        if subject not in subject_totals:
            subject_totals[subject] = 0
        subject_totals[subject] += duration

    return subject_totals

def get_study_time_by_week(logs):
    if not logs:
        return {}, {}

    df = pd.DataFrame(logs)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["week"] = df["timestamp"].dt.to_period("W").apply(lambda r: r.start_time.strftime("%Y-%m-%d"))

    weekly = df.groupby("week")["duration"].sum()

    # Fill in missing weeks with 0
    full_range = pd.period_range(df["timestamp"].min(), df["timestamp"].max(), freq="W")
    full_index = [p.start_time.strftime("%Y-%m-%d") for p in full_range]

    weekly = weekly.reindex(full_index, fill_value=0).sort_index()
    cumulative = weekly.cumsum()

    return weekly.to_dict(), cumulative.to_dict()

def get_study_time_by_month(logs):
    if not logs:
        return {}, {}

    df = pd.DataFrame(logs)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["month"] = df["timestamp"].dt.to_period("M").astype(str)

    monthly = df.groupby("month")["duration"].sum()

    # Fill in missing months with 0
    full_range = pd.period_range(df["timestamp"].min(), df["timestamp"].max(), freq="M")
    full_index = [p.strftime("%Y-%m") for p in full_range]

    monthly = monthly.reindex(full_index, fill_value=0).sort_index()
    cumulative = monthly.cumsum()

    return monthly.to_dict(), cumulative.to_dict()