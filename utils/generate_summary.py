import requests
import random
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

OUTROS = [
    "Bhai tu manega?yrrrr 😭",
    "Scene khatarnak hai 🤯",
    "Toh fir milte hain next update mein 🔥",
    "scene badal raha hai,fr💥",
    "chai piyega?",
    "bhayy would you believe"
]

def generate_summary(text: str, style: str = "tadka") -> str:
    """
    Generate a summary of the given news text using Groq API with optional 'tadka' style.

    Parameters:
        text (str): The original news text to summarize.
        style (str): The summary style; default is 'tadka' for spicy GenZ style.

    Returns:
        str: The summarized text or error message.
    """
    if not text:
        return "Error: No text provided for summary."

    if not GROQ_API_KEY:
        return "Error: GROQ_API_KEY is missing in environment."

    if style.lower() == "tadka":
        prompt = [
            {
                "role": "system",
                "content": (
                    "You're a savage GenZ news anchor from India 🗞️🎤. "
                    "Convert boring news into fun, Hinglish, emoji-filled spicy gossips with GenZ slang.\n\n"
                    "IMPORTANT:\n"
                    "Keep the summary **super short**, around 5-6 lines maximum.\n"
                    "End it with one quirky or filmy outro like “Bhai kya hi bolu 😭”.\n\n"
                    "Example:\n"
                    "Original: “The stock market declined 2% due to inflation fears.”\n"
                    "Tadka: “Bro Sensex ne full gadda kha diya 💀—mehengaai ka bhoot back again! Market ne bola: ‘Main toh gaya bhai 🥲’ Bhai kya hi bolu 😭”"
                )
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
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15
        )
        response.raise_for_status()
        data = response.json()

        summary = data.get("choices", [{}])[0].get("message", {}).get("content", "")

        if not summary:
            return "Error: Received empty summary from Groq API."

        if style.lower() == "tadka":
            summary += "\n\n" + random.choice(OUTROS)

        return summary

    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error: {http_err}")
        print(response.text)
        return "Something went wrong with Groq API."
    except requests.exceptions.RequestException as req_err:
        print(f"❌ Request error: {req_err}")
        return "Error: Unable to connect to Groq API."
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return "Error: An unexpected error occurred."
