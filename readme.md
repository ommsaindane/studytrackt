## Study Trackt

A personal study tracking app with an AI assistant built using Python, Tkinter, Pandas, and LangChain with Ollama. It helps you track your sessions, analyze your study habits, get productivity insights, and receive personalized recommendations on what to study next.

---

### Features

- Log study sessions with subject, topic, duration, and notes
- Visualize time spent per subject, weekly/monthly trends, and cumulative effort
- Get AI-generated summaries and custom answers about your study patterns
- Get subject recommendations based on study frequency and recency using machine learning
- Clean, dark-themed Tkinter GUI with a multi-tab dashboard

---

### Requirements

- Python 3.10
- [Ollama](https://ollama.com/) (must be installed and running with the `mistral` model)
- Virtual environment (recommended)

---

### Installation

```bash
# Clone the repo
git clone https://github.com/your-username/study-trackt.git
cd study-trackt

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Ollama
ollama run mistral
```

---

### How to Use

```bash
python main.py
```

- Log new sessions from the **Tracker** tab
- View visualizations in the **Analytics** tab
- Ask AI questions or generate summaries in the **Assistant** tab
- Get what-to-study-next suggestions from the recommender

---

### Optional: Build a Standalone Executable

If you want to distribute it as a Windows `.exe`:

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --add-data "data;data" main.py
```

Find the `.exe` in the `dist/` folder.

> Ollama must still be installed and running on the user’s machine for AI features to work.

---

### Project Structure

```
study-trackt/
├── core/
│   ├── ai.py
│   ├── analytics.py
│   ├── langchain_llm.py
│   ├── recommender.py
│   └── tracker.py
├── gui/
│   ├── analytics_tab.py
│   ├── assistant_tab.py
│   ├── dashboard.py
│   └── tracker_tab.py
├── data/
│   └── study_log.json
├── main.py
└── requirements.txt
```

---

### Models Used

- **LangChain** as LLM framework
- **Mistral** model via **Ollama** (locally served)
- **KMeans Clustering** (via `scikit-learn`) for personalized subject recommendations

