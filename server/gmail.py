import re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from firebase_admin import storage
import base64


def write_email_info_to_db(user_ref, google_access_token):
    email_info = compile_emails(google_access_token)
    write_email_info(user_ref, email_info)

    
def compile_emails(google_access_token):
    # Use the access token to query the Gmail API
    creds = Credentials(token=google_access_token)
    service = build('gmail', 'v1', credentials=creds)

    # Retrieve messages from the user's Gmail inbox
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=15).execute()
    messages = results.get('messages', [])

    emails_infos = []

    # Iterate over each message
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        headers = msg['payload']['headers']

        # Extract the 'Date' and 'From' fields from headers
        email_from = None
        email_timestamp = None
        has_pdf_attachment = False
        pdf_url = None
        

        for header in headers:
            if header['name'] == 'From':
                email_from = extract_email(header['value'])
            if header['name'] == 'Date':
                email_timestamp = header['value']
        

        # Check for attachments
        if 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if part['mimeType'] == 'application/pdf':
                    has_pdf_attachment = True
                    pdf_filename = part.get('filename', 'Unknown filename')

                    # Get attachment data
                    attachment_id = part['body'].get('attachmentId')
                    if attachment_id:
                        pdf_data = get_attachment_data(service, 'me', message['id'], attachment_id)
                        pdf_url = upload_pdf_to_storage(pdf_data, pdf_filename)

                    break  # Exit loop after finding the first PDF attachment

        if has_pdf_attachment:
            emails_infos.append({
                'from': email_from,
                'timestamp': email_timestamp,
                'pdf': pdf_url,
            })
    

    return emails_infos

def extract_email(email_from):
    # Regular expression to extract the email address from the 'From' field
    match = re.search(r'<(.+?)>', email_from)
    return match.group(1)  # Return the email address between the < and >


def get_attachment_data(service, user_id, message_id, attachment_id):
    attachment = service.users().messages().attachments().get(userId=user_id, messageId=message_id, id=attachment_id).execute()
    data = attachment.get('data', '')
    return data


def upload_pdf_to_storage(pdf_data, filename):
    # Get a reference to the storage bucket
    bucket = storage.bucket()

    # Create a new blob (file) in the storage bucket
    blob = bucket.blob(f"pdfs/{filename}")

    # Upload the PDF data (decoded) to the bucket
    blob.upload_from_string(base64.urlsafe_b64decode(pdf_data), content_type="application/pdf")

    # Make the blob publicly accessible and return the public URL
    blob.make_public()
    return blob.public_url


def write_email_info(user_ref, email_infos):
    delete_subcollection(user_ref, 'beforeCheck')
    before_check_ref = user_ref.collection('beforeCheck')
    for email_info in email_infos:
        before_check_ref.add(email_info)


def delete_subcollection(user_ref, subcollection_name):
    # Get a reference to the subcollection
    subcollection_ref = user_ref.collection(subcollection_name)
    
    # Retrieve all documents in the subcollection
    docs = subcollection_ref.stream()
    
    # Delete each document in the subcollection
    for doc in docs:
        doc.reference.delete()