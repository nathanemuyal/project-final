import re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from firebase_admin import storage
import base64
from datetime import datetime
from email.utils import parsedate_to_datetime
from ai import sort_pdf


def write_email_info_to_db(user_ref, google_access_token):
    doc = user_ref.get()
    try:
        last_email_timestamp = doc.get('last_email')
    except KeyError:
        last_email_timestamp = None

    email_info = compile_emails(google_access_token, last_email_timestamp)
    write_email_info(user_ref, email_info)
    write_latest_email_timestamp(user_ref, email_info)

    
def compile_emails(google_access_token, timestamp):
    # steps:
    #     - verify google access token
    #     - create user entry if no already created
    #     - iterate over emails:
    #         - for each email:
    #             - store email from
    #             - for each attachment:
    #                 - if attachment is a pdf:
    #                     - download the pdf data
    #                     - run it through the ai
    #                     - add the data to a list of attachments (sorted data, attachment name, pdf url via email??)
    #             - add email data to list of email (email from, list of attachments)

    # Use the access token to query the Gmail API
    creds = Credentials(token=google_access_token)
    service = build('gmail', 'v1', credentials=creds)

    # Retrieve messages from the user's Gmail inbox
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=100).execute()
    messages = results.get('messages', [])


    time_format = "%a, %d %b %Y %H:%M:%S %z"
    latest_timestamp_dt = None
    if timestamp is not None:
        timestamp = clean_timestamp(timestamp)
        latest_timestamp_dt = datetime.strptime(timestamp, time_format)

    emails_infos = []
    # Iterate over each message
    for message in messages:
        message_id = message['id']
        msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        headers = msg['payload']['headers']

        # Extract the 'Date' and 'From' fields from headers
        email_from = None
        email_timestamp = None
        has_pdf_attachment = False
        pdf_url = None
        email_url = None
        

        for header in headers:
            if header['name'] == 'From':
                email_from = extract_email(header['value'])
            if header['name'] == 'Date':
                email_timestamp = header['value']


        

        email_timestamp = clean_timestamp(email_timestamp)
        this_email_timestamp_dt = datetime.strptime(email_timestamp, time_format)


        if latest_timestamp_dt is not None:
            if latest_timestamp_dt >= this_email_timestamp_dt:
                break

        email_attachments = []
        # Check for attachments
        if 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if part['mimeType'] == 'application/pdf':
                    has_pdf_attachment = True
                    pdf_filename = part.get('filename', 'Unknown filename')

                    # Get attachment data
                    attachment_id = part['body'].get('attachmentId')
                    if attachment_id:
                        # email_url = f"https://mail.google.com/mail/u/0/#inbox/{message_id}"
                        # pdf_url = f"https://mail.google.com/mail/u/0?ui=2&ik=&view=att&th={message['id']}&attid=0"

                        pdf_data = get_attachment_data(service, 'me', message_id, attachment_id)
                        pdf_data = base64.urlsafe_b64decode(pdf_data)
                        sorted_data = sort_pdf(pdf_data)
                        pdf_storage_url = upload_pdf_to_storage(pdf_data, pdf_filename)

                        sorted_data['pdf'] = pdf_storage_url
                        # sorted_data['pdf'] = pdf_url
                        # sorted_data['pdf'] = email_url

                        if sorted_data != None:
                            email_attachments.append(sorted_data)


        if has_pdf_attachment:
            emails_infos.append({
                'from': email_from,
                'timestamp': email_timestamp,
                'attachments': email_attachments
            })
    
    return emails_infos

def clean_timestamp(timestamp):
    pattern = r'^(.*?\d{2}:\d{2}:\d{2})\s*.*$'
    return re.sub(pattern, r'\1', timestamp)+' +0000'

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
    blob.upload_from_string(pdf_data, content_type="application/pdf")

    # Make the blob publicly accessible and return the public URL
    blob.make_public()
    return blob.public_url


def write_email_info(user_ref, email_infos):
    print('adding', len(email_infos), ' emails.')

    emails_ref = user_ref.collection('emails')
    for email_info in email_infos:
        emails_ref.add(email_info)

    
def write_latest_email_timestamp(user_ref, email_info):
    latest_timestamp = None

    for email in email_info:
        # Convert the timestamp string to a datetime object
        current_timestamp = datetime.strptime(email['timestamp'], "%a, %d %b %Y %H:%M:%S %z")

        # Update if this is the latest timestamp
        if latest_timestamp is None or current_timestamp > latest_timestamp:
            latest_timestamp = current_timestamp

    if latest_timestamp is not None:
        # if none that means no new emails -> don't update the timestamp
        user_ref.update({
            'last_email': latest_timestamp.strftime("%a, %d %b %Y %H:%M:%S %z")
        })