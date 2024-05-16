from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ImageGenerationForm(forms.Form):
    prompt = forms.CharField(label='Prompt', max_length=512, required=False)
    negative_prompt = forms.CharField(label='Negative prompt', max_length=512, required=False)
    width = forms.IntegerField(label='Width', min_value=64, max_value=2048, required=True, initial=512)
    height = forms.IntegerField(label='Height', min_value=64, max_value=2048, required=True, initial=768)
    seed = forms.IntegerField(label='Seed', min_value=-1, initial=-1, required=True)