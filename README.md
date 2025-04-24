# Slack Message Scheduler

A web application that allows users to schedule Slack messages to be sent after a specified delay. Built with React (frontend) and Django (backend).

## Features

- Schedule messages to be sent to Slack channels at specific times
- View, edit, and delete scheduled messages
- Send scheduled messages immediately
- Modern UI built with React and Tailwind CSS

## Project Structure

```
slack_scheduler/
├── backend/         # Django backend
│   ├── core/        # Django project settings
│   ├── scheduler/   # Django app for message scheduling
│   └── manage.py    # Django management script
└── frontend/        # React frontend
    ├── public/      # Static files
    └── src/         # React source code
```

## Setup and Installation

### Backend (Django)

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser (for admin access):
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

The backend will be available at http://localhost:8000/

### Frontend (React)

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Run the development server:
   ```
   npm start
   ```

The frontend will be available at http://localhost:3000/

## API Endpoints

- `GET /api/messages/` - List all scheduled messages
- `POST /api/messages/` - Create a new scheduled message
- `GET /api/messages/{id}/` - Retrieve a specific message
- `PUT /api/messages/{id}/` - Update a specific message
- `DELETE /api/messages/{id}/` - Delete a specific message
- `POST /api/messages/send_message/` - Send a message immediately

## Processing Scheduled Messages

To process scheduled messages that are due to be sent, run:

```
python manage.py process_messages
```

In a production environment, you would set up a cron job or a task scheduler to run this command periodically.

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Frontend**: React, TypeScript, Tailwind CSS
- **API Communication**: Axios

## Future Improvements

- Add authentication to secure the API
- Implement real Slack API integration
- Add more advanced scheduling options (recurring messages, etc.)
- Add notifications for successful/failed message deliveries
