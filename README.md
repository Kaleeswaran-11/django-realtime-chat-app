# Django Real-Time Chat Application

A full-stack real-time chat application built using Django, Django Channels, and WebSockets.  
This project enables users to communicate instantly with features like live messaging, typing indicators, online status, and notifications.

---

## Features

- User Authentication (Register, Login, Logout)
- Real-Time One-to-One Messaging (WebSockets)
- Online / Offline Status
- Typing Indicator
- Notifications for new messages
- Chat History Storage
- Responsive UI using Bootstrap
- Secure Backend with Django

---

## Tech Stack

Backend:
- Python
- Django
- Django Channels
- WebSockets

Frontend:
- HTML5
- CSS3
- Bootstrap
- JavaScript

Database:
- SQLite (default) / PostgreSQL

Tools:
- Git & GitHub
- VS Code
- Postman

---

## Screenshots

### Home Page
![Home](screenshots/home_page.png)

### Register Page
![Register](screenshots/register_page.png)

### Login Page
![Login](screenshots/login_page.png)

### Chat Dashboard
![Chat](screenshots/chat_dashboard.png)

### Online Status
![Online](screenshots/online_status.png)

### Typing Indicator
![Typing](screenshots/typing_indicator.png)

### Notifications
![Notifications](screenshots/notifications.png)

### Chat History
![History](screenshots/chat_history.png)

---

## Installation and Setup

1. Clone the repository

git clone https://github.com/Kaleeswaran-11/django-realtime-chat-app.git
cd django-realtime-chat-app

2. Create virtual environment

python -m venv venv

3. Activate virtual environment

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

4. Install dependencies

pip install -r requirements.txt

5. Apply migrations

python manage.py migrate

6. Run server

python manage.py runserver

Open in browser:
http://127.0.0.1:8000/

---

## Project Structure

django-realtime-chat-app/
│
├── chat/
├── templates/
├── static/
├── screenshots/
├── manage.py
├── requirements.txt
└── README.md

---

## Security Features

- Password Hashing
- CSRF Protection
- Session Management
- Input Validation

---

## Future Enhancements

- File Sharing
- Group Chat
- Cloud Deployment
- Mobile Optimization
- Push Notifications

---

## Author

Kaleeswaran B  
GitHub: https://github.com/Kaleeswaran-11  
LinkedIn: https://linkedin.com/in/kaleeswaran-b  

---

## Support

If you find this project useful, consider starring the repository.
