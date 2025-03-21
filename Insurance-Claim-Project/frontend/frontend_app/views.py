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
    #claims = ClaimUpload.objects.filter(user=request.user)

    return render(request, "profile.html", {
        "user_data": user_data,
        #"claims" : claims,             # need fixing to new claims
    })
 


#-----------------User Claims---------------------
@authenticated_required
def submit_claim_view(request):
    backend_url = "http://backend:8000/api"
    headers = {
        "Authorization": f"Bearer {request.session.get('access_token')}"
    }

    # Fetch foreign key options for form
    vehicle_types = []
    weather_conditions = []

    vt_response = requests.get(f"{backend_url}/vehicle_types/", headers=headers)
    wc_response = requests.get(f"{backend_url}/weather_conditions/", headers=headers)

    if vt_response.status_code == 200:
        vehicle_types = vt_response.json()

    if wc_response.status_code == 200:
        weather_conditions = wc_response.json()

    if request.method == "POST":
        data = request.POST
        files = request.FILES

        payload = {
            #"user": request.user.id,
            "passengers_involved": data.get("passengers_involved"),
            "psychological_injury": data.get("psychological_injury") == "on",
            "injury_prognosis_months": data.get("injury_prognosis_months"),
            "exceptional_circumstance": data.get("exceptional_circumstance") == "on",
            "dominant_injury": data.get("dominant_injury"),
            "whiplash": data.get("whiplash") == "on",
            "vehicle_type": data.get("vehicle_type"),
            "weather_condition": data.get("weather_condition"),
            "driver_age": data.get("driver_age"),
            "vehicle_age": data.get("vehicle_age"),
            "police_report": data.get("police_report") == "on",
            "witness_present": data.get("witness_present") == "on",
            "gender": data.get("gender"),
        }

        files_data = {"supporting_documents": files.get("supporting_documents")} if files.get("supporting_documents") else None

        response = requests.post(
            f"{backend_url}/user_claims/",
            data=payload,
            files=files_data,
            headers=headers
        )

        if response.status_code == 201:
            return redirect("profile")
        else:
            return render(request, "submit_claim.html", {
                "error": "Failed to submit claim.",
                "vehicle_types": vehicle_types,
                "weather_conditions": weather_conditions
            })

    return render(request, "submit_claim.html", {
        "vehicle_types": vehicle_types,
        "weather_conditions": weather_conditions
    })
