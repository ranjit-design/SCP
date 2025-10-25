# PostgreSQL Setup Guide for Smart College Portal

This guide will help you connect PostgreSQL to your Django Smart College Portal project.

## Prerequisites

1. **Python 3.8+** installed
2. **PostgreSQL 12+** installed
3. **Virtual environment** activated

## Step 1: Install PostgreSQL

### Windows:
1. Download PostgreSQL from [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
2. Run the installer and follow the setup wizard
3. Remember the password you set for the `postgres` user
4. Make sure PostgreSQL service is running

### macOS:
```bash
# Using Homebrew
brew install postgresql
brew services start postgresql
```

### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

## Step 2: Create Database

1. **Open PostgreSQL command line:**
   - Windows: Open "SQL Shell (psql)" from Start Menu
   - macOS/Linux: Run `psql` in terminal

2. **Connect to PostgreSQL:**
   ```sql
   -- Connect as postgres user
   psql -U postgres
   ```

3. **Create database:**
   ```sql
   CREATE DATABASE smart_college_portal;
   CREATE USER django_user WITH PASSWORD 'your_secure_password';
   GRANT ALL PRIVILEGES ON DATABASE smart_college_portal TO django_user;
   \q
   ```

## Step 3: Configure Environment Variables

1. **Update your `.env` file** with your database credentials:
   ```env
   # Database Configuration for PostgreSQL
   DB_NAME=smart_college_portal
   DB_USER=django_user
   DB_PASSWORD=your_secure_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

## Step 4: Install Dependencies

```bash
# Activate your virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

## Step 5: Run Database Setup

### Option A: Using the setup script (Recommended)
```bash
python setup_postgres.py
```

### Option B: Manual setup
```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

## Step 6: Verify Installation

1. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

2. **Open your browser** and go to `http://127.0.0.1:8000`

3. **Test database connection** by logging in with your superuser account

## Troubleshooting

### Common Issues:

1. **"psycopg2" installation error:**
   ```bash
   # Install Microsoft Visual C++ Build Tools first, then:
   pip install psycopg2-binary
   ```

2. **Database connection refused:**
   - Check if PostgreSQL service is running
   - Verify database credentials in `.env`
   - Ensure database exists

3. **Permission denied:**
   - Check database user permissions
   - Verify password is correct

4. **Migration errors:**
   ```bash
   # Reset migrations (WARNING: This will delete all data)
   python manage.py migrate --fake-initial
   ```

### Database Connection Test:

```python
# Test in Django shell
python manage.py shell
>>> from django.db import connection
>>> with connection.cursor() as cursor:
...     cursor.execute("SELECT version();")
...     print(cursor.fetchone())
```

## Production Deployment

For production, consider:

1. **Use environment variables** for sensitive data
2. **Set up database connection pooling**
3. **Configure SSL connections**
4. **Use a managed database service** (AWS RDS, Google Cloud SQL, etc.)

## Database Backup

```bash
# Backup database
pg_dump -U django_user -h localhost smart_college_portal > backup.sql

# Restore database
psql -U django_user -h localhost smart_college_portal < backup.sql
```

## Additional Configuration

### For Heroku Deployment:
```python
# In settings.py, uncomment this section:
DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite3')
}
```

### For Docker:
```yaml
# docker-compose.yml
version: '3.8'
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: smart_college_portal
      POSTGRES_USER: django_user
      POSTGRES_PASSWORD: your_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Support

If you encounter any issues:
1. Check the Django logs
2. Verify PostgreSQL logs
3. Ensure all environment variables are set correctly
4. Test database connection manually

---

**Note:** Always backup your data before making database changes in production!

