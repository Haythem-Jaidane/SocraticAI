import firebase_admin
from firebase_admin import credentials, firestore
import os

def init_firebase():
    """Initializes Firebase Admin SDK and returns the Firestore client."""
    if not firebase_admin._apps:
        # Use absolute path for service account key
        base_dir = os.path.dirname(os.path.abspath(__file__))
        cred_path = os.path.join(base_dir, '../../socraticai.json')
        
        if not os.path.exists(cred_path):
            raise FileNotFoundError(f"Firebase credentials not found at {cred_path}")
            
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    
    return firebase_admin.get_app(), firestore.client()

# Provide a globally accessible db client
_, db = init_firebase()