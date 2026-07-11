import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API Error")

client=Groq(api_key=my_api_key)
model="llama-3.3-70b-versatile"
role="user"
prompt="Suggest a name for my food company"
#System
message_system={
    "role":"system",
    "content":"You are a brand manager you suggest name for my food company suggest one name only"
}
message={
    "role":role,
    "content":prompt
}

messages=[message_system,message]
response=client.chat.completions.create(model=model,messages=messages,temperature=2)


print("=========================")

answer=response.choices[0].message.content
print(answer)