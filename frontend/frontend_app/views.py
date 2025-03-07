from django.shortcuts import render
import requests


def home(request):
    try:
        response = requests.get("http://backend:8000/api/")
        data = response.json()
    except Exception as e:
        data = {"error": str(e)}

    message = data.get("message", "No message available")
    return render(request, "home.html", {"message": message})
