import PyPDF2
from openai import OpenAI
import os

client = OpenAI(
    api_key="***",   #hidden for security
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
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content.strip()

def check_company_eligibility(placement_data, resume_text):

    chunk_size = 4000  
    placement_chunks = [placement_data[i:i+chunk_size] for i in range(0, len(placement_data), chunk_size)]
    
    all_responses = []
    
    system_message = {
        "role": "system", 
        "content": "You are an AI assistant that analyzes placement data and resumes to determine company eligibility."
    }
    
    for i, chunk in enumerate(placement_chunks):
        messages = [
            system_message,
            {"role": "user", "content": f"Here's part {i+1} of the placement data:\n{chunk}\n\nAnalyze this data and keep it in memory."}
        ]
        chat_gpt(messages) 
    

    final_message = [
        system_message,
        {"role": "user", "content": f"Based on the placement data I've provided, and the following resume, list the companies this candidate is eligible for. Provide a brief explanation for each company.\n\nResume:\n{resume_text[:4000]}"}
    ]
    
    final_response = chat_gpt(final_message)
    return final_response

def main():
    placement_data_path = "pastcriteria.pdf"  #add paths to pdf. in this case my pdf was in same directory
    resume_path = "Resume.pdf"      #add paths to pdf. in this case my pdf was in same directory

    print("Extracting placement data...")
    placement_data = extract_text_from_pdf(placement_data_path)

    print("Extracting resume data...")
    resume_text = extract_text_from_pdf(resume_path)

    print("Analyzing eligibility...")
    eligibility_result = check_company_eligibility(placement_data, resume_text)
    
    print("\nEligibility Results:")
    print(eligibility_result)

if __name__ == "__main__":
    main()
