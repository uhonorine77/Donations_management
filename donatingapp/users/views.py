from django.shortcuts import render # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.shortcuts import get_object_or_404, render, redirect # type: ignore
from django.contrib.auth import login,logout # type: ignore
from users.models import User
from users.forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserUpdateForm
from django.core.paginator import Paginator # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import HttpResponseForbidden, JsonResponse # type: ignore

@login_required(login_url="/login/")
def home(request):
    return render(request, 'home.html')

@login_required(login_url="/login/")
def dashboard(request):
    return render(request, 'dashboard/auth_dashboard.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(f"User {user.username} created successfully!")
            return redirect('/login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            if user.is_staff:
                return redirect('analytics')
            else:
                return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form, 'is_update': False})

def user_logout(request):
    logout(request)
    return redirect('user_login')

# @login_required(login_url="/login/")
def user_list(request):
    users = User.objects.all()
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Commented out the HTML return and using JsonResponse
    user_list_data = [{'id': user.id, 'username': user.username, 'email': user.email, 'role': user.role} for user in page_obj]
    return JsonResponse({'users': user_list_data, 'page': page_obj.number, 'total_pages': page_obj.paginator.num_pages})

@login_required(login_url="/login/")
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('auth')
    else:
        form = CustomUserUpdateForm(instance=user)
    return render(request, 'users/register.html', {'form': form, 'is_update': True})

# @login_required(login_url="/login/")
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('auth')
    return render(request, 'users/delete_user.html', {'user': user})

