from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        help_texts = {
            'username': "(Required. 150 characters or fewer. Letters, digits, and @/./+/-/_ only.)",
            'password2': "(Enter the same password as before, for verification.)",
        }

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=150)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class ChatbotForm(forms.Form):
    question = forms.CharField(
        label="Ask your health question",
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g., What should I do for a headache?'
        })
    )

class PredictionForm(forms.Form):
    symptoms = forms.CharField(
        label="Enter your symptoms",
        widget=forms.Textarea(attrs={
            'placeholder': 'E.g., fever, cough, headache'
        })
    )

