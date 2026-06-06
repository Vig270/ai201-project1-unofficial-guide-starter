from embedding import retrieve
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask(question):
    results = retrieve(question, k=4)

    # build context
    context = ""
    sources = []

    for r in results:
        context += f"\n\nSOURCE: {r['source']}\n{r['text']}"
        sources.append(r["source"])

    prompt = f"""
You are a helpful assistant for Binghamton CS students.

RULES:
- Use ONLY the provided context
- If answer is not in context, say "I don't have enough information"
- Do NOT use outside knowledge
- Always be factual

CONTEXT:
{context}

QUESTION:
{question}

Answer clearly and concisely:
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": list(set(sources))
    }