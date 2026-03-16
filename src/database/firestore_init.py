import firebase_admin
from firebase_admin import credentials, firestore
import os

def init_firebase():
    """Initializes Firebase Admin SDK and returns the Firestore client."""
    if not firebase_admin._apps:
        # Use absolute path for service account key
        cred_dict = dict(st.secrets["FIREBASE_KEY"])
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    
    return firebase_admin.get_app(), firestore.client()

# Provide a globally accessible db client
_, db = init_firebase()