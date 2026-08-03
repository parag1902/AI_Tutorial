import os
import json
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel
from pypdf import PdfReader
import time

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("Groq API Key Issue")

client=Groq(api_key=my_api_key)
model="llama-3.3-70b-versatile"


def readResume():
    reader=PdfReader("/workspaces/AI_Tutorial/week2/Portfolio/ParagDeshpande_CV.pdf")
    text=""
    for page in reader.pages:
        page_text=page.extract_text()
        if page_text:
            text=text+page_text+"\n"
    return text

resume_text=readResume()

class Experience(BaseModel):
    company: str
    role: str
    duration: str
    description: str

class Resume(BaseModel):
    name:str
    phone:str
    email:str
    github:str
    linkedin:str
    location:str
    summary:str
    experience:list[Experience]
    projects:list[str]
    skills:list[str]
    certifications:list[str]

Resume_schema=Resume.model_json_schema()

system_prompt = f"""
You are an expert resume parser.

Your task is to extract structured information from the given resume and return it as valid JSON.

The resume may contain information in different formats and section names. Extract information based on its meaning, not just the section headings.

Examples:
- "Experience", "Professional Experience", "Employment", "Work History", and "Internships" all represent work experience.
- Skills may appear in dedicated skills sections, project descriptions, certifications, or work experience.
- Projects may appear under "Projects", "Academic Projects", "Personal Projects", or within experience.

Return ONLY a valid JSON object that strictly follows the schema below.

JSON Schema:
{Resume_schema}

Rules:
1. Follow the JSON schema exactly.
2. Do NOT add fields that are not present in the schema.
3. Extract only information explicitly mentioned in the resume.
4. Do NOT guess, infer, or fabricate any information.
5. If a string field is missing, return an empty string ("").
6. If a list field has no information, return an empty list ([]).
7. Preserve the original wording as much as possible.
8. Remove duplicate values from lists while preserving order.
9. Return ONLY the JSON object. Do not include explanations, markdown, or code fences.
"""
system_message={
    "role":"system",
    "content":system_prompt
}
user_prompt = f"""
Extract the structured information from the following resume.

Resume:

{resume_text}
"""
user_messsage={
    "role":"user",
    "content":user_prompt
}
messages=[system_message,user_messsage]
response_format={
    "type": "json_object"
}
response=client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=0,
    response_format=response_format)

answer=response.choices[0].message.content


