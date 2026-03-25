import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone

from .EmailBackend import EmailBackend
from .models import Attendance, Session, Subject

# Create your views here.

# Temporary user creation for deployment (remove after use)
@csrf_exempt
def create_initial_users(request):
    """Create initial users - remove this after deployment"""
    from main_app.models import CustomUser
    
    users_created = []
    
    # Create Admin user
    if not CustomUser.objects.filter(email='admin@scp.com').exists():
        admin = CustomUser.objects.create_user(
            email='admin@scp.com',
            password='admin123',
            user_type='1',
            first_name='System',
            last_name='Administrator'
        )
        users_created.append("Admin: admin@scp.com / admin123")
    else:
        users_created.append("Admin: admin@scp.com / admin123 (already exists)")
    
    # Create Staff user
    if not CustomUser.objects.filter(email='staff@scp.com').exists():
        staff = CustomUser.objects.create_user(
            email='staff@scp.com',
            password='staff123',
            user_type='2',
            first_name='Staff',
            last_name='User'
        )
        users_created.append("Staff: staff@scp.com / staff123")
    else:
        users_created.append("Staff: staff@scp.com / staff123 (already exists)")
    
    # Create Student user
    if not CustomUser.objects.filter(email='student@scp.com').exists():
        student = CustomUser.objects.create_user(
            email='student@scp.com',
            password='student123',
            user_type='3',
            first_name='Student',
            last_name='User'
        )
        users_created.append("Student: student@scp.com / student123")
    else:
        users_created.append("Student: student@scp.com / student123 (already exists)")
    
    return HttpResponse(f"""
    <h2>✅ Users Created Successfully!</h2>
    <p>Use these credentials to login:</p>
    <ul>
        {"".join([f"<li>{user}</li>" for user in users_created])}
    </ul>
    <p><strong><a href="/">Go to Login Page</a></strong></p>
    <p><strong>Important: Remove this URL after use for security!</strong></p>
    <p>Time: {timezone.now()}</p>
    """)


def login_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("admin_home"))
        elif request.user.user_type == '2':
            return redirect(reverse("staff_home"))
        else:
            return redirect(reverse("student_home"))
    return render(request, 'main_app/login.html')


def doLogin(request, **kwargs):
    if request.method != 'POST':
        return HttpResponse("<h4>Denied</h4>")
    else:
        #Authenticate
        user = EmailBackend.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            if user.user_type == '1':
                return redirect(reverse("admin_home"))
            elif user.user_type == '2':
                return redirect(reverse("staff_home"))
            else:
                return redirect(reverse("student_home"))
        else:
            messages.error(request, "Invalid details")
            return redirect("/")



def logout_user(request):
    if request.user != None:
        logout(request)
    return redirect("/")


@csrf_exempt
def get_attendance(request):
    subject_id = request.POST.get('subject')
    session_id = request.POST.get('session')
    try:
        subject = get_object_or_404(Subject, id=subject_id)
        session = get_object_or_404(Session, id=session_id)
        attendance = Attendance.objects.filter(subject=subject, session=session)
        attendance_list = []
        for attd in attendance:
            data = {
                    "id": attd.id,
                    "attendance_date": str(attd.date),
                    "session": attd.session.id
                    }
            attendance_list.append(data)
        return JsonResponse(json.dumps(attendance_list), safe=False)
    except Exception as e:
        return None


def showFirebaseJS(request):
    data = """
    // Give the service worker access to Firebase Messaging.
// Note that you can only use Firebase Messaging here, other Firebase libraries
// are not available in the service worker.
importScripts('https://www.gstatic.com/firebasejs/7.22.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/7.22.1/firebase-messaging.js');

// Initialize the Firebase app in the service worker by passing in
// your app's Firebase config object.
// https://firebase.google.com/docs/web/setup#config-object
firebase.initializeApp({
    apiKey: "AIzaSyBarDWWHTfTMSrtc5Lj3Cdw5dEvjAkFwtM",
    authDomain: "sms-with-django.firebaseapp.com",
    databaseURL: "https://sms-with-django.firebaseio.com",
    projectId: "sms-with-django",
    storageBucket: "sms-with-django.appspot.com",
    messagingSenderId: "945324593139",
    appId: "1:945324593139:web:03fa99a8854bbd38420c86",
    measurementId: "G-2F2RXTL9GT"
});

// Retrieve an instance of Firebase Messaging so that it can handle background
// messages.
const messaging = firebase.messaging();
messaging.setBackgroundMessageHandler(function (payload) {
    const notification = JSON.parse(payload);
    const notificationOption = {
        body: notification.body,
        icon: notification.icon
    }
    return self.registration.showNotification(payload.notification.title, notificationOption);
});
    """
    return HttpResponse(data, content_type='application/javascript')
