from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login, get_user_model

from .forms import UserProfileForm, UserRegistrationForm
from .models import UserProfile
from functools import wraps
import requests
from .forms import ClaimUploadForm
from .models import ClaimUpload
import pdfkit
import io
from django.http import FileResponse
from django.http import HttpResponseForbidden


# --------- custom decorators ---------
def authenticated_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        access_token = request.session.get("access_token")
        if access_token:
            # verify token is valid
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get("http://backend:8000/api/auth/users/me", headers=headers)

            if response.status_code == 200:  # Token is valid
                return view_func(request, *args, **kwargs)
        # if missing or no token
        return redirect("login")

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


            

            # 3) Fetch the user's details from the backend
            user_data_response = requests.get(
                "http://backend:8000/api/auth/users/me",
                headers={"Authorization": f"Bearer {tokens['access']}"}
            )

            if user_data_response.status_code == 200:
                backend_user = user_data_response.json()
                User = get_user_model()
                # 4) Get or create a local Django user
                user, _ = User.objects.get_or_create(
                    username=backend_user["username"],
                    defaults={
                        # Optionally copy other fields, e.g. email:
                        "email": backend_user.get("email", "")
                    }
                )
                # 5) Mark them logged in in Django
                login(request, user)




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
                "permission_level": form.data["permission_level"]
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
                    return render(request, "register.html", {"form": form,
                                                             "error": "Registration succeeded, but login failed. Please try logging in manually."})
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
    user_response = requests.get(f"http://backend:8000/api/auth/users/me", headers=headers)

    if user_response.status_code == 200:
        user_data = user_response.json()  # user info
    else:
        user_data = {"error": "Could not retrieve user details"}

    # Get user's Claim
    claim_response = requests.get('http://backend:8000/api/user_claims/', headers=headers)
    if claim_response.status_code == 200:
        claim_data = claim_response.json()
    else:
        claim_data = {"error": "Can not retrieve claims"}

    return render(request, "profile.html", {
        "user_data": user_data,
        "claims": claim_data
    })


# -----------------User Claims---------------------
@authenticated_required
def submit_claim_view(request):
    backend_url = "http://backend:8000/api"
    headers = {
        "Authorization": f"Bearer {request.session.get('access_token')}"
    }

    # Fetch foreign key options for form
    vehicle_types = []
    weather_conditions = []
    genders = []
    injury_descriptions = []

    vt_response = requests.get(f"{backend_url}/vehicle_types/", headers=headers)
    wc_response = requests.get(f"{backend_url}/weather_conditions/", headers=headers)
    gender_response = requests.get(f"{backend_url}/gender/", headers=headers)
    injury_response = requests.get(f"{backend_url}/injury_description/", headers=headers)

    if vt_response.status_code == 200:
        vehicle_types = vt_response.json()

    if wc_response.status_code == 200:
        weather_conditions = wc_response.json()

    if gender_response.status_code == 200:
        genders = gender_response.json()

    if injury_response.status_code == 200:
        injury_descriptions = injury_response.json()

    if request.method == "POST":
        data = request.POST
        files = request.FILES

        payload = {
            # "user": request.user.id,
            "passengers_involved": data.get("passengers_involved"),
            "injury_description": data.get("injury_description"),
            "psychological_injury": data.get("psychological_injury") == "on",
            "injury_prognosis_months": data.get("injury_prognosis_months"),
            "exceptional_circumstance": data.get("exceptional_circumstance") == "on",
            "whiplash": data.get("whiplash") == "on",
            "vehicle_type": data.get("vehicle_type"),
            "weather_condition": data.get("weather_condition"),
            "driver_age": data.get("driver_age"),
            "vehicle_age": data.get("vehicle_age"),
            "police_report": data.get("police_report") == "on",
            "witness_present": data.get("witness_present") == "on",
            "gender": data.get("gender"),
        }

        files_data = {"supporting_documents": files.get("supporting_documents")} if files.get(
            "supporting_documents") else None

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
                "weather_conditions": weather_conditions,
                "injury_descriptions": injury_descriptions,
                "genders": genders
            })

    return render(request, "submit_claim.html", {
        "vehicle_types": vehicle_types,
        "weather_conditions": weather_conditions,
        "injury_descriptions": injury_descriptions,
        "genders": genders
    })


