from django import forms
from .models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    fullname = forms.CharField(max_length=255)

    def save(self, commit=True):
        user = super().save(commit)

        if user.password:
            user.set_password(user.password)
            user.save()
        return user

    class Meta:
        model = User
        fields = [
            'phone_number',
            'password',
            'fullname',
            'boss',
            'type',
            'email'
            # 'fcm_token'
        ]

