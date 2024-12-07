from django import forms
from .models import RequestForDonation, DonationDecision

class RequestForm(forms.ModelForm):
    """Form for creating a new donation request."""
    class Meta:
        model = RequestForDonation
        fields = ['title', 'description', 'amount_needed', 'user_type'] 
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter request title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your need'}),
            'amount_needed': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount needed'}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Request Title',
            'description': 'Description',
            'amount_needed': 'Amount Needed',
            'user_type': 'Type of User',
        }

class DecisionForm(forms.ModelForm):
    """Form for donors to accept or decline a donation request."""
    class Meta:
        model = DonationDecision
        fields = ['decision']
        widgets = {
            'decision': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'decision': 'Your Decision',
        }

class RejectionReasonForm(forms.ModelForm):
    class Meta:
        model = RequestForDonation
        fields = ['rejection_reason']
        widgets = {
            'rejection_reason': forms.Select(
                attrs={'class': 'form-control'},
                choices=[
                    ('Not Necessary', 'Not Necessary'),
                    ('Not Feasible', 'Not Feasible'),
                    ('High Amount', 'High Amount'),
                ],
            )
        }
