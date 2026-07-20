import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key not found")

model="llama-3.3-70b-versatile"
client = Groq(api_key=my_api_key)
complaint = input("Enter your complaint:")
prompt = f"""
#Role
You are support assistant for a very large mobile and laptop company.
#Task
You have to classify the customer queries into categories.
#Constraints
You have to classify the customer queries into one of the following categories:
1.Technical
2.Billing
3.Return/Exchange
#Output Format
You have to output the category in a single word only and the output should be within the given categories only.
#Zero/One/Few Shot 
For instance if a user compalin says he wants a refund then the category is Return.
#Fallback
If issue is not related to any of the above categories then you have to output "Other".

This is users compaint.
{complaint}
"""
def llmOP(prompt):
    message={
        "role": "user",
        "content": prompt
    }
    messages=[message]
    response = client.chat.completions.create(model=model, messages=messages)
    ans=response.choices[0].message.content
    return ans


print ("AI Response: ", llmOP(prompt))


