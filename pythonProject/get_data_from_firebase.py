import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(
    "private_keys_to_be_ignored/beta-test-40bcf-firebase-adminsdk-c86jz-4448da56cd.json"
)
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_parcels_by_state_and_county(state, county):
    """Get parcels by specific state and county"""
    parcels_ref = db.collection("States").document(state).collection("Counties").document(county).collection("Parcels")
    docs = parcels_ref.stream()
    return [doc.to_dict() for doc in docs]

def get_parcels_by_state(state):
    """Get all parcels across all counties for a state"""
    counties_ref = db.collection("States").document(state).collection("Counties")
    all_parcels = []
    for county_doc in counties_ref.stream():
        parcels_ref = counties_ref.document(county_doc.id).collection("Parcels")
        parcels = parcels_ref.stream()
        all_parcels.extend(doc.to_dict() for doc in parcels)
    return all_parcels

# Example usage:
if __name__ == "__main__":
    state = "California"
    county = "Los Angeles"

    parcels_in_county = get_parcels_by_state_and_county(state, county)
    print(f"Parcels in {county}:", parcels_in_county)

    # parcels_in_state = get_parcels_by_state(state)
    # print(f"All parcels in {state}:", parcels_in_state)
