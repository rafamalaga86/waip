from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        label=_('Email'),
        widget=forms.TextInput(attrs={'placeholder': _('johndoe@mymail.com')}),
        help_text=_('Required. Your email address email address.')
    )
    first_name = forms.CharField(
        max_length=63,
        label=_('First Name'),
        widget=forms.TextInput(attrs={'placeholder': _('John')}),
        help_text=_('Required. Your First Name.')
    )
    last_name = forms.CharField(
        max_length=63,
        label=_('Last Name'),
        widget=forms.TextInput(attrs={'placeholder': _('Doe')}),
        help_text=_('Required. Your Last Name.')
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': _('sephirot543')}),
        }

    # Set the class "form-control" to every input in the form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
