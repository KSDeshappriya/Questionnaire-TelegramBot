from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import mimetypes

# Initialize Google Drive API
def initialize_drive():
    from google.oauth2.service_account import Credentials
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file(
        os.getenv("GOOGLE_CREDENTIALS_PATH"), scopes=SCOPES)
    return build("drive", "v3", credentials=creds)

drive_service = initialize_drive()

def create_folder(name, parent_id=None):
    """Create a folder in Google Drive."""
    folder_metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_id:
        folder_metadata["parents"] = [parent_id]
    folder = drive_service.files().create(body=folder_metadata, fields="id").execute()
    return folder["id"]

def upload_file(file_path, folder_id):
    """Upload a file to a Google Drive folder."""
    file_metadata = {"name": os.path.basename(file_path), "parents": [folder_id]}
    media = MediaFileUpload(file_path, mimetype=mimetypes.guess_type(file_path)[0])
    file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    return file["id"]
