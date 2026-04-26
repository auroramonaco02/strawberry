# shop/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Электрондук почта'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Талааларга ыңгайлуу placeholder жана стиль кошуу
        placeholders = {
            'username': 'Колдонуучунун аты',
            'email': 'Электрондук почта',
            'password1': 'Пароль',
            'password2': 'Паролду кайталаңыз',
        }
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': placeholders.get(field_name, field.label or '')
            })
            field.help_text = None  # Керексиз жардам текстти өчүрүү