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

# Project Structure

 ```
 ad-platform/
  apps/ # Django applications
   channels/ # Ad channels management
   clients/ # Client management
   core/ # Core functionality
   events/ # Calendar events
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