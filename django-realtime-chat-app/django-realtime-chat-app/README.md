# Django Real-Time Chat App

A complete advanced full-stack real-time chat application built with **Python, Django, Django Channels, WebSockets, HTML, CSS, Bootstrap, and JavaScript**. This project supports instant one-to-one messaging, user authentication, online/offline presence, typing indicators, notifications, and unread message tracking.

---

## Project Description

This project demonstrates how to build a modern real-time communication system using Django and WebSockets. It is structured in a beginner-friendly but production-style manner so it can be used for learning, portfolio building, GitHub showcase, and resume projects.

---

## Features

- User registration, login, and logout
- Protected chat dashboard for authenticated users only
- Real-time one-to-one messaging using WebSockets
- Online/offline status indicator
- Typing indicator in live chat rooms
- Real-time notifications for new messages
- Unread message count on conversation list
- Message history stored in the database
- Message timestamps
- Responsive UI using Bootstrap
- Admin access for inspecting messages, notifications, and presence records

---

## Tech Stack

- **Backend:** Python, Django, Django Channels, WebSockets
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Database:** SQLite (default)
- **ASGI Server:** Daphne

---

## Folder Structure

```text
django-realtime-chat-app/
│── chat_project/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│── users/
│   ├── forms.py
│   ├── urls.py
│   └── views.py
│── chat/
│   ├── admin.py
│   ├── consumers.py
│   ├── models.py
│   ├── routing.py
│   ├── urls.py
│   ├── views.py
│   ├── signals.py
│   └── management/commands/seed_chat_data.py
│── templates/
│   ├── base/base.html
│   ├── users/login.html
│   ├── users/register.html
│   ├── chat/dashboard.html
│   └── chat/room.html
│── static/
│   ├── css/styles.css
│   └── js/
│       ├── main.js
│       ├── dashboard.js
│       └── chat.js
│── screenshots/
│── requirements.txt
│── manage.py
│── README.md
```

---

## Installation Steps

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd django-realtime-chat-app
```

### 2. Create and activate a virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scriptsctivate
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 6. Seed sample users and demo messages (optional)

```bash
python manage.py seed_chat_data
```

Sample demo credentials created by the seed command:
- alice / alice12345
- bob / bob12345
- charlie / charlie12345

### 7. Start the development server

```bash
python manage.py runserver
```

Open in browser:

```text
http://127.0.0.1:8000/
```

---

## WebSocket Usage Note

This project uses **Django Channels** and **ASGI** instead of the traditional WSGI-only request/response flow. Real-time chat, notifications, and presence updates run over WebSocket connections:

- `/ws/chat/<room_name>/` → real-time messages and typing events
- `/ws/presence/` → online/offline user updates
- `/ws/notifications/` → unread notification alerts

The default configuration uses an in-memory channel layer, which is ideal for local development and demo use. For production, switch to Redis as the channel layer backend.

---

## Run Commands Summary

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed_chat_data
python manage.py runserver
```

---

## Notes for Production Improvement

- Replace the hardcoded secret key with environment variables
- Use PostgreSQL for production
- Use Redis for Channels layer
- Add file/image sharing and message delivery receipts
- Add user profile pictures and search
- Deploy with Daphne/Uvicorn + Nginx

---

## Resume-Ready Project Description

- Developed a real-time chat application using Django, Django Channels, and WebSockets to enable instant one-to-one messaging.
- Implemented secure user authentication, online/offline presence tracking, typing indicators, notifications, and unread message counters.
- Built a responsive user interface with HTML, CSS, Bootstrap, and JavaScript while storing chat history and timestamps in SQLite.
- Structured the application with modular Django apps and ASGI-based real-time architecture for scalable communication workflows.

---

## Screenshots

Add screenshots in the `screenshots/` folder, for example:
- `dashboard.png`
- `chat-room.png`
- `login.png`
- `register.png`

---

## License

This project is free to use for learning and portfolio purposes.
