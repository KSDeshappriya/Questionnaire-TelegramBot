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
    """Create a folder in Google Drive or return the existing folder ID if it already exists."""
    # Check if the folder already exists
    query = f"mimeType='application/vnd.google-apps.folder' and name='{name}'"
    if parent_id:
        query += f" and '{parent_id}' in parents"

    # Search for the folder
    response = drive_service.files().list(q=query, fields="files(id)").execute()
    folders = response.get('files', [])

    if folders:
        # Folder already exists, return the ID of the existing folder
        return folders[0]['id']
    else:
        # Folder does not exist, create a new one
        folder_metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        if parent_id:
            folder_metadata["parents"] = [parent_id]
        
        folder = drive_service.files().create(body=folder_metadata, fields="id").execute()
        return folder["id"]

def upload_file(file_path, parent_folder_id):
    service = initialize_drive()
    
    file_metadata = {
        "name": os.path.basename(file_path),
        "parents": [parent_folder_id]  # Assign to the specific folder
    }
    media = MediaFileUpload(file_path, resumable=True)
    
    try:
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id"  # Request only the file ID
        ).execute()
        
        print(f"Uploaded file {file_path} with ID: {file.get('id')}")
        return file.get("id")  # Return the file ID
    except Exception as e:
        print(f"Error uploading file {file_path}: {e}")
        return None

def share_folder(folder_id):
    service = initialize_drive()

    permission = {
        "role": "reader",  # Can be 'reader' or 'writer'
        "type": "anyone"   # Makes the folder accessible to anyone with the link
    }

    try:
        service.permissions().create(
            fileId=folder_id,
            body=permission,
            fields="id"
        ).execute()
        print(f"Folder {folder_id} is now shared.")
        return folder_id
    except Exception as e:
        print(f"Error sharing folder: {e}")