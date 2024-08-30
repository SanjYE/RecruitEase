import PyPDF2
from openai import OpenAI
import os

client = OpenAI(
    api_key="***",
)

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def chat_gpt(messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message.content.strip()

def set_internship_criteria():
    criteria = """
    Internship Eligibility Criteria:
    1. Minimum GPA: 7.0
    2. Year of study: 2nd year or above
    3. Major: Computer Science
    4. Skills: Python programming, C programming
    5. Projects: At least one relevant project in the field
    """
    return criteria

def check_eligibility(criteria, resume_text):
    messages = [
        {"role": "system", "content": "You are an AI assistant that evaluates resumes for internship eligibility."},
        {"role": "user", "content": f"Here are the internship criteria:\n{criteria}\n\nNow, evaluate the following resume and determine if the candidate is eligible for the internship.\n\nResume:\n{resume_text[:4000]}"}
    ]
    return chat_gpt(messages)

def main():
    pdf_path = "Resume.pdf"
    
    pdf_text = extract_text_from_pdf(pdf_path)
    
    
    criteria = set_internship_criteria()
    
   
    eligibility_result = check_eligibility(criteria, pdf_text)
    
    print("Eligibility Evaluation:")
    print(eligibility_result)

if __name__ == "__main__":
    main()
