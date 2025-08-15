import time
from openai import OpenAI

def ask_deepseek(command):
    # Create client
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
        default_headers={
            "Authorization": "Bearer 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",
            "HTTP-Referer": "https://yourapp.com"
        }
    )

    stream = client.chat.completions.create(
        model="deepseek/deepseek-r1-zero:free",
        messages=[{"role": "user", "content": command}],
        stream=True
    )

    final_text = ""  # Collect all the text here

    for chunk in stream:
        if chunk.choices[0].delta and chunk.choices[0].delta.content:
            token = chunk.choices[0].delta.content
            final_text += token
            print(token, end='', flush=True)
            time.sleep(0.01)

    # Remove \boxed{} if DeepSeek added it
    final_text = final_text.strip()
    if final_text.startswith("\\boxed{") and final_text.endswith("}"):
        final_text = final_text[len("\\boxed{"):-1].strip()

    return final_text
