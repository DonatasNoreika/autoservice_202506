from .models import OrderReview
from .models import Profile, Order, OrderLine
from django import forms
from django.contrib.auth.models import User


class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = OrderReview
        fields = ['content']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['car', 'deadline']
        widgets = {'deadline': forms.DateInput(attrs={'type': 'datetime-local'})}


