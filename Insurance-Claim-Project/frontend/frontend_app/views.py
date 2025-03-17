from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm 
from .models import UserProfile
import requests
from .forms import ClaimUploadForm
from .models import ClaimUpload

def home(request):
    try:
        response = requests.get("http://backend:8000/api/")
        data = response.json()
    except Exception as e:
        data = {"error": str(e)}

    message = data.get("message", "No message available")
    return render(request, "home.html", {"message": message})


@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, "frontend_app/profile.html", {"form": form})
 
@login_required
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
    
    return render(request, "frontend_app/upload_claim.html", {"form": form})

@login_required
def claim_list(request):
    claims = ClaimUpload.objects.filter(user=request.user)  
    return render(request, "frontend_app/claim_list.html", {"claims": claims})