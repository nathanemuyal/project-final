import base64
from flask import Flask, request, redirect, jsonify
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from flask_cors import CORS
from dotenv import load_dotenv
import os
load_dotenv()


from firebase import user_login
import concurrent.futures


# Create a thread pool executor
executor = concurrent.futures.ThreadPoolExecutor(max_workers=100)

app = Flask(__name__)
CORS(app)

# Your Google credentials
CLIENT_ID = os.getenv('REACT_APP_CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:5000/auth/callback'  # Redirect URI in Google Cloud settings
TOKEN_URL = 'https://oauth2.googleapis.com/token'

@app.route('/auth/callback')
def oauth2callback():
    # Get the authorization code from the request
    code = request.args.get('code')
    if not code:
        return 'Authorization code not found', 400

    # Exchange the authorization code for access and refresh tokens
    token_data = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }

    # Exchange the code for tokens
    token_response = requests.post(TOKEN_URL, data=token_data)
    token_json = token_response.json()

    if 'access_token' not in token_json:
        return jsonify({'error': 'Failed to obtain access token'}), 400

    access_token = token_json['access_token']

    executor.submit(handle_user, access_token)
    return redirect(f'http://localhost:3000/?token={access_token}')


    # # Use the access token to query the Gmail API
    # creds = Credentials(token=access_token)
    # service = build('gmail', 'v1', credentials=creds)

    # # Retrieve messages from the user's Gmail inbox
    # results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=25).execute()
    # messages = results.get('messages', [])

    # emails = []
    # for message in messages:
    #     msg = service.users().messages().get(userId='me', id=message['id']).execute()
    #     headers = msg['payload']['headers']
    #     parts = msg['payload'].get('parts', [])

    #     # Find the subject in the headers
    #     subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')
        
    #     attachments = []
    #     for part in parts:
    #         filename = part.get('filename')
    #         mime_type = part.get('mimeType')
    #         body = part.get('body')
            
    #         if 'attachmentId' in body:
    #             attachment_id = body['attachmentId']
    #             attachment = service.users().messages().attachments().get(userId='me', messageId=message['id'], id=attachment_id).execute()


    #             data = attachment.get('data')
                
    #             if data:
    #                 # Decode the base64 encoded attachment data
    #                 data = base64.urlsafe_b64decode(data.encode('UTF-8'))
    #                 attachments.append({
    #                     'filename': filename,
    #                     'mimeType': mime_type,
    #                 })

    #     emails.append({
    #         'subject': subject,
    #         'attachments': attachments
    #     })
    
    # resp = jsonify(success=True)
    # return resp



def handle_user(access_token):
    import time
    time.sleep(10)
    user_login(access_token)

@app.teardown_appcontext
def shutdown_thread_pool(exception=None):
    # Shutdown the ThreadPoolExecutor when the app is closing
    print("Shutting down thread pool...")
    executor.shutdown(wait=False)  # wait=False allows shutting down immediately without waiting for tasks to finish
    print("Thread pool shut down.")


if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        shutdown_thread_pool()  # Ensure thread pool shutdown when Flask stops
