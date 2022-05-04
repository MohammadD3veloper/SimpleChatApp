from django import forms
from .models import Chat


class ChatForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


    class Meta:
        model = Chat
        fields = [
            'title',
            'description',
            'private',
        ]
    