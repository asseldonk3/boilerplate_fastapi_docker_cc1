import os
from openai import OpenAI

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Model selection (configure in .env)
MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")

def simple_completion(prompt: str, max_tokens: int = 1000) -> str:
    """
    Simple AI completion for small apps.
    Supports multiple models via AI_MODEL env var.
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.7
    )
    return response.choices[0].message.content

def structured_chat(messages: list, max_tokens: int = 1000) -> str:
    """
    For more complex conversations with context.
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.7
    )
    return response.choices[0].message.content

# Test function
if __name__ == "__main__":
    print(f"Testing {MODEL}...")
    result = simple_completion("Say 'Hello from the AI model!'")
    print(result)
