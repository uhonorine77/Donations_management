from django.db import models # type: ignore
from django.conf import settings # type: ignore
from users.models import User

class Donation(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('mobile', 'Mobile Money'),
        ('bank', 'Bank Transfer'),
        ('card', 'Credit Card'),
    ]
    
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Donation by {self.donor.username} - {self.amount}"

    class Meta:
        ordering = ['-date']
