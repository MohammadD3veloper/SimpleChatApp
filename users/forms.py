from django.core.cache import cache
from .models import Users
from django import forms
# from .models import User


class UserForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(required=True)
    code = forms.CharField(required=False, min_length=5)
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        code = cleaned_data.get('code')
        if cache.get(email):
            if int(cache.get(email)) == int(code):
                return cleaned_data
            else:
                self.add_error("code", "Code is invalid.")
        else:
            self.add_error("code", "Code has been expired.")

        return cleaned_data


class MainUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['email'].disabled = True

    class Meta:
        model = Users
        fields = [
            'profile_photo',
            'first_name',
            'last_name',
            'about',
            'username',
            'email',
        ]