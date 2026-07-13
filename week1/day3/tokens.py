#Helps Python interact with your computer (e.g., read environment variables).
import os

#Makes it easy to work with files and folders
from pathlib import Path

#This reads your .env file so that your API keys are available in python
from dotenv import load_dotenv

#Lets your python program send request to Groq AI models
from groq import Groq

# Loads the values from the .env file into your program
load_dotenv()  

# Gets the value of GROQ_API_KEY from the environment variables
my_api_key = os.getenv("GROQ_API_KEY")

# Checks if the API key is missing or empty
if not my_api_key:
    # Stops the program and shows an error if the API key is not found
    raise ValueError("API Key Issue")
    
# Creates a Groq client using your API key so you can send requests to Groq AI
client = Groq(api_key=my_api_key)

# Name of the AI model that will answer our questions
model = "llama-3.3-70b-versatile"


# Stores the role of the user (not used later in this code)
role = "user"


# Takes a question from the user as input
prompt = input("Enter your query!")


# Defines the system message
# This tells the AI how it should behave before answering
message_system = {
    "role": "system",
    "content": "You are a technical support assistant. Solve users' technical queries."
}


# Defines the user's message
# This is the actual question that will be sent to the AI
message = {
    "role": "user",
    "content": prompt
}


# Combines the system message and user message into one list
# The API expects all conversation messages in this format
messages = [message_system, message]


# Sends the request to the Groq AI model
# The model reads the messages and generates a response
response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=1,
    max_tokens=400
)


# Extracts only the AI's answer from the response
answer = response.choices[0].message.content


# Gets token usage information from the API response
usage = response.usage


# Prints a separator line
print("*********")


# Prints the user's question and the number of prompt tokens used
print(f"User Query: {prompt} Token Consumption: {usage.prompt_tokens} Finish Reason {response.choices[0].finish_reason}")


# Prints the AI's answer and the number of completion tokens used
print(f"AI Answer: {answer} Token Consumption: {usage.completion_tokens} Finish Reason {response.choices[0].finish_reason}")


# Prints the total number of tokens used (prompt + completion)
print(f"Total Token Consumption: {usage.total_tokens} Finish Reason {response.choices[0].finish_reason}")


