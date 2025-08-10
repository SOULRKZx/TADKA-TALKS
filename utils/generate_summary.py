import requests
import random
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_summary(text, style="tadka"):
    outros = [
        "Bhai kya hi bolu 😭",
        "Scene khatarnak hai 🤯",
        "Toh fir milte hain next update mein 🔥",
        "scene badal raha hai,fr kya he scene hai 💥",
        "Kahani abhi baaki hai mere dost 🎬"
    ]

    if not GROQ_API_KEY:
        return "Error: GROQ_API_KEY is missing in environment."

    if style.lower() == "tadka":
        prompt = [
            {
                "role": "system",
                "content": """
You're a savage GenZ news anchor from India 🗞️🎤. 
Convert boring news into fun, Hinglish, emoji-filled spicy gossips with GenZ slang.

IMPORTANT: 
Keep the summary **super short**, around 5-6 lines maximum.
End it with one quirky or filmy outro like “Bhai kya hi bolu 😭”.

Example:
Original: “The stock market declined 2% due to inflation fears.”
Tadka: “Bro Sensex ne full gadda kha diya 💀—mehengaai ka bhoot back again! Market ne bola: ‘Main toh gaya bhai 🥲’ Bhai kya hi bolu 😭”
"""
            },
            {
                "role": "user",
                "content": text
            }
        ]
    else:
        prompt = [
            {"role": "system", "content": "Summarize this news briefly in 3-5 lines."},
            {"role": "user", "content": text}
        ]

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": prompt,
        "temperature": 0.8
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        summary = response.json()["choices"][0]["message"]["content"]

        if style.lower() == "tadka":
            summary += "\n\n" + random.choice(outros)
        return summary

    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error: {http_err}")
        print(response.text)
        return "Something went wrong with Groq API."
    except Exception as e:
        print("❌ Exception occurred:", e)
        return "Error: Unable to connect to Groq API."
