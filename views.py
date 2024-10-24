from datetime import timezone
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Attendance
from django.contrib.auth.models import User

def home(request):
    return render(request, 'home.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    return render(request, 'login.html')

def user_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, password=password)
        messages.success(request, "User registered successfully")
        return redirect('login')
    return render(request, 'register.html')

@login_required
def dashboard(request):
    user = request.user
    today = timezone.now().date()

    # Calculate total attendance, present days, and percentage
    total_days = Attendance.objects.filter(user=user).count()
    present_days = Attendance.objects.filter(user=user, date__lte=today).count()
    attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0

    context = {
        'attendance_percentage': round(attendance_percentage, 2),
        'attendance_count': total_days,
        'present_count': present_days,
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def submit_attendance(request):
    if request.method == 'POST':
        today = timezone.now().date()

        # Get or create the attendance record for the current user and today’s date
        attendance, created = Attendance.objects.get_or_create(
            user=request.user,
            date=today
        )

        if created:
            messages.success(request, "Attendance registered successfully.")
        else:
            messages.info(request, "Attendance for today has already been registered.")

        return redirect('dashboard')  # Redirect to the dashboard or another page

    # For GET requests, render the submit attendance template
    return render(request, 'submit_attendance.html')

def user_logout(request):
    logout(request)
    return redirect('home')

# Create your views here.
