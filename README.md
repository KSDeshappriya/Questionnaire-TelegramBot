Questionnaire Telegram Bot
==========================
*( with Web Dashboard for admin using Flask )*

A **Telegram bot** built with **Python** that collects user responses through a questionnaire, uploads text-based answers and images to Google Drive, and manages the data in Firebase. This bot supports features like user input validation, data categorization, and admin controls.

* * *

Features
--------

1.  **Dynamic Questionnaire**:
    
    *   The bot dynamically fetches questions from Firebase.
    *   Supports text-based and image-based questions.
2.  **Categorized Data Storage**:
    
    *   User responses and uploaded images are categorized based on the first answer.
    *   Data is stored in structured Google Drive folders.
3.  **Unique Submission IDs**:
    
    *   Each submission gets a unique ID that is sent to the user as confirmation.
4.  **Admin Controls**:
    
    *   Admins can:
        *   Add, edit, or delete questions.
        *   View and filter user responses via Firebase.
5.  **One-Time Submission**:
    
    *   Prevents users from submitting the questionnaire multiple times.
6.  **Cloud Integration**:
    
    *   Text files and images are uploaded to Google Drive.
    *   Submission metadata is saved in Firebase.

* * *

Prerequisites
-------------

1.  **Python 3.8 or later** installed on your machine.
2.  **Firebase Project**:
    *   Create a Firebase project.
    *   Enable Firestore Database.
3.  **Google Cloud Service Account**:
    *   Create a service account with Drive API enabled.
    *   Download the service account JSON key file.
4.  **Telegram Bot Token**:
    *   Obtain a bot token from BotFather on Telegram.

* * *

Installation
------------

1.  **Clone the repository**:
    
    ```cmd
    git clone https://github.com/KSDeshappriya/Questionnaire-TelegramBot.git
    cd Questionnaire-TelegramBot
    ``` 
    
2.  **Set up a virtual environment**:
    
    ```cmd
    python -m venv .venv
    source .venv/bin/activate # On Windows, use `.venv\Scripts\activate` 
    ```
    
3.  **Install dependencies**:
    
    ```bash
    pip install -r requirements.txt
    ``` 
    or
    ```bash
    pip install pyrogram firebase-admin google-api-python-client flask python-dotenv
    ```
    
4.  **Configure environment variables**:
    
    *   Create a `.env` file in the project root:
        
        ```bash
        BOT_TOKEN=<your-telegram-bot-token>
        API_ID=<your-telegram-api-id>
        API_HASH=<your-telegram-api-hash>
        GOOGLE_SERVICE_ACCOUNT_JSON=service_account.json
        FIREBASE_PROJECT_ID=<your-firebase-project-id>
        ```
        
    *   Replace the placeholders with actual values.
5.  **Add Firebase credentials**:
    
    *   Place the downloaded Firebase JSON key file in the project root and name it `firebase_credentials.json`.
6.  **Enable Drive API**:
    
    *   Follow the instructions here to enable the Google Drive API.

* * *

Running the Bot
---------------

1.  Activate the virtual environment:
    
    `source .venv/bin/activate` 
    
2.  Start the bot:
    
    `python bot.py` 
    
3.  Interact with your bot on Telegram to test the functionality.
    
* * *

Running the Admin Dashboard
---------------

1.  Activate the virtual environment:
    
    `source .venv/bin/activate` 
    
2.  Start the bot:
    
    `python admin_panel.py` 
    
3.  Interact with your bot on Telegram to test the functionality.

* * *

Folder Structure
----------------

The bot categorizes data as follows:

*   **Parent Folder**: Based on the first question's response (e.g., `Bat`, `Ball`, `Car`).
*   **Subfolder**: Unique ID for each submission (e.g., `Bat-123456`).
    *   Contains a `.txt` file with answers.
    *   Contains uploaded images.

* * *

Firebase Integration
--------------------

The bot saves the following metadata to Firebase:

*   User ID
*   Unique Submission ID
*   Folder ID on Google Drive
*   Text responses
*   Uploaded image file IDs (Google Drive file IDs)

* * *

Admin Panel (Basic)
-------------------

Admins can use Firebase to:

*   Add, edit, or delete questions in the `questions` collection.
*   View responses categorized by submission IDs.

* * *

Troubleshooting
---------------

### Common Errors

1.  **Google Drive 404 Error**:  
    Ensure the service account has sufficient permissions to access the specified Drive folders.
    
2.  **Firebase KeyError**:  
    Verify that Firebase keys and collection paths are configured correctly.
    
3.  **Pyrogram API Key Error**:  
    Ensure your API ID and API Hash are correct in the `.env` file.
    

* * *

License
-------

This project is licensed under the [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) License.

* * *

Contributions
-------------

Feel free to open issues and submit pull requests for improvements or bug fixes.

* * *

Author
------

[KSDeshappriya](https://github.com/KSDeshappriya/)  
If you have any questions or feedback, please feel free to reach out!