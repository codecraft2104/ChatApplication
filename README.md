ChatApplication
This chat application is messaging app to communicate with others like whatsapp and Email.
"# ChatApplication" 

HG Chat Application Documentation
1. Project Title

HG Chat Application

A real-time chat application developed using Django that enables users to register, log in, manage contacts, and exchange messages securely.


2. Project Overview

The HG Chat Application is a web-based messaging platform designed to facilitate communication between registered users. The system provides user authentication, contact management, and chat functionality through a user-friendly interface.

Features

*   User Registration
  
*   User Login & Logout
  
*   Contact Management
  
*   One-to-One Messaging
  
*   Chat History  
  
*   Responsive User Interface
  
*   Secure Authentication


3. Technologies Used
   
i.  Python	-  Backend Development

ii.  Django  -  	Web Framework

iii.  HTML5  -	Frontend Structure

iv.  CSS3  - 	Styling

v.  Bootstrap  -	Responsive Design

vi.  JavaScript  -	Client-side Interaction

vii.  SQLite/MySQL  -	Database

viii.  Git & GitHub  -	Version Control


4. System Requirements
   
*  Software Requirements
  
  -  Python 3.10 or higher
    
  -  Django 5.x or higher
    
  -  git
    
  -  VS Code or any IDE
    
  -  Web Browser (Chrome, Firefox, Edge)

*  Hardware Requirements

  -  Minimum 4 GB RAM
    
  -  Dual Core Processor
    
  -  500 MB Free Disk Space

    
5. Project Structure

<img width="200" height="400" alt="image" src="https://github.com/user-attachments/assets/d05c92fa-7506-4dc0-b511-a8590f40359c" />


6. Installation Steps
   
  --  Step 1: Download the Project
  
  Option A: Clone from GitHub

    git clone https://github.com/yourusername/hg_chat.git
    
  Option B: Download ZIP
  
    -  Open GitHub Repository.
    
    -  Click Code.
    
    -  Select Download ZIP.
    
    -  Extract the ZIP file.

  <img width="700" height="400" alt="image" src="https://github.com/user-attachments/assets/c3f47693-9fb1-426d-b956-dbbbfc1f29e8" />

  --  Step 2: Open Project

Open terminal in the project directory.

    cd hg_chat

<img width="700" height="400" alt="image" src="https://github.com/user-attachments/assets/f42e8014-2775-45e2-8ed1-30bb0af1f51c" />

  --  Step 3: Create Virtual Environment

  Windows
      
    python -m venv env

  Activate Environment:

    env\Scripts\activate

  Linux/Mac

    python3 -m venv env
    
    source env/bin/activate

  <img width="500" height="150" alt="image" src="https://github.com/user-attachments/assets/2bd6773d-9ba0-407e-8a8f-3fe20da0af11" />

  --  Step 4: Install Dependencies

  Install required packages:

    pip install -r requirements.txt

  If requirements.txt is unavailable:

    pip install django

  --  Step 5: Configure Database

  Apply migrations:

    python manage.py makemigrations
    python manage.py migrate
    
  --  Step 6: Create Superuser

    python manage.py createsuperuser

  Enter:

    Username
    Email
    Password

  --  Step 7: Run the Server

    python manage.py runserver

  Output:

    Starting development server at
    http://127.0.0.1:8000/

  <img width="904" height="555" alt="image" src="https://github.com/user-attachments/assets/760411e9-fa9c-459c-bde1-4eebc5062f64" />


7. Execution Steps

  Open browser:


    http://127.0.0.1:8000/


User Workflow

  1. Register New Account
  
  2. Login
    
  3. Add Contacts
    
  4. Open Chat Window
     
  5. Send Messages
      
  6. View Chat History
      
  7. Logout


 ** --  Login Page**

<img width="1365" height="727" alt="image" src="https://github.com/user-attachments/assets/537d4934-9e88-426b-893a-d76ad7d31e42" />

**  --  Registration Page**

<img width="1348" height="726" alt="image" src="https://github.com/user-attachments/assets/8a24f439-064a-48aa-85f3-654d0dc41a57" />


  --  Home Page

  <img width="1364" height="730" alt="image" src="https://github.com/user-attachments/assets/8f46f469-28c8-4811-9018-a93341417b74" />


  --  Contact List

  <img width="339" height="641" alt="image" src="https://github.com/user-attachments/assets/4c847e17-88ab-4c31-a6fe-6c95b1ae2a48" />


  --  Chat Window

<img width="1030" height="640" alt="image" src="https://github.com/user-attachments/assets/3603a94a-592d-49e2-8a69-9498153b4958" />


  --  Admin Panel

  <img width="1356" height="726" alt="image" src="https://github.com/user-attachments/assets/8482ecb2-af00-4a4a-929b-4a402254f476" />


8. Admin Panel


   Access Admin Panel:

        http://127.0.0.1:8000/admin


   Login using superuser credentials.


    Functions:

       * Manage Users
   
       * Manage Contacts
   
       * Manage Messages


10. Testing

  -  Registration Testing
 
  -  Create account

  -  Verify database entry

  -  Login Testing

  -  Valid Credentials

  -  Invalid Credentials

  -  Messaging Testing

  -  Send Message

  -  Receive Message

  -  Verify Message Storage


12. Future Enhancements

  -  Group Chat

  -  Voice Calling

  -  Video Calling

  -  File Sharing

  -  Emoji Support

  -  Message Notifications

  -  Online Status Indicator


13. Conclusion

The HG Chat Application provides a secure and user-friendly communication platform using Django. It demonstrates user authentication, contact management, and real-time messaging concepts while maintaining scalability for future enhancements.
