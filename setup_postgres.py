#!/usr/bin/env python
"""
PostgreSQL Database Setup Script for Smart College Portal
This script helps you set up PostgreSQL database for your Django project.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Smart_College_Portal.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection
from django.conf import settings

def create_database():
    """Create PostgreSQL database if it doesn't exist"""
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\nPlease make sure:")
        print("1. PostgreSQL is installed and running")
        print("2. Database credentials in .env file are correct")
        print("3. Database 'smart_college_portal' exists")
        return False

def run_migrations():
    """Run Django migrations"""
    try:
        print("\n🔄 Running migrations...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def create_superuser():
    """Create Django superuser"""
    try:
        print("\n👤 Creating superuser...")
        execute_from_command_line(['manage.py', 'createsuperuser'])
        print("✅ Superuser created successfully!")
        return True
    except Exception as e:
        print(f"❌ Superuser creation failed: {e}")
        return False

def main():
    print("🚀 Setting up PostgreSQL for Smart College Portal...")
    print("=" * 50)
    
    # Step 1: Test database connection
    if not create_database():
        return False
    
    # Step 2: Run migrations
    if not run_migrations():
        return False
    
    # Step 3: Create superuser (optional)
    create_superuser()
    
    print("\n🎉 PostgreSQL setup completed successfully!")
    print("\nNext steps:")
    print("1. Update your .env file with correct database credentials")
    print("2. Run: python manage.py runserver")
    print("3. Access your application at http://127.0.0.1:8000")

if __name__ == "__main__":
    main()

