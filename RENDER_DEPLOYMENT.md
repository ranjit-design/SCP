# Render Deployment Guide for Smart College Portal

## Quick Fix for "ModuleNotFoundError: No module named 'app'"

This error occurs because Render is trying to run `gunicorn app:app` instead of using your Procfile.

### Solution 1: Update Render Dashboard Settings (Recommended)

1. Go to your Render dashboard
2. Navigate to your Web Service
3. Click on "Settings"
4. Find "Start Command" section
5. **Replace** `gunicorn app:app` with:
   ```
   gunicorn Smart_College_Portal.wsgi:application --bind 0.0.0.0:$PORT --workers 2
   ```
6. Or **leave it blank** to use the Procfile

### Solution 2: Verify Your Procfile

Your `Procfile` should contain:
```
web: gunicorn Smart_College_Portal.wsgi:application --bind 0.0.0.0:$PORT --workers 2
```

This is already correct in your project! The issue is Render is ignoring it.

## Complete Deployment Setup

### 1. Environment Variables

Add these in Render Dashboard → Environment:

#### Required Variables:
```
SECRET_KEY=your-super-secret-key-here-generate-one
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
```

#### Database Variables (if using PostgreSQL):
```
DB_NAME=smart_college_portal
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432
```

#### Email Configuration (Optional):
```
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

### 2. Build Command

In Render Dashboard → Build & Deploy:
- **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- **Start Command:** Leave blank (uses Procfile) OR use the gunicorn command above

### 3. Database Setup

After deployment, SSH into your instance and run:
```bash
python manage.py migrate
python manage.py createsuperuser
```

Or create a webhook/script to run migrations automatically.

### 4. Static Files

WhiteNoise is already configured in your `settings.py` for serving static files.

### 5. Required Files

Your project has these deployment files:
- ✅ `Procfile` - Correct gunicorn command
- ✅ `requirements.txt` - All dependencies
- ✅ `runtime.txt` - Python version specification (Python 3.13.4)
- ✅ `Smart_College_Portal/wsgi.py` - WSGI application

## Troubleshooting

### Error: "No module named 'app'"
→ Render is using wrong start command. Fix in dashboard settings.

### Error: "Database connection failed"
→ Check your PostgreSQL environment variables in Render dashboard.

### Error: "Static files not found"
→ Run `python manage.py collectstatic` in build command.

### Error: "SECRET_KEY not set"
→ Add SECRET_KEY environment variable in Render dashboard.

## Post-Deployment Checklist

- [ ] Set DEBUG=False in production
- [ ] Add proper SECRET_KEY environment variable
- [ ] Configure ALLOWED_HOSTS with your domain
- [ ] Set up PostgreSQL database
- [ ] Run database migrations
- [ ] Create superuser account
- [ ] Configure email settings (if needed)
- [ ] Test all major features
- [ ] Set up custom domain (optional)

## Important Notes

1. **Never commit secrets:** Use environment variables for all sensitive data
2. **DEBUG=False:** Always disable debug mode in production for security
3. **Database:** PostgreSQL is configured; don't use SQLite in production
4. **Static Files:** WhiteNoise is configured to serve static files
5. **Timezone:** Currently set to 'Africa/Lagos'; change if needed

## Need Help?

- Render Docs: https://render.com/docs
- Django Deployment: https://docs.djangoproject.com/en/5.1/howto/deployment/
- Your WSGI app: `Smart_College_Portal.wsgi:application`

