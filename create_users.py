"""
Create initial users for the Smart College Portal
Run this after deployment: python manage.py shell < create_users.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Smart_College_Portal.settings')
django.setup()

from main_app.models import CustomUser

def create_initial_users():
    # Create Admin user
    if not CustomUser.objects.filter(email='admin@scp.com').exists():
        admin = CustomUser.objects.create_user(
            email='admin@scp.com',
            password='admin123',
            user_type='1',
            first_name='System',
            last_name='Administrator'
        )
        print("✅ Admin user created: admin@scp.com / admin123")
    else:
        print("ℹ️ Admin user already exists")

    # Create Staff user
    if not CustomUser.objects.filter(email='staff@scp.com').exists():
        staff = CustomUser.objects.create_user(
            email='staff@scp.com',
            password='staff123',
            user_type='2',
            first_name='Staff',
            last_name='User'
        )
        print("✅ Staff user created: staff@scp.com / staff123")
    else:
        print("ℹ️ Staff user already exists")

    # Create Student user
    if not CustomUser.objects.filter(email='student@scp.com').exists():
        student = CustomUser.objects.create_user(
            email='student@scp.com',
            password='student123',
            user_type='3',
            first_name='Student',
            last_name='User'
        )
        print("✅ Student user created: student@scp.com / student123")
    else:
        print("ℹ️ Student user already exists")

if __name__ == '__main__':
    create_initial_users()
    print("\n🎉 Initial users created successfully!")
    print("\nLogin Credentials:")
    print("Admin: admin@scp.com / admin123")
    print("Staff: staff@scp.com / staff123")
    print("Student: student@scp.com / student123")
