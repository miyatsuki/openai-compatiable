from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="dummy")

response = client.chat.completions.create(
    model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello!"}], stream=True
)

for chunk in response:
    # print(chunk)
    print(chunk.choices[0].delta.content, end="", flush=True)
