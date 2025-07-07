from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence

# Use a faster model like 'mistral' instead of 'llama3' (optional)
# Or use 'llama3' if you still prefer that
llm = ChatOllama(model="mistral", temperature=0.4, max_tokens=150)

# Concise and directly helpful prompt
prompt = ChatPromptTemplate.from_template("""
You're an AI study coach. Based on this short list of logged study topics, write only 3 concise bullet points:

- Most studied subject
- Subject or topic needing more time
- Productivity tip
(Keep it under 80 words.)

Study Log:
{log_summary}
""")

chain = prompt | llm

def generate_summary_from_logs(logs):
    if not logs:
        return "No logs to summarize."

    # Limit to last 5 logs for speed and relevance
    logs = logs[-5:]

    summary_lines = []
    for entry in logs:
        subject = entry.get("subject", "Unknown")
        topic = entry.get("topic", "")
        duration = entry.get("duration", 0)
        summary_lines.append(f"{subject}: {topic} - {duration} mins")

    base_summary = "\n".join(summary_lines)

    response = chain.invoke({"log_summary": base_summary})
    return response.content.strip()

def ask_question_about_logs(logs, user_question):
    if not logs:
        return "No study logs found."

    logs = logs[-10:]  # limit for speed and relevance

    log_summary = "\n".join([
        f"{entry.get('subject')} - {entry.get('topic')} ({entry.get('duration')} min)"
        for entry in logs
    ])

    question_prompt = f"""
You are an AI study assistant. You will receive a short study log and a question.
Respond clearly in no more than 80 words.

Study Log:
{log_summary}

Question: {user_question}

Answer:
"""

    response = llm.invoke(question_prompt)
    return response.content.strip()