# Smart Campus Helpdesk API

A backend REST API for a Smart Campus Helpdesk system built with Django and Django REST Framework. Students can raise tickets (issues) and administrators can manage them.

## Features

- **Ticket Management**: Full CRUD operations for campus issues.
- **Authentication**: JWT-based secure login and session authentication for admins.
- **Pagination**: Efficient handling of ticket lists.
- **Filtering**: Filter tickets by category and status.
- **Ordering**: Sort by priority and creation date.
- **Search**: Search tickets by title or description.
- **Redis Caching**: Optimized list API performance with Redis.
- **Database**: PostgreSQL integration for reliable data storage.

## Data Model (Ticket)

- `id`: Unique identifier (Auto Field).
- `title`: Title of the issue.
- `description`: Detailed description.
- `category`: `classroom`, `hostel`, or `network`.
- `priority`: `low`, `medium`, or `high`.
- `status`: `open`, `in-progress`, or `closed`.
- `created_at`: Timestamp of creation.
- `updated_at`: Timestamp of last update.

## Tech Stack

- **Framework**: Django, Django REST Framework
- **Auth**: SimpleJWT
- **Database**: PostgreSQL
- **Cache**: Redis (django-redis)

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Omkarbonda/Smart-Campus-Helpdesk-API.git
   cd Smart-Campus-Helpdesk-API
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Database**:
   Update `smart_campus/settings.py` with your PostgreSQL credentials.

4. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Start Redis Server**:
   Ensure Redis is running on your machine.

6. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

- `POST /api/token/`: Get JWT access and refresh tokens.
- `POST /api/token/refresh/`: Refresh the access token.
- `POST /tickets/`: Create a new ticket (Authenticated).
- `GET /tickets/`: List all tickets with pagination/filtering (Authenticated).
- `GET /tickets/<id>/`: Get ticket details (Authenticated).
- `PATCH /tickets/<id>/`: Update ticket status or details (Authenticated).
- `DELETE /tickets/<id>/`: Delete a ticket (Authenticated).

## Project Structure

- `smart_campus/`: Project configuration.
- `tickets/`: Main app logic (models, views, serializers).
- `requirements.txt`: Project dependencies.
- `.gitignore`: Files to exclude from Git.
- `README.md`: This file.
