from django import forms
from .models import UserProfile
from .models import ClaimUpload
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'birth_date']

class ClaimUploadForm(forms.ModelForm):
    class Meta:
        model = ClaimUpload
        fields = ['title', 'description', 'document']