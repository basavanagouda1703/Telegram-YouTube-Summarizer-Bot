import requests
from config import OLLAMA_URL, MODEL_NAME


def generate_summary(transcript_text, language):

    prompt = f"""
Summarize the following YouTube transcript.

Provide:
1. 5 Key Points
2. Short Summary
3. Main Takeaway

Write the entire response in {language}.

Transcript:
{transcript_text}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    return response.json()["response"]


def answer_question(transcript_text, question, language):

    prompt = f"""
Answer the question clearly based only on this transcript.

Write the answer in {language}.

Transcript:
{transcript_text[:3000]}

Question:
{question}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    return response.json()["response"]


def generate_deepdive(transcript_text, language):

    prompt = f"""
Provide a deep detailed breakdown of this video.

Include:
- Concept explanation
- Important insights
- Real-world examples
- Final summary

Write in {language}.

Transcript:
{transcript_text[:3000]}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    return response.json()["response"]