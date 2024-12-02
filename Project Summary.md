### **Project Summary**

You want a **Telegram bot** with the following functionality:

1.  **Questionnaire**:
    
    *   The bot will ask **10-15 questions** (customizable).
    *   Answers to most questions are **text-based**, while the last few will involve uploading images.
2.  **File Management**:
    
    *   Answers and images will be saved in a structured **folder hierarchy** based on the **first answer** (e.g., "Bat," "Ball," "Car").
    *   Subfolders will be named sequentially (e.g., `Bat 1`, `Bat 2`) under a parent folder like `Bat`.
    *   All data will be stored on **Google Drive**.
3.  **Unique Identification**:
    
    *   A **unique ID** will be generated for each completed response.
    *   The text file with answers will be named after this unique ID.
    *   The bot will send the unique ID to the user as a confirmation.
4.  **One-Time Response Per User**:
    
    *   The bot will ensure users cannot submit the form more than once.
5.  **Admin Panel**:
    
    *   Admins can:
        *   **Add, delete, or modify questions**.
        *   View or filter user responses by categories (e.g., "Bat," "Ball," "Car").
