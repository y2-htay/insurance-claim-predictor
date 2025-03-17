from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class ClaimUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    title = models.CharField(max_length=255)  
    description = models.TextField(blank=True, null=True)  
    document = models.FileField(upload_to='claims/')  
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.title} - {self.user.username}"