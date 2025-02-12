from django.shortcuts import render
import requests


def home(request):
    response = requests.get("http://backend:8000/api/")
    data = response.json()
    return render(request, "home.html", {"message": data["message"]})
