import firebase_admin
from firebase_admin import credentials, firestore

# Initialize the app with a service account, granting admin privileges
cred = credentials.Certificate('invoic-ia-firebase-adminsdk-1zi97-3b9fa29923.json')  # Replace with the path to your service account JSON file
firebase_admin.initialize_app(cred)

# Initialize Firestore DB
db = firestore.client()

def user_login(user_email, display_name):
    if check_user_exists(user_email):
        pass
    else:
        add_new_user(user_email, display_name)


def add_new_user(user_email, display_name):
    # Data for the new user
    new_user = {
        'createdAt': firestore.SERVER_TIMESTAMP,  # Use Firestore's server timestamp,
        'displayName': display_name,
        'email': user_email
    }

    # Add the user to the 'users' collection
    doc_ref = db.collection('users').add(new_user)

    # Get the document ID of the newly created user
    user_doc_id = doc_ref[1].id

    # Create 'beforeCheck' and 'afterCheck' subcollections for the user
    before_check_ref = db.collection('users').document(user_doc_id).collection('beforeCheck')
    after_check_ref = db.collection('users').document(user_doc_id).collection('afterCheck')

    # Optionally, you can add initial documents to the subcollections
    before_check_ref.add({'status': 'not_started'})
    after_check_ref.add({'status': 'not_started'})

    # Confirm the operation
    print(f"Added user with ID: {doc_ref[1].id}")


def check_user_exists(email):
    # Query the 'users' collection where the email field matches
    users_ref = db.collection('users')
    query = users_ref.where('email', '==', email).get()

    # If the query returns a document, the user exists
    if len(query) > 0:
        user_doc = query[0]  # Get the first document that matches
        print(f"User exists with ID: {user_doc.id}")
        return True
    else:
        print("User does not exist.")
        return False