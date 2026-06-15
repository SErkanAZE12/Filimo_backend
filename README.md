# Filimoo Backend

Backend API for the Filimoo movie and series platform.

## Tech Stack

- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Django Filter
- Pillow

## Features

### Implemented

- Movie API
- Movie Detail API
- Search
- Filtering
- Ordering
- Pagination
- JWT Authentication
- User Registration
- User Login
- User Profile Endpoint

### In Progress

- Series API
- Favorites
- Ratings
- Comments
- API Documentation
- Automated Tests

## Project Structure

```text
accounts/
catalog/
common/
interactions/
reviews/
config/
```

## Installation

Clone repository:

```bash
git clone https://github.com/YOUR_USERNAME/filimoo-backend.git
cd filimoo-backend
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create environment file:

```env
DEBUG=True

SECRET_KEY=your-secret-key

DB_NAME=movie_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

Apply migrations:

```bash
python manage.py migrate
```

Create superuser:

```bash
python manage.py createsuperuser
```

Run server:

```bash
python manage.py runserver
```

## API Base URL

```text
http://127.0.0.1:8000/api/v1/
```

## Available Endpoints

### Movies

```http
GET /api/v1/movies/
GET /api/v1/movies/{slug}/
```

### Authentication

```http
POST /api/v1/auth/register/
POST /api/v1/auth/login/
POST /api/v1/auth/refresh/
GET /api/v1/auth/me/
```

## Development Roadmap

- [x] Django Project Setup
- [x] PostgreSQL Configuration
- [ ] DRF Configuration
- [ ] Movie APIs
- [ ] Search & Filtering
- [ ] JWT Authentication
- [ ] Series APIs
- [ ] Favorites
- [ ] Ratings
- [ ] Comments
- [ ] API Documentation
- [ ] Automated Tests
- [ ] Production Deployment

## Frontend Repository

Frontend project:

https://github.com/SaraGolMohammadi/filimoo

## License

This project is developed for educational and portfolio purposes.
