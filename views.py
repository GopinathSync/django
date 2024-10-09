from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
# View for the Sign In page using username and password
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate the user with username and password
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)  # Log in the user
                messages.success(request, 'You are now logged in.')
                return redirect('index')  # Redirect to index page
            else:
                messages.error(request, 'Your account is disabled. Please contact support.')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'signin.html')

# View for the Sign Up page
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Check for empty fields
        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return redirect('signup')
        # Check if username or email is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('signup')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('signup')
        try:
            # Create and save the new user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('signin')
        except Exception as e:
            messages.error(request, f'Error during registration: {str(e)}')
    return render(request, 'signup.html')

# Index view
def index(request):
    return render(request, 'index.html')
