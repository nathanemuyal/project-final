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
from ai import sort_user_emails

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
    return redirect(f'http://localhost:3000/?token={access_token}')


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

    # beforeCheck
    write_email_info_to_db(user_ref, access_token)

    # afterCheck
    sort_user_emails(user_ref)

    # delete non relevent email documents
    delete_non_invoice_or_reciept_emails(user_ref)


def delete_non_invoice_or_reciept_emails(user_ref):
    # Get the afterCheck subcollection
    after_check_ref = user_ref.collection('afterCheck')
    
    # Create a query to find documents where type == 'null'
    query = after_check_ref.where(filter=FieldFilter('sorted_data.type', '==', 'null'))
    
    # Get all matching documents
    docs = query.stream()
    
    # Delete each matching document
    for doc in docs:
        doc.reference.delete()


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

    data = compile_sorted_data(user_email, category)

    return data, 200


if __name__ == '__main__':
    app.run(debug=True)