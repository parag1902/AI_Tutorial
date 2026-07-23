import os 
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv
import time
load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("API Key Issue")
client=Groq(api_key=my_api_key)
model="llama-3.3-70b-versatile"

JD="""
We are hiring a Backend Python Developer.

Requirements:
- Strong Python
- FastAPI or Django
- PostgreSQL
- Docker
- AWS
- REST APIs
- 2+ years of experience
"""
resume="""
Name: Rahul Sharma

Experience:
3 years as a Software Developer.

Skills:
Python, FastAPI, MySQL, Docker,
REST APIs, Git

Projects:
Built a food delivery backend using
FastAPI and MySQL.

Deployed applications using Docker.
"""

def askLLM(system_prompt,user_prompt):
    system_message={
        "role":"system",
        "content":system_prompt
    }

    user_message={
        "role":"user",
        "content":user_prompt
    }

    messages=[system_message,user_message]
    response=client.chat.completions.create(
        model=model,
        temperature=0,
        messages=messages
    )
    answer=response.choices[0].message.content
    return answer


def step1_res_extract(resume):
    #Extract Skills from resume
    system_prompt="""
    You are a professional HR assistant. Extarct the skills from the candidates resume provided.
    Only return the no other information.
    Do not invent skills by yourself
    Output Format:
    Skills should be separated by commas. Just return comma separated skills do not return any other filler information
    """
    user_prompt=f"""
    Extarct the skills from this resume.
    {resume}
    """
    return askLLM(system_prompt,user_prompt)

def step2_res_extract(jd):
    #Extract Skills from resume
    system_prompt="""
    You are a professional HR assistant. Extarct the skills from the candidates Job Description provided.
    Only return the no other information.
    Do not invent skills by yourself
    Output Format:
    Skills should be separated by commas. Just return comma separated skills do not return any other filler information
    """
    user_prompt=f"""
    Extarct the skills from this resume.
    {jd}
    """
    return askLLM(system_prompt,user_prompt)


def step_3_match(candidate,jd):
    system_prompt="""
    You are a professional HR assistant. Compare the skills of candidate and the skills required in Job Description and produce a final score between 1 and 100 and also produce a final verdict in short weather a candidate is a good fit for a role or not.
    """
    user_prompt=f"""
    Compare and match the skills.
    JD:
    {jd}
    Candidate:
    {candidate}
    """

    return askLLM(system_prompt,user_prompt)


candidate=step1_res_extract(resume)
time.sleep(2)
jd=step2_res_extract(JD)
time.sleep(2)
score=step_3_match(candidate,jd)

print(score)