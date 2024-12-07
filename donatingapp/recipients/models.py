from django.db import models
from donations.models import Donation
from users.models import User

class RequestForDonation(models.Model):
    USER_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('organization', 'Organization'),
        ('company', 'Company'),
    ]
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests', limit_choices_to={'role': 'user'})
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='individual')
    title = models.CharField(max_length=255)
    description = models.TextField()
    amount_needed = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    fulfilled = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    rejection_reason = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=[
            ('Not Necessary', 'Not Necessary'),
            ('Not Feasible', 'Not Feasible'),
            ('High Amount', 'High Amount')
        ]
    )

    def total_donated(self):
        return sum(donation.amount for donation in self.donations.all())

    def is_fulfilled(self):
        return self.total_donated() >= self.amount_needed

    def __str__(self):
        return f"{self.title} - {self.recipient.username} ({self.user_type})"

class DonationDecision(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decisions', limit_choices_to={'role': 'donor'})
    request = models.ForeignKey(RequestForDonation, on_delete=models.CASCADE, related_name='decisions')
    decision = models.CharField(max_length=10, choices=[('accepted', 'Accepted'), ('declined', 'Declined')])
    date = models.DateTimeField(auto_now_add=True)
    donation = models.OneToOneField(Donation, on_delete=models.SET_NULL, null=True, blank=True, related_name='decision')

    def __str__(self):
        return f"{self.donor.username} - {self.decision} for {self.request.title}"
