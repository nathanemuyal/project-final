from io import BytesIO
from flask import Flask, request, redirect, jsonify, send_file
import requests
from google.cloud.firestore_v1.base_query import FieldFilter
from flask_cors import CORS
from dotenv import load_dotenv
import os
load_dotenv()


from firebase import user_login, compile_sorted_data
from gmail import write_email_info_to_db

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


    # Step 2: Retrieve user email using the access token
    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo?alt=json'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    userinfo_response = requests.get(userinfo_url, headers=headers)
    user_info = userinfo_response.json()

    # Get the user's email and display name from the response
    user_email = user_info.get('email')
    display_name = user_info.get('name')  # This retrieves the display name

    if not user_email or not display_name:
        return jsonify({'error': 'Failed to obtain user email and display name'}), 400

    handle_user(access_token, user_email, display_name)
    #logout or close the browser
    return redirect(f'http://localhost:3000/?token={access_token}')


@app.route('/get_pdf', methods=['POST'])
def get_pdf():
    data = request.json
    access_token = data.get('access_token')
    if not access_token:
        return jsonify({'error': 'Missing access token'}), 400
    pdf_url = data.get('pdf_url')
    if not pdf_url:
        return jsonify({'error': 'Missing pdf url'}), 400
    











    """
    Downloads an attachment from Gmail using the access token and private URL.
    
    :param access_token: The OAuth2 access token with Gmail scopes.
    :param private_url: The private URL of the attachment.
    :param save_path: Path to save the downloaded attachment.
    :return: None
    """
    # Add the authorization header
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Make a GET request to the private URL
    response = requests.get(pdf_url, headers=headers, stream=True)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Write the content to the specified file
        with open('temp.pdf', "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Attachment downloaded successfully to {'temp.pdf'}")
    else:
        print(f"Failed to download attachment. Status code: {response.status_code}")
        print(response.text)





    return jsonify({'success': 'worked'}), 200


@app.route('/get_profile_pic', methods=['POST'])
def get_profile_pic():
    data = request.json
    access_token = data.get('access_token')

    if not access_token:
        return jsonify({'error': 'Missing access token'}), 400

    # Get user info including profile picture URL
    user_info = get_user_info(access_token)
    
    if not user_info:
        return jsonify({'error': 'Failed to retrieve user info'}), 500

    profile_pic_url = user_info.get('picture')

    # Return the profile picture URL
    return jsonify({'profile_pic_url': profile_pic_url})


def get_user_info(access_token):
    """Get user info from Google API using access token."""
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    userinfo_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
    response = requests.get(userinfo_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


def handle_user(access_token, user_email, display_name):
    user_ref = user_login(user_email, display_name)

    # emails collection
    write_email_info_to_db(user_ref, access_token)

    delete_non_invoice_or_reciept_emails(user_ref)


def delete_non_invoice_or_reciept_emails(user_ref):
    emails_ref = user_ref.collection('emails')
    emails = emails_ref.stream()

    for email in emails:
        email_data = email.to_dict()
        email_id = email.id

        # Check if 'attachments' exists and is a list
        if 'attachments' in email_data and isinstance(email_data['attachments'], list):
            original_attachments = email_data['attachments']
            # Filter out attachments where 'type' is 'null'
            updated_attachments = [att for att in original_attachments if att.get('type') != 'null']

            if not updated_attachments:
                # If updated_attachments is empty aka all of type 'null', delete the document
                emails_ref.document(email_id).delete()
                print(f"Deleted email ID {email_id} as all attachments were removed")

            # If there are changes, update the document
            elif original_attachments != updated_attachments:
                emails_ref.document(email_id).update({
                    'attachments': updated_attachments
                })
                print(f'removed {len(original_attachments) - len(updated_attachments)} from attachements for email.')


@app.route('/sort', methods=['POST'])
def sort_data():
    # Parse the incoming JSON request
    req_data = request.get_json()
    access_token = req_data.get('access_token')
    category = req_data.get('category')

    # Step 1: Get user information using Google access token
    user_info = get_user_info(access_token)

    if user_info is None:
        return jsonify({"error": 'could not get user info'}), 401

    user_email = user_info.get('email')

    if not user_email:
        return jsonify({"error": "Could not retrieve email from token"}), 401

    # TODO update the compile_sorted_data method
    data = compile_sorted_data(user_email, category)

    return data, 200


if __name__ == '__main__':
    app.run(debug=True)
