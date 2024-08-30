import PyPDF2
import os

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def save_text_to_file(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)
        

def main():
    pdf_path = "placements.pdf"
    output_path = "placements.txt"
    
  
    pdf_text = extract_text_from_pdf(pdf_path)
  
    save_text_to_file(pdf_text, output_path)
    
    


if __name__ == "__main__":
    main()