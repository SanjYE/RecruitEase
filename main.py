import PyPDF2
from openai import OpenAI
import json
import random

client = OpenAI(
    api_key="***",  # Replace with your actual API key
)

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def chat_gpt(messages):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=messages
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in chat_gpt: {e}")
        return None

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

def generate_questions(company, skills):
    messages = [
        {"role": "system", "content": "You are an AI assistant that generates interview questions based on specific skills."},
        {"role": "user", "content": f"Generate 10 technical questions related to the following skills for {company}: {', '.join(skills)}. Format your response as a JSON array of objects, where each object has a 'question' and an 'answer' field."}
    ]
    response = chat_gpt(messages)
    if response is None:
        return []
    
    try:
        # Remove any text before and after the JSON content
        json_start = response.find("[")
        json_end = response.rfind("]") + 1
        json_str = response[json_start:json_end]
        return json.loads(json_str)
    except json.JSONDecodeError:
        print(f"Error: Unable to parse JSON response for {company}.")
        print(f"Response: {response}")
        return []


def evaluate_answer(question, expected_answer, user_answer):
    messages = [
        {"role": "system", "content": "You are an AI assistant that evaluates interview answers."},
        {"role": "user", "content": f"""
Compare the following:
Question: {question}
Expected Answer: {expected_answer}
User's Answer: {user_answer}

Rate the user's answer on a scale of 0 to 10, where 0 is completely incorrect and 10 is perfect.
Provide your rating and a brief explanation in the following format:
Rating: [0-10]
Explanation: [Your explanation here]
        """}
    ]
    response = chat_gpt(messages)
    if response is None:
        return 0
    
    try:
        rating = int(response.split('\n')[0].split(':')[1].strip())
        return rating
    except (ValueError, IndexError):
        print(f"Error: Unable to parse rating from response.")
        print(f"Response: {response}")
        return 0

def main():
    pdf_path = "Resume.pdf"
    json_path = "placement_criteria.json"
    
    pdf_text = extract_text_from_pdf(pdf_path)
    criteria = load_criteria_from_json(json_path)
    
    eligibility_result = check_eligibility(criteria, pdf_text)
    
    print("Eligibility Evaluation:")
    print(eligibility_result)
    
    eligible_companies = [company for company in criteria['companies'] if company['name'] in eligibility_result]
    
    if not eligible_companies:
        print("You are not eligible for any companies at this time.")
        return
    
    print("\nYou are eligible for the following companies:")
    for i, company in enumerate(eligible_companies, 1):
        print(f"{i}. {company['name']}")
    
    while True:
        try:
            choice = int(input("\nEnter the number of the company you want to be assessed for: ")) - 1
            if 0 <= choice < len(eligible_companies):
                selected_company = eligible_companies[choice]
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
    
    print(f"\nAssessment for {selected_company['name']}:")
    questions = generate_questions(selected_company['name'], selected_company['criteria']['skills'])
    
    if not questions:
        print(f"Unable to generate questions for {selected_company['name']}. Ending assessment.")
        return
    
    total_score = 0
    for i, q in enumerate(questions, 1):
        print(f"\nQuestion {i}: {q['question']}")
        user_answer = input("Your answer: ")
        score = evaluate_answer(q['question'], q['answer'], user_answer)
        total_score += score
        print(f"Score for this question: {score}/10")
    
    average_score = total_score / len(questions)
    if average_score>=7:
        print("Congratulations, you have passed one round 1")
    else:
        print("you have failed the test")

if __name__ == "__main__":
    main()
