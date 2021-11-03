from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from dapp.models import Account, DataFile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
                             required=True, max_length=254, label=False)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
                                required=True, min_length=8, label=False, help_text='')
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm password"}), label=False,
        required=True, min_length=8, help_text='')

    class Meta:
        model = Account
        fields = ('email', 'password1', 'password2')

    def email_exists(email):
        if Account.objects.filter(email=email).exists():
            return True
        return False

    def save(self, commit=True):
        user = Account.objects.create_user(
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")
