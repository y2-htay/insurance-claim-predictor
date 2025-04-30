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
    PERMISSION_LEVEL_CHOICES = [('3', 'End User'),
                                ('2', 'AI Engineer'),
                                ('1', 'Finance'),
                                ('0', 'Administrator')]
    permission_level = forms.ChoiceField(choices=PERMISSION_LEVEL_CHOICES)