# -----------------edit/delete claim for GDPR------
@authenticated_required
def edit_or_delete_claim_view(request, claim_id):
    backend_url = "http://backend:8000/api"
    headers = {
        "Authorization": f"Bearer {request.session.get('access_token')}"
    }

    claim_response = requests.get(f"{backend_url}/user_claims/{claim_id}/", headers=headers)
    if claim_response.status_code != 200:
        return render(request, "error.html", {"message": "Could not retrieve claim data."})
    claim_data = claim_response.json()

    vehicle_types = []
    weather_conditions = []
    genders = []
    injury_descriptions = []

    vt_response = requests.get(f"{backend_url}/vehicle_types/", headers=headers)
    wc_response = requests.get(f"{backend_url}/weather_conditions/", headers=headers)
    gender_response = requests.get(f"{backend_url}/gender/", headers=headers)
    injury_response = requests.get(url=f"{backend_url}/injury_description/", headers=headers)

    if vt_response.status_code == 200:
        vehicle_types = vt_response.json()

    if wc_response.status_code == 200:
        weather_conditions = wc_response.json()

    if gender_response.status_code == 200:
        genders = gender_response.json()

    if injury_response.status_code == 200:
        injury_descriptions = injury_response.json()

    if request.method == "POST":
        if "delete" in request.POST:
            delete_response = requests.delete(f"{backend_url}/user_claims/{claim_id}/", headers=headers)
            if delete_response.status_code == 204:
                return redirect("profile")
            else:
                return render(request, "edit_claim.html", {
                    "claim": claim_data,
                    "vehicle_types": vehicle_types,
                    "weather_conditions": weather_conditions,
                    "injury_descriptions": injury_descriptions,
                    "genders": genders,
                    "error": "Failed to delete claim."
                })

        # Edit claim logic
        data = request.POST
        files = request.FILES

        payload = {
            "passengers_involved": data.get("passengers_involved"),
            "psychological_injury": data.get("psychological_injury") == "on",
            "injury_description": data.get("injury_description"),
            "injury_prognosis_months": data.get("injury_prognosis_months"),
            "exceptional_circumstance": data.get("exceptional_circumstance") == "on",
            "whiplash": data.get("whiplash") == "on",
            "vehicle_type": data.get("vehicle_type"),
            "weather_condition": data.get("weather_condition"),
            "driver_age": data.get("driver_age"),
            "vehicle_age": data.get("vehicle_age"),
            "police_report": data.get("police_report") == "on",
            "witness_present": data.get("witness_present") == "on",
            "gender": data.get("gender"),
        }

        files_data = {"supporting_documents": files.get("supporting_documents")} if files.get(
            "supporting_documents") else None

        update_response = requests.put(
            f"{backend_url}/user_claims/{claim_id}/",
            data=payload,
            files=files_data,
            headers=headers
        )

        if update_response.status_code == 200:
            return redirect("profile")
        else:
            return render(request, "edit_claim.html", {
                "claim": claim_data,
                "vehicle_types": vehicle_types,
                "weather_conditions": weather_conditions,
                "injury_descriptions": injury_descriptions,
                "genders": genders,
                "error": "Failed to update claim."
            })

    return render(request, "edit_claim.html", {
        "claim": claim_data,
        "vehicle_types": vehicle_types,
        "weather_conditions": weather_conditions,
        "injury_descriptions": injury_descriptions,
        "genders": genders,
    })


# -----------------Admin Dash---------------------

