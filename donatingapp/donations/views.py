from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from .models import Donation
from .forms import DonationForm
from django.db.models import Sum, Count # type: ignore
from django.db.models.functions import TruncMonth # type: ignore

@login_required
def donation_list(request):
    donations = Donation.objects.filter(donor=request.user)
    return render(request, 'donations/donation_list.html', {'donations': donations})

@login_required
def add_donation(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user
            donation.save()
            return redirect('donation_list')
    else:
        form = DonationForm()
    return render(request, 'donations/add_donation.html', {'form': form})

@login_required
def edit_donation(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id, donor=request.user)
    if request.method == 'POST':
        form = DonationForm(request.POST, instance=donation)
        if form.is_valid():
            form.save()
            return redirect('donation_list')
    else:
        form = DonationForm(instance=donation)
    return render(request, 'donations/edit_donation.html', {'form': form, 'donation': donation})

@login_required
def delete_donation(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id, donor=request.user)
    if request.method == 'POST':
        donation.delete()
        return redirect('donation_list')
    return render(request, 'donations/delete_donation.html', {'donation': donation})

def is_admin(user):
    return user.is_staff

from django.core.serializers.json import DjangoJSONEncoder
import json

@login_required
def analytics_view(request):
    total_donations = Donation.objects.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    
    donations_by_method = (
        Donation.objects.values('method')  
        .annotate(total=Sum('amount'))     
        .order_by('-total')               
    )

    donations_by_date = (
        Donation.objects.filter(date__isnull=False)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    context = {
        'total_donations': total_donations,
        'donations_by_date': json.dumps(list(donations_by_date), cls=DjangoJSONEncoder),
        'donations_by_method': json.dumps(list(donations_by_method), cls=DjangoJSONEncoder),
    }

    return render(request, 'analytics/analytics.html', context)

