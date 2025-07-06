# core/langchain_llm.py

from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence


# Load llama3 from Ollama
llm = ChatOllama(model="llama3")  # Or mistral, phi3, etc.

# Prompt template
prompt = ChatPromptTemplate.from_template("""
You are a helpful study assistant.

Based on the following study log summary, generate a motivational and insightful reflection for the user.

Study Log Summary:
{log_summary}

Assistant:
""")

# Use LangChain's new RunnableSequence (pipe-style)
chain = prompt | llm


def generate_summary_from_logs(logs):
    if not logs:
        return "No logs to summarize."

    grouped = {}
    for entry in logs:
        subject = entry.get("subject", "Unknown")
        grouped.setdefault(subject, []).append(entry)

    summary_lines = []
    total_minutes = 0

    for subject, entries in grouped.items():
        total = sum(e.get("duration", 0) for e in entries)
        topics = ", ".join(e.get("topic", "") for e in entries)
        summary_lines.append(f"- {subject}: {total} mins, topics: {topics}")
        total_minutes += total

    base_summary = f"You studied for {total_minutes} minutes across {len(grouped)} subjects.\n" + "\n".join(summary_lines)

    response = chain.invoke({"log_summary": base_summary})
    return response.content.strip()

def ask_question_about_logs(logs, user_question):
    if not logs:
        return "No study logs found."

    log_summary = ""
    for entry in logs[-20:]:  # limit for performance
        log_summary += (
            f"Subject: {entry.get('subject')}, "
            f"Topic: {entry.get('topic')}, "
            f"Duration: {entry.get('duration')} minutes, "
            f"Timestamp: {entry.get('timestamp')}\n"
        )

    full_prompt = f"""
You are an AI study coach. Below is the user's recent study log.

Study Log:
{log_summary}

User's Question: {user_question}

Based on the log, provide a helpful, honest, and clear answer.
"""

    response = llm.invoke(full_prompt)
    return response.content.strip()