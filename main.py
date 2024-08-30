import PyPDF2
from openai import OpenAI
import json

client = OpenAI(
    api_key="***",    #hidden for security
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

def load_criteria_from_json(json_path):
    with open(json_path, 'r') as file:
        return json.load(file)

def check_eligibility(criteria, resume_text):
    companies_criteria = json.dumps(criteria['companies'], indent=2)
    messages = [
        {"role": "system", "content": "You are an AI assistant that evaluates resumes for job eligibility based on company criteria."},
        {"role": "user", "content": f"""
Here are the criteria for multiple companies:
{companies_criteria}

Evaluate the following resume against each company's criteria. Determine if the candidate is eligible for each company's position. 
Provide a list of companies the candidate is eligible for, along with brief explanations.
If the candidate is not eligible for any company, explain why.

Resume:
{resume_text[:4000]}

Your response should be in the following format:
Eligible Companies:
1. [Company Name] - [Brief explanation of eligibility]
2. [Company Name] - [Brief explanation of eligibility]
...

If not eligible for any:
Not eligible for any companies. Reasons:
- [Reason 1]
- [Reason 2]
...
        """}
    ]
    return chat_gpt(messages)

def main():
    pdf_path = "Resume.pdf"
    json_path = "placement_criteria.json"
    
    pdf_text = extract_text_from_pdf(pdf_path)
    criteria = load_criteria_from_json(json_path)
    
    eligibility_result = check_eligibility(criteria, pdf_text)
    
    print("Eligibility Evaluation:")
    print(eligibility_result)

if __name__ == "__main__":
    main()
