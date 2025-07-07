from datetime import datetime
from collections import defaultdict
from sklearn.cluster import KMeans
import numpy as np


def recommend_subjects(logs, num_recommendations=3):
    if not logs:
        return ["No study data found."]

    now = datetime.now()
    subject_features = defaultdict(lambda: {"count": 0, "total_duration": 0, "last": datetime.min})

    for entry in logs:
        subject = entry["subject"]
        duration = entry.get("duration", 0)
        timestamp = datetime.fromisoformat(entry["timestamp"])

        subject_features[subject]["count"] += 1
        subject_features[subject]["total_duration"] += duration
        subject_features[subject]["last"] = max(subject_features[subject]["last"], timestamp)

    subject_data = []
    subject_names = []

    for subject, stats in subject_features.items():
        days_since = (now - stats["last"]).days
        avg_duration = stats["total_duration"] / stats["count"]
        subject_data.append([stats["count"], days_since, avg_duration])
        subject_names.append(subject)

    # Cluster subjects
    k = min(3, len(subject_data))
    model = KMeans(n_clusters=k, n_init="auto", random_state=42)
    model.fit(subject_data)
    cluster_labels = model.labels_

    # Assume the cluster with least frequency is priority
    cluster_counts = np.bincount(cluster_labels)
    under_studied_cluster = np.argmin(cluster_counts)

    recommended = [
        subject_names[i]
        for i, label in enumerate(cluster_labels)
        if label == under_studied_cluster
    ]

    return recommended[:num_recommendations]
