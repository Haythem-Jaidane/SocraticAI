from .firestore_init import db

def get_all_users():
    users_ref = db.collection("App")
    docs = users_ref.stream()  # fetch all documents
    all_users = []
    for doc in docs:
        user_data = doc.to_dict()
        user_data["id"] = doc.id  # include document ID
        all_users.append(user_data)
    return all_users

def get_user_data(uid):
    """Fetches user data from Firestore by UID."""
    user_ref = db.collection("App").document(uid)
    doc = user_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None

def save_user_data(uid, data):
    """Saves or updates user data in Firestore."""
    db.collection("App").document(uid).set(data, merge=True)