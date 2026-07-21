import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import time
import re

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("API Key Issue")
client=Groq(api_key=my_api_key)
model="llama-3.3-70b-versatile"

#Creating tools

def get_product_price(product):
    if product=="iPhone 17":
        return 70000
    elif product=="iPhone 15":
        return 40000
    else:
        return 0

def calculator(exp):
    try:
        return eval(exp)
    except:
        return "Calculator Error"

tools={
    "get_product_price":get_product_price,
    "calculator":calculator
}

#System Prompt
system_prompt="""
#Role
You are a shopping assistant.

#Task and Few Shot
You have these tools:

get_product_price(product)
calculator(exp)

Important:
call tools exactly like these examples:
Action:get_product_price("iPhone 17)
Action:calculator("100000-70000")

#Constraints
Never write:
get_product_price(product="iPhone 17")
Never write:
Action:calculator(exp="100000-70000")

#Rules
Follow these rules:
1.Decide what you need to do next.
2.Call only one tool at a time.
3.After writing an action STOP immediately.
4.Never guess or invent a tool result.
5.Wait until you receive an observation.
6.Then decide your next action.
7.when a task is complete give the final answer.

#Output Format
Format:

Thought:What you need to do.
Action:tool_name(argument)

When Finished:
Final Answer:Your Ansewer
"""
def run_agent(question):
    system_message={
        "role":"system",
        "content":system_prompt
    }

    user_message={
        "role":"user",
        "content":question
    }

    messages=[system_message,user_message]

    for step in range(5):
        print("\n--------------")
        print("Step No= ",step+1)
        print("\n---------------")

        response=client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
        )
        answer=response.choices[0].message.content
        print(answer)

        if "Final Answer" in answer:
            break

        #Now Find the Action
        match = re.search(
           r'Action:\s*([a-zA-Z_]\w*)\((.*?)\)',
           answer
        )

        if match:
            tool_name=match.group(1)
            tool_input=match.group(2)
            tool_input=tool_input.strip()
            tool_input=tool_input.strip('"')

            #Run The Tool
            if tool_name in tools:
                tool=tools[tool_name]
                observation=tool(tool_input)
            else:
                observation="Tool Not Found"

            print("observation",observation)

            # Add LLM response to memory
            messages.append({
                "role": "assistant",
                "content": answer
            })


            # Give tool result back to LLM
            messages.append({
                "role": "user",
                "content":
                    "Observation: "
                    + str(observation)
            })
            time.sleep(5)



prompt="""
I have 100000 rupees. What is the price of an iphone 17?
and how much money will I have left?
"""
run_agent(prompt)