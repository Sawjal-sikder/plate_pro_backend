# Plate Pro Backend

Django REST API backend for Plate Pro application with Celery task processing and Docker support.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Method 1: Using Docker (Recommended)](#method-1-using-docker-recommended)
  - [Method 2: Local Setup](#method-2-local-setup)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [Database Management](#database-management)
- [Common Commands](#common-commands)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### For Docker Setup

- [Docker](https://www.docker.com/get-started) (version 20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0+)

### For Local Setup

- Python 3.8 or higher
- pip (Python package manager)
- Redis (for Celery task queue)
- Virtual environment (recommended)

## Installation

### Method 1: Using Docker (Recommended)

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd plate_pro_backend
   ```

2. **Create environment file**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` file with your configuration values.

3. **Build and start containers**

   ```bash
   docker compose build
   docker compose up -d
   ```

4. **Run migrations**

   ```bash
   docker compose exec web python manage.py migrate
   ```

5. **Create superuser**

   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   docker compose exec web python manage.py collectstatic --noinput
   ```

### Method 2: Local Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd plate_pro_backend
   ```

2. **Create and activate virtual environment**

   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` file with your configuration values.

5. **Run migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (if not using SQLite)
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Redis
REDIS_URL=redis://localhost:6380

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password

# Social Auth (if applicable)
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret

# Celery
CELERY_BROKER_URL=redis://localhost:6380/0
CELERY_RESULT_BACKEND=redis://localhost:6380/0
```

## Running the Project

### Using Docker

1. **Start all services**

   ```bash
   docker compose up -d
   ```

2. **View logs**

   ```bash
   docker compose logs -f
   ```

3. **Stop services**

   ```bash
   docker compose down
   ```

4. **Restart services**
   ```bash
   docker compose restart
   ```

### Local Development

1. **Start Redis server** (in a separate terminal)

   ```bash
   redis-server --port 6380
   ```

2. **Start Django development server**

   ```bash
   python manage.py runserver
   ```

   The API will be available at http://localhost:8000

3. **Start Celery worker** (in a separate terminal)

   ```bash
   celery -A project worker --loglevel=info
   ```

4. **Start Celery beat** (optional, for scheduled tasks)
   ```bash
   celery -A project beat --loglevel=info
   ```

## Database Management

### Migrations

**Create new migrations after model changes:**

```bash
# Docker
docker compose exec web python manage.py makemigrations

# Local
python manage.py makemigrations
```

**Apply migrations:**

```bash
# Docker
docker compose exec web python manage.py migrate

# Local
python manage.py migrate
```

**Show migration status:**

```bash
# Docker
docker compose exec web python manage.py showmigrations

# Local
python manage.py showmigrations
```

**Rollback migrations:**

```bash
# Docker
docker compose exec web python manage.py migrate <app_name> <migration_name>

# Local
python manage.py migrate <app_name> <migration_name>
```

### Database Shell

**Access Django shell:**

```bash
# Docker
docker compose exec web python manage.py shell

# Local
python manage.py shell
```

**Access database directly:**

```bash
# Docker
docker compose exec web python manage.py dbshell

# Local
python manage.py dbshell
```

## Common Commands

### User Management

**Create superuser:**

```bash
# Docker
docker compose exec web python manage.py createsuperuser

# Local
python manage.py createsuperuser
```

**Change user password:**

```bash
# Docker
docker compose exec web python manage.py changepassword <username>

# Local
python manage.py changepassword <username>
```

### Static Files

**Collect static files:**

```bash
# Docker
docker compose exec web python manage.py collectstatic --noinput

# Local
python manage.py collectstatic --noinput
```

**Clear static files:**

```bash
# Docker
docker compose exec web python manage.py collectstatic --clear --noinput

# Local
python manage.py collectstatic --clear --noinput
```

### Testing

**Run all tests:**

```bash
# Docker
docker compose exec web python manage.py test

# Local
python manage.py test
```

**Run specific app tests:**

```bash
# Docker
docker compose exec web python manage.py test accounts

# Local
python manage.py test accounts
```

**Run with coverage:**

```bash
# Docker
docker compose exec web coverage run --source='.' manage.py test
docker compose exec web coverage report

# Local
coverage run --source='.' manage.py test
coverage report
```

### Custom Management Commands

**Delete expired reset codes:**

```bash
# Docker
docker compose exec web python manage.py delete_expired_reset_codes

# Local
python manage.py delete_expired_reset_codes
```

### Container Management (Docker)

**View running containers:**

```bash
docker compose ps
```

**Access container shell:**

```bash
docker compose exec web bash
```

**View container logs:**

```bash
docker compose logs -f web
docker compose logs -f worker
docker compose logs -f redis
```

**Rebuild containers:**

```bash
docker compose build --no-cache
docker compose up -d
```

**Remove containers and volumes:**

```bash
docker compose down -v
```

## Project Structure

```
plate_pro_backend/
├── accounts/              # User authentication and account management
│   ├── models.py         # Custom user model
│   ├── views.py          # Authentication views
│   ├── serializers.py    # API serializers
│   ├── urls.py           # URL routing
│   └── management/       # Custom management commands
├── services/             # Core business logic services
│   ├── models.py         # Service models
│   ├── views.py          # Service views
│   └── serializers.py    # API serializers
├── project/              # Project configuration
│   ├── settings.py       # Django settings
│   ├── urls.py           # Root URL configuration
│   ├── celery.py         # Celery configuration
│   └── wsgi.py           # WSGI configuration
├── media/                # User uploaded files
│   └── dxf/              # DXF files
├── staticfiles/          # Collected static files
├── docker-compose.yml    # Docker compose configuration
├── Dockerfile            # Docker build instructions
├── requirements.txt      # Python dependencies
├── manage.py             # Django management script
└── db.sqlite3            # SQLite database (development)
```

## API Documentation

### Access API Documentation

Once the server is running, access the API documentation at:

- **Swagger UI:** http://localhost:8000/swagger/
- **ReDoc:** http://localhost:8000/redoc/
- **Django Admin:** http://localhost:8000/admin/

### Main API Endpoints

- **Authentication:**

  - `POST /api/accounts/register/` - User registration
  - `POST /api/accounts/login/` - User login
  - `POST /api/accounts/logout/` - User logout
  - `POST /api/accounts/password/reset/` - Password reset

- **Services:**
  - `GET /api/services/` - List all services
  - `POST /api/services/` - Create new service
  - `GET /api/services/{id}/` - Get service details
  - `PUT /api/services/{id}/` - Update service
  - `DELETE /api/services/{id}/` - Delete service

## Troubleshooting

### Common Issues

**Port already in use:**

```bash
# Check what's using the port
# Windows
netstat -ano | findstr :14030

# Linux/macOS
lsof -i :14030

# Change port in docker-compose.yml or stop the conflicting service
```

**Database locked error:**

```bash
# Stop all services and restart
docker compose down
docker compose up -d
```

**Permission denied errors:**

```bash
# On Linux/macOS, you may need to adjust file permissions
sudo chown -R $USER:$USER .
```

**Migrations not applying:**

```bash
# Reset migrations (WARNING: This will delete data)
docker compose exec web python manage.py migrate --fake <app_name> zero
docker compose exec web python manage.py migrate <app_name>
```

**Celery tasks not running:**

```bash
# Check Redis connection
docker compose logs redis

# Restart Celery worker
docker compose restart worker
```

**Static files not loading:**

```bash
# Recollect static files
docker compose exec web python manage.py collectstatic --clear --noinput
```

### Reset Development Environment

```bash
# Stop and remove all containers
docker compose down -v

# Remove SQLite database
rm db.sqlite3

# Rebuild and start
docker compose build --no-cache
docker compose up -d

# Run migrations and create superuser
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py collectstatic --noinput
```

## Development Workflow

1. **Create a new feature branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes and test**

   ```bash
   python manage.py test
   ```

3. **Create migrations if models changed**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin feature/your-feature-name
   ```

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in environment variables
2. Use a production-grade database (PostgreSQL recommended)
3. Configure proper `ALLOWED_HOSTS`
4. Use environment variables for all secrets
5. Set up proper logging
6. Use HTTPS/SSL certificates
7. Configure proper CORS settings
8. Set up monitoring and error tracking

## License

[Add your license information here]

## Support

For support, email [your-email] or open an issue in the repository.
