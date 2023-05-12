from django import forms

from accounts.models import *

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "strand",
        )
