from django import forms # type: ignore
from .models import Donation

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount', 'method', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
