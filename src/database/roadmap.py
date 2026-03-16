from .firestore_init import db

from .firestore_init import db
import streamlit as st

def add_roadmap(uid, roadmap):
    """Saves the roadmap to the user's document in Firestore."""
    try:
        # Handle if roadmap is the full response dict or just the list
        if isinstance(roadmap, dict) and "plan" in roadmap:
            weeks = roadmap["plan"]
        elif isinstance(roadmap, list):
            weeks = roadmap
        else:
            raise ValueError("Invalid roadmap data format")

        clean_roadmap = []
        for item in weeks:
            if hasattr(item, "dict"):
                clean_roadmap.append(item.dict())
            else:
                clean_roadmap.append(dict(item))

        db.collection("App").document(uid).set(
            {"roadmap": clean_roadmap}, 
            merge=True
        )
        return True
    except Exception as e:
        st.error(f"Firestore Error: {e}")
        print(f"Firestore Error: {e}")
        return False
