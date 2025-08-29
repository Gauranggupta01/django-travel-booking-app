# travel/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking

# --- Create a new custom registration form ---
class CustomUserCreationForm(UserCreationForm):
    # Make the email field required
    email = forms.EmailField(required=True, help_text='Required. Please use a valid Gmail address.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_email(self):
        """
        Validate that the email address is a Gmail account.
        """
        email = self.cleaned_data.get('email')
        if not email.lower().endswith('@gmail.com'):
            raise forms.ValidationError("Only Gmail accounts are allowed for registration.")
        return email

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_email(self):
        """
        Validate that the email address is a Gmail account during profile updates.
        """
        email = self.cleaned_data.get('email')
        if not email.lower().endswith('@gmail.com'):
            raise forms.ValidationError("Only Gmail accounts are allowed.")
        return email

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('number_of_seats',)
