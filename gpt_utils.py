import os
import time
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

# ✅ Use environment variable (recommended way for new SDK)
client = OpenAI()

def generate_contract(prompt: str, retries: int = 2, delay: float = 1.5) -> str:
    """
    Generate a contract using GPT-3.5-Turbo via OpenAI API.

    :param prompt: Full prompt to send to GPT
    :param retries: Number of retry attempts on failure
    :param delay: Seconds to wait between retries
    :return: Generated contract text
    """
    print("📤 Prompt sent to OpenAI:")
    print(prompt)
    print("🔁 Generating contract...")

    for attempt in range(retries + 1):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a legal assistant that drafts clear, professional contracts."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            content = response.choices[0].message.content.strip()
            print("✅ GPT Contract Generated Successfully")
            return content

        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed: {str(e)}")
            if attempt < retries:
                time.sleep(delay)
            else:
                raise RuntimeError(f"OpenAI API Error after {retries + 1} attempts: {str(e)}")
