# import ollama
import fitz  # PyMuPDF
import google.generativeai as genai
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


def download_pdf_data(pdf_url):
    pass


def sort_user_emails(user_ref):
    # for each
    model = genai.GenerativeModel('gemini-1.5-flash')

    pdf_text = extract_text_from_pdf('../test-pdfs/2024-470754526_20240520_200237.pdf')
    
    prompt = f"""
    Analyze the following text and determine whether it is an invoice or a receipt.
    If it is, extract the following details and provide the response in the following format:

    - Type: [Invoice or Receipt or none]
    - Issue Date: [Date and time of issuance]
    - Billing Company: [Name of the billing company]
    - Amount: [Invoice amount]
    - Currency: [Currency (e.g., USD, ILS, or any other currency)]
    - Category: [Category of the expense from the following options: property tax, energy, communication, health, sewage bill, other]

    Text:
    {pdf_text}

    """

    response = model.generate_content(prompt)
    print(response.text)


# sort_user_emails('h')