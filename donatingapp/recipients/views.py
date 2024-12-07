from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import RequestForDonation
from .forms import RequestForm, DecisionForm, RejectionReasonForm

@login_required
def add_request(request):
    if request.user.role != 'user':
        return HttpResponseForbidden("You are not authorized to make a request!")
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.recipient = request.user
            new_request.save()
            return redirect('recipient_dashboard')
    else:
        form = RequestForm()
    return render(request, 'recipients/add_recipient.html', {'form': form})

@login_required
def my_requests(request):
    requests = RequestForDonation.objects.filter(recipient=request.user)
    return render(request, 'recipients/my_requests.html', {'requests': requests})

@login_required
def reject_request(request, pk):
    donation_request = get_object_or_404(RequestForDonation, pk=pk)
    if request.method == 'POST':
        form = RejectionReasonForm(request.POST, instance=donation_request)
        if form.is_valid():
            donation_request = form.save(commit=False)
            donation_request.rejected = True
            donation_request.save()
            return redirect('recipient_list')
    else:
        form = RejectionReasonForm(instance=donation_request)
    return render(request, 'recipients/reject_request.html', {'form': form, 'donation_request': donation_request})

@login_required
def recipient_list(request):
    if request.user.role not in ['donor', 'admin']:
        return redirect('home') 
    requests = RequestForDonation.objects.filter(fulfilled=False, rejected=False)
    return render(request, 'recipients/recipient_list.html', {'requests': requests})

@login_required
def handle_decision(request, request_id):
    donation_request = get_object_or_404(RequestForDonation, id=request_id)
    if request.method == 'POST':
        form = DecisionForm(request.POST)
        if form.is_valid():
            decision = form.save(commit=False)
            decision.donor = request.user
            decision.request = donation_request
            decision.save()
            if decision.decision == 'accepted':
                donation_request.fulfilled = True
                donation_request.save()
            return redirect('recipient_list')
    else:
        form = DecisionForm()
    return render(request, 'recipients/handle_decision.html', {'form': form, 'request': donation_request})

@login_required
def recipient_dashboard(request):
    requests = RequestForDonation.objects.filter(recipient=request.user)
    return render(request, 'recipients/recipient_dashboard.html', {'requests': requests})

