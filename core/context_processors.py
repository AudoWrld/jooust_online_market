import os

def google_client_id(request):
    return {
        "google_client_id": os.environ.get("GOOGLE_CLIENT_ID", "")
    }