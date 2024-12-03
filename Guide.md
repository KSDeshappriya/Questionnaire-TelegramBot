# Guide for Creating `.json` and `.env` Files

Here’s how you can create and set up the necessary JSON and `.env` files for the **Questionnaire Telegram Bot** project.

* * *

1\. **Creating the `.env` File**
--------------------------------

The `.env` file is used to store sensitive information like bot tokens and API keys securely. Follow these steps:

### File: `.env`

*   Create a file named `.env` in the root directory of your project.

### Structure of the `.env` File:

```bash
BOT_TOKEN=<your-telegram-bot-token>
API_ID=<your-telegram-api-id>
API_HASH=<your-telegram-api-hash>
GOOGLE_CREDENTIALS_PATH=credentials.json
FIREBASE_CREDENTIALS_PATH=serviceAccountKey.json
``` 

### Where to Get These Values:

1.  **`BOT_TOKEN`**:
    
    *   Get this from BotFather on Telegram when you create your bot.
2.  **`API_ID` and `API_HASH`**:
    
    *   Obtain these from Telegram's Developer Portal.
3.  **`GOOGLE_SERVICE_ACCOUNT_JSON`**:
    
    *   This should match the name of the JSON file for your Google Drive service account credentials (see below).
4.  **`FIREBASE_PROJECT_ID`**:
    
    *   Find this in the Firebase Console under **Project Settings**.

* * *

2\. **Creating the Google Drive Service Account JSON File**
-----------------------------------------------------------

This JSON file contains credentials for your bot to interact with Google Drive using the Drive API.

### Steps to Create the JSON File:

1.  Go to the Google Cloud Console.
2.  Create a new project or select an existing one.
3.  Enable the **Google Drive API** for your project:
    *   Navigate to **APIs & Services > Library**.
    *   Search for **Google Drive API** and enable it.
4.  Create a Service Account:
    *   Go to **APIs & Services > Credentials**.
    *   Click **Create Credentials > Service Account**.
5.  Download the JSON Key:
    *   After creating the service account, click on it in the **Credentials** page.
    *   Go to the **Keys** section and click **Add Key > Create New Key**.
    *   Select **JSON** as the key type and download the file.
6.  Save the file as `service_account.json` in the root directory of your project.

### Structure of the JSON File:

The downloaded JSON will look like this:

```json
{
  "type": "service_account",
  "project_id": "your-google-cloud-project-id",
  "private_key_id": "your-private-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account-email",
  "client_id": "your-service-account-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account-email"
}
``` 

> **Note**: Ensure this file is kept private and not committed to source control.

* * *

3\. **Setting Up Firebase JSON File**
-------------------------------------

To integrate Firebase, you’ll need to download a Firebase Admin SDK key.

### Steps to Create the Firebase Credentials JSON:

1.  Go to the Firebase Console.
2.  Select your project.
3.  Navigate to **Project Settings > Service Accounts**.
4.  Click **Generate New Private Key** and download the JSON file.
5.  Save the file as `firebase_credentials.json` in the root directory of your project.

### Structure of the JSON File:

The downloaded JSON will look like this:

```json
{
  "type": "service_account",
  "project_id": "your-firebase-project-id",
  "private_key_id": "your-private-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-abcde@your-project-id.iam.gserviceaccount.com",
  "client_id": "your-service-account-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-abcde@your-project-id.iam.gserviceaccount.com"
}
``` 

* * *

4\. **Verify and Test**
-----------------------

1.  Ensure both the `.env` file and JSON files (`serviceAccountKey.json` and `credentials.json`) are in the project directory.
2.  Test the bot by running:
    
    `python bot.py` 
    
3.  Check for successful integration with Google Drive and Firebase.
