# Ad Platform

A Django-based platform for managing advertising campaigns, channels, and events.

# Prerequisites

- Python 3.10+ 
- Node.js 18+ 
- PostgreSQL 14+

# Installation

1. Clone the repository: 
```bash
git clone <repository-url> cd ad-platform
```

1. Create and activate a virtual environment: 
```bash
# On Windows 
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

1. Install Python dependencies: 
```bash
pip install -r requirements.txt
```

2. Install Node.js dependencies: 
```bash
npm install
```

3. Create a PostgreSQL database.

4. Create a .env file in the project root with the following content: 
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/database_name
```

Replace user, password, and database_name with your PostgreSQL credentials.

# Database Setup

1. Apply migrations: 
```bash
python manage.py migrate
```

2. Create a superuser: 
```bash
python manage.py createsuperuser
```

3. (Optional) Load sample data:
```bash
python manage.py populate_db
```

# Running the Development Server

1. Start the Vite development server: 
```bash
npm run dev
```

2. In a separate terminal, start the Django development server: 
```bash
python manage.py runserver
```

3. Visit http://localhost:8000 in your browser.

4. Log in with your superuser credentials.

# Notifications Setup

# Email Configuration

Add these settings to your .env file: 

```env
// Email settings (using Gmail as an example)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587 EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-specific-password'
```

For Gmail: 

1. Enable 2-Factor Authentication 
2. Generate an App Password: Google Account → Security → App Passwords 
3. Use the generated password as `EMAIL_HOST_PASSWORD`

# SMS Configuration

This project can use Twilio for SMS. Add these to your .env: 

```env
TWILIO_ACCOUNT_SID = 'your-account-sid'
TWILIO_AUTH_TOKEN = 'your-auth-token'
TWILIO_FROM_NUMBER = 'your-twilio-number'
```

To set up Twilio: 
1. Create an account at https://www.twilio.com 
2. Get your Account SID and Auth Token from the Twilio Console 
3. Purchase or use an existing Twilio phone number 

# Initial Notification Setup

Set up user preferences in Django Admin: 

- Navigate to /admin/notifications/usernotificationpreference/ 
- Create preferences for users who should receive notifications

# Background Tasks

For notification processing, add to your crontab: 

```bash 
// Process reminders every 15 minutes
*/15 * * * * /path/to/venv/bin/python /path/to/project/manage.py process_reminders
```

Or using Celery (recommended for production): 

```python
// settings.py
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
```

```bash
// Run Celery worker
celery -A config.celery worker -l info
// Run Celery beat for scheduled tasks
celery -A config.celery beat -l info
```

# Project Structure

 ```
 ad-platform/
  apps/ # Django applications
   channels/ # Ad channels management
   clients/ # Client management
   core/ # Core functionality
   events/ # Calendar events
   notifications/ # Notification management
   projects/ # Project management
   users/ # User management
  config/ # Project configuration
  static_src/ # Frontend source files
   css/ # CSS files
   js/ # JavaScript files
  templates/ # Base templates
```

# Features

- User authentication and authorization - Client management - Advertising channels management - Project tracking - Event calendar - Analytics -board

# Development

# Adding New Dependencies

- Python dependencies:
```bash
pip install package-name pip freeze > requirements.txt
```

- Node.js dependencies: 
```bash
npm install package-name
```

# Database Updates

After making model changes: 
```bash
python manage.py makemigrations python manage.py migrate
```

# Frontend Assets

- CSS and JavaScript files are processed by Vite 

The project uses: 
- TailwindCSS for styling 
- DaisyUI for UI components 
- HTMX for dynamic interactions 
- FullCalendar for the calendar view 
- Chart.js for analytics

# Deployment

1. Set DEBUG=False in your production environment 
2. Configure your production database 
3. Collect static files: 
```bash
npm run build python manage.py collectstatic
```