@authenticated_required
def admin_dashboard(request):
    backend_url = "http://backend:8000/api"
    headers = {
        "Authorization": f"Bearer {request.session.get('access_token')}"
    }

    # Fetch current user
    current_user_response = requests.get(f"{backend_url}/auth/users/me/", headers=headers)
    if current_user_response.status_code != 200:
        return HttpResponseForbidden("Authentication failed.")
    current_user = current_user_response.json()

    #  Enforce admin access only
    if current_user.get("permission_level") != "admin":
        return HttpResponseForbidden("You do not have admin privileges.")

    # Fetch all users and logs
    users_response = requests.get(f"{backend_url}/user_profiles/", headers=headers)
    users_data = users_response.json() if users_response.status_code == 200 else []

    user_filter = request.GET.get("user_filter", "")
    logs_url = f"{backend_url}/usage_logs/"
    if user_filter:
        logs_url += f"?user_id={user_filter}"

    logs_response = requests.get(logs_url, headers=headers)
    logs_data = logs_response.json() if logs_response.status_code == 200 else []

    # Handle user deletion
    if request.method == "POST" and "user_id" in request.POST:
        user_id = request.POST.get("user_id")

        if int(user_id) == current_user.get("id"):
            return render(request, "admin.html", {
                "error": "You cannot delete yourself.",
                "users": users_data,
                "current_user": current_user,
                "form": UserRegistrationForm(),
                "logs": logs_data,
                "user_filter": user_filter
            })

        delete_response = requests.delete(f"{backend_url}/user_profiles/{user_id}/", headers=headers)
        if delete_response.status_code == 204:
            return redirect("admin")
        else:
            return render(request, "admin.html", {
                "error": "User deletion failed. Please try again.",
                "users": users_data,
                "current_user": current_user,
                "form": UserRegistrationForm(),
                "logs": logs_data,
                "user_filter": user_filter
            })

    # Register new user (same as admin-created registration)
    if request.method == "POST" and "username" in request.POST:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            data = {
                "username": form.cleaned_data["username"],
                "password": form.cleaned_data["password"],
                "permission_level": form.cleaned_data["permission_level"]
            }

            create_response = requests.post(f"{backend_url}/auth/users/", json=data, headers=headers)
            if create_response.status_code == 201:
                return redirect("admin")
            else:
                error_message = create_response.json().get("error", "User creation failed. Please try again.")
                return render(request, "admin.html", {
                    "error": error_message,
                    "users": users_data,
                    "current_user": current_user,
                    "form": form,
                    "logs": logs_data,
                    "user_filter": user_filter
                })
    else:
        form = UserRegistrationForm()

    return render(request, "admin.html", {
        "users": users_data,
        "current_user": current_user,
        "form": form,
        "logs": logs_data,
        "user_filter": user_filter
    })


# ---------------- feedback ----------------
@authenticated_required
def feedback_view(request):
    if request.method == "POST":
        message = request.POST.get("message")
        headers = {
            "Authorization": f"Bearer {request.session.get('access_token')}",
            "Content-Type": "application/json"
        }
        payload = {"message": message}

        response = requests.post("http://backend:8000/api/user_feedback/", json=payload, headers=headers)

        if response.status_code == 201:
            return render(request, "feedback.html", {"success": "Thank you for your feedback!"})
        else:
            return render(request, "feedback.html", {"error": "Could not submit feedback. Please try again."})

    return render(request, "feedback.html")


# ------------------Finance Dashboard---------------------
@authenticated_required
def finance_dashboard(request):
    headers = {
        "Authorization": f"Bearer {request.session.get('access_token')}"
    }
    backend_url = "http://backend:8000/api"

    # get all users
    users_response = requests.get(f"{backend_url}/user_profiles/", headers=headers)
    users = users_response.json() if users_response.status_code == 200 else []

    selected_user_id = request.GET.get("user_id", None)
    claims = []
    if selected_user_id:
        claims_response = requests.get(f"{backend_url}/user_claims/?user_id={selected_user_id}",
                                       headers=headers)  # list a specific users claims
        claims = claims_response.json() if claims_response.status_code == 200 else []

    if request.method == "POST" and selected_user_id:
        total_amount = sum(claim['passengers_involved'] for claim in claims) * 5
        invoice_data = {
            "user_id": selected_user_id,
            "total_amount": total_amount
        }
        invoice_response = requests.post(f"{backend_url}/invoices/", json=invoice_data, headers=headers)

        if invoice_response.status_code == 201:
            invoice = invoice_response.json()
            pdf_content = f"Invoice ID: {invoice['id']}\nTotal Amount: ${invoice['total_amount']}\nCreated At: {invoice['created_at']}"  # make pdf content

            # reender and convert to pdf
            pdf_binary = pdfkit.from_string(pdf_content, output_path=False)
            pdf_buffer = io.BytesIO(pdf_binary)
            pdf_buffer.seek(0)

            # save the pdf
            response = FileResponse(pdf_buffer, as_attachment=True, filename=f"invoice_{invoice['id']}.pdf")
            return response
        else:
            return render(request, "finance.html", {"error": "Could not generate pdf invoice. Please try again."})

    return render(request, "finance.html", {
        "users": users,
        "claims": claims
    })


# ---------------privacy policy-----------
def privacy_policy_view(request):
    return render(request, "privacy_policy.html")


# ---------------terms--------------------

def terms_view(request):
    return render(request, "terms.html")
