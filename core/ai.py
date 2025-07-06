# core/ai.py

from core.langchain_llm import generate_summary_from_logs

def generate_study_summary(logs):
    return generate_summary_from_logs(logs)

from core.langchain_llm import ask_question_about_logs

def answer_custom_question(logs, question):
    return ask_question_about_logs(logs, question)
