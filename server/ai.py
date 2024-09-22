from firebase_admin import storage, firestore, credentials
import io
import re
import time
import fitz  # PyMuPDF
import google.generativeai as genai
import requests
from dotenv import load_dotenv
import os
load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def extract_text_from_pdf(pdf_path):
    extracted_text = ""
    
    # Open the PDF file
    doc = fitz.open(pdf_path)
    
    # Loop through each page and extract text
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)  # Load each page by number
        text = page.get_text("text")  # Extract the text in plain format
        extracted_text += f"Page {page_num + 1} Text:\n{text}\n"
    
    # Close the document
    doc.close()
    
    return extracted_text


def download_pdf_from_firebase(pdf_url):
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()  # Raise an error for bad responses
        pdf_data = io.BytesIO(response.content)  # Create a BytesIO object from the content
        return pdf_data
    except Exception as e:
        print(f"Error downloading PDF: {e}")
        return None


def sort_user_emails(user_ref):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Analyze the following text and determine whether it is an invoice or a receipt.
    If it is, extract the following details and provide the response in the following format:

    - Type: [Invoice or Receipt]
    - Issue Date: [Date and time of issuance]
    - Billing Company: [Name of the billing company]
    - Amount: [Invoice amount]
    - Currency: [Currency (USD, ILS, or any other currency)]
    - Category: [Category of the expense from the following options: property tax, energy, communication, health, sewage bill, other]

    if you are unsure about an item just write null.
    DO NOT add additional infomation. just use what is provided in the square brackets.
    put a ';' at the end of each item line.
    
    Text:
    """

    before_check_ref = user_ref.collection('beforeCheck')
    after_check_write_counter = 0
    
    # Iterate over the documents in the 'beforeCheck' subcollection
    for doc in before_check_ref.stream():
        # Access the 'pdf' field in each document
        pdf_url = doc.to_dict().get('pdf')
        pdf_bytes = download_pdf_from_firebase(pdf_url)
        if not pdf_bytes:
            continue
        with fitz.open("pdf", pdf_bytes) as pdf:
            all_text = ""
            
            # Iterate through all pages and extract text
            for page in pdf:
                all_text += page.get_text() + "\n"  # Add a newline for separation

            time.sleep(2)
            response = model.generate_content(prompt + '\n' + all_text)

            extracted_sorted_data = extract_data(response.text)
            if not extracted_sorted_data:
                print('the llm did not return the desired format.', response.text)
            else:
                write_sorted_email_info(user_ref, pdf_url, extracted_sorted_data)
                after_check_write_counter += 1

    
    print('wrote', after_check_write_counter, 'to afterCheck')
    # delete the beforeCheck subcollection as it's not needed anymore
    delete_subcollection(user_ref, 'beforeCheck')
    print('deleted the beforeCheck subcollection')


def extract_data(text: str):
    # Define the regex pattern
    pattern = r"- Type: (.+?);.*?- Issue Date: (.+?);.*?- Billing Company: (.+?);.*?- Amount: (.+?);.*?- Currency: (.+?);.*?- Category: (.+?);"
    
    match = re.search(pattern, text, re.DOTALL)

    if match:
        # Extract the matched groups and return them in a dictionary
        return {
            "type": match.group(1),
            "issue_date": match.group(2),
            "billing_company": match.group(3),
            "amount": match.group(4),
            "currency": match.group(5),
            "category": match.group(6)
        }
    else:
        return None



def write_sorted_email_info(user_ref, pdf_url, sorted_email_info):
    # Get a reference to the 'afterCheck' subcollection
    after_check_ref = user_ref.collection('afterCheck')
    
    after_check_ref.add({
        'pdf': pdf_url,
        'sorted_data': sorted_email_info
    })


def delete_subcollection(user_ref, subcollection_name):
    # Get a reference to the subcollection
    subcollection_ref = user_ref.collection(subcollection_name)
    
    # Retrieve all documents in the subcollection
    docs = subcollection_ref.stream()
    
    # Delete each document in the subcollection
    for doc in docs:
        doc.reference.delete()