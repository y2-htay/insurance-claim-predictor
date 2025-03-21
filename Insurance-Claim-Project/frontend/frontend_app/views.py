from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, UserRegistrationForm
from .models import UserProfile
from functools import wraps
import requests
from .forms import ClaimUploadForm
from .models import ClaimUpload


# --------- custom decorators ---------
def authenticated_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.session.get("access_token"):
            return view_func(request, *args, **kwargs)
        return redirect("login")  # redirect to login if not authenticated
    return wrapper
# -------------------------------------

def home(request):
    try:
        response = requests.get("http://backend:8000/api/")
        data = response.json()
    except Exception as e:
        data = {"error": str(e)}

    message = data.get("message", "Welcome to the frontend!")
    return render(request, "home.html", {"message": message})

# --------- LOGIN & LOGOUT & REGISTER -----------

def login_view(request):
    # handles user login, gets jwt token and stores it locally
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        response = requests.post(f"http://backend:8000/api/token/", json={
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            tokens = response.json()
            request.session["access_token"] = tokens["access"]  # store access token in user session
            request.session["refresh_token"] = tokens["refresh"]
            return redirect("profile")  # once user logged in, redirect then to their profile
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")

def logout_view(request):
    request.session.flush()  # clear session data
    return redirect("login")  # redirect to login page   # Can we do home page instead?

def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            data = {
                "username": form.data["username"],
                "password": form.data["password"],
                "permission_level":form.data["permission_level"]
            }

            # Register the user via the backend API
            response = requests.post("http://backend:8000/api/auth/users/", json=data)

            if response.status_code == 201:
                # Automatically log in the user after successful registration
                login_response = requests.post(f"http://backend:8000/api/token/", json={
                    "username": data["username"],
                    "password": data["password"]
                })

                if login_response.status_code == 200:
                    tokens = login_response.json()
                    request.session["access_token"] = tokens["access"]  # Store access token in user session
                    request.session["refresh_token"] = tokens["refresh"]
                    return redirect("profile")  # Redirect to profile page
                else:
                    return render(request, "register.html", {"form": form, "error": "Registration succeeded, but login failed. Please try logging in manually."})
            else:
                error_message = response.json().get("error", "Registration failed. Please try again.")
                return render(request, "register.html", {"form": form, "error": error_message})
    else:
        form = UserRegistrationForm()

    return render(request, "register.html", {"form": form})


# --------------------------------------------

@authenticated_required
def profile(request):

    headers = {"Authorization": f"Bearer {request.session.get('access_token')}"}

    # get user details from backend
    response = requests.get(f"http://backend:8000/api/auth/users/me", headers=headers)

    if response.status_code == 200:
        user_data = response.json()  # user info
    else:
        user_data = {"error": "Could not retrieve user details"}


    #Get user's Claim
    claims = ClaimUpload.objects.filter(user=request.user)

    return render(request, "profile.html", {
        "user_data": user_data,
        "claims" : claims,
    })
 

# this below will need revisiting vvvvvv


def upload_claim(request):
    if request.method == "POST":
        form = ClaimUploadForm(request.POST, request.FILES)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.user = request.user  
            claim.save()
            return redirect("claim_list")  
    else:
        form = ClaimUploadForm()
    
    return render(request, "upload_claim.html", {"form": form})

def claim_list(request):
    claims = ClaimUpload.objects.filter(user=request.user)  
    return render(request, "claim_list.html", {"claims": claims})