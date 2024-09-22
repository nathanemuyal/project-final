import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter


# Initialize the app with a service account, granting admin privileges
cred = credentials.Certificate('invoic-ia-firebase-adminsdk-1zi97-2040a20591.json')  # Replace with the path to your service account JSON file
firebase_admin.initialize_app(cred, {'storageBucket': 'invoic-ia.appspot.com'})

# Initialize Firestore DB
db = firestore.client()

def user_login(user_email, display_name):
    if not check_user_exists(user_email):
        add_new_user(user_email, display_name)

    users_ref = db.collection('users')
    query = users_ref.where(filter=FieldFilter('email', '==', user_email)).limit(1).get()

    user_doc = query[0]
    return user_doc.reference


def add_new_user(user_email, display_name):
    # Data for the new user
    new_user = {
        'createdAt': firestore.SERVER_TIMESTAMP,  # Use Firestore's server timestamp,
        'displayName': display_name,
        'email': user_email
    }
    # Add the user to the 'users' collection
    doc_ref = db.collection('users').add(new_user)

    # Confirm the operation
    print(f"Added user with ID: {doc_ref[1].id}")


def check_user_exists(email):
    # Query the 'users' collection where the email field matches
    users_ref = db.collection('users')
    query = users_ref.where(filter=FieldFilter('email', '==', email)).get()

    # If the query returns a document, the user exists
    if len(query) > 0:
        user_doc = query[0]  # Get the first document that matches
        return True
    else:
        return False