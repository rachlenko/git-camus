from openai import OpenAI, OpenAIError
import os

client = OpenAI(api_key=str(os.getenv("OPENAI_API_KEY")))

try:
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Write a haiku about recursion in programming."},
        ]
    )
    print(completion.choices[0].message.content)
except OpenAIError as e:
    print(f"An error occurred: {e}")
