from flask import Flask, jsonify, request
from firebase_admin import credentials, firestore, initialize_app
import openai
import base64
import PyPDF2
from io import BytesIO

app = Flask(__name__)

# אתחול Firebase
cred = credentials.Certificate('')
initialize_app(cred)
db = firestore.client()

# מפתח ה-API של OpenAI
openai.api_key = ''

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    data = request.get_json()
    pdf_content = base64.b64decode(data['pdf'])
    pdf_text = extract_text_from_pdf(pdf_content)
    
    # בקשה ל-ChatGPT
    prompt = f"""
    Analyze the following text and determine whether it is an invoice or a receipt.
    If it is, extract the following details and provide the response in the following format:

    - Type: [Invoice or Receipt or not]
    - Issue Date: [Date and time of issuance]
    - Billing Company: [Name of the billing company]
    - Amount: [Invoice amount]
    - Currency: [Currency (e.g., USD, ILS, or any other currency)]
    - Category: [Category of the expense (e.g., property tax, energy, communication, health, sewerage charge, other)]

    Text:
    {pdf_text}
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )

    result = response.choices[0].text.strip()

    # הוספת תוצאות ChatGPT לנתונים המקוריים
    data['analysis'] = result
    
    # עדכון הקולקציות ב-Firestore
    if 'invoice' in result.lower() or 'receipt' in result.lower():
        before_check_ref = db.collection('users').document(data['user_id']).collection('beforeCheck').document(data['doc_id'])
        after_check_ref = db.collection('users').document(data['user_id']).collection('afterCheck').document(data['doc_id'])
        
        before_check_data = before_check_ref.get().to_dict()
        if before_check_data:
            after_check_ref.set({**before_check_data, **data})
            before_check_ref.delete()

    return jsonify({'message': 'ה-PDF עובד והועבר ל-afterCheck אם נדרש.'})

def extract_text_from_pdf(pdf_content):
    pdf_reader = PyPDF2.PdfFileReader(BytesIO(pdf_content))
    text = ""
    for page in range(pdf_reader.getNumPages()):
        text += pdf_reader.getPage(page).extractText()
    return text

if __name__ == '__main__':
    app.run(debug=True)
