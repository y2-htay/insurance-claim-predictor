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

class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    permission_level = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=3,
        widget=forms.NumberInput(attrs={'min': 0, 'max': 3})
        )

