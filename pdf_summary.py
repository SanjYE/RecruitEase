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

def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def main():
    pdf_path = "Resume.pdf"
    
    pdf_text = extract_text_from_pdf(pdf_path)
    
    prompt = f"Here's the text extracted from a PDF. please summarize the pdf\n\n{pdf_text[:4000]}" 
    
    response = chat_gpt(prompt)
    
    print(response)
    

if __name__ == "__main__":
    main()
