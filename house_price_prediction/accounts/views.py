from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ProfileForm
from django.core.paginator import Paginator
from homes.models import Prediction

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']
        if password != confirm:
            messages.error(request, "Passwords do not match!")
            return redirect("register")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("register")
        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")
    return render(request, "accounts/register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Role-based redirect
            if user.is_superuser:
                return redirect('admin_dashboard')  # superuser dashboard
            else:
                return redirect('predict')   # normal user dashboard (predict page)
        
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")


@login_required(login_url='/accounts/login/')
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = ProfileForm(instance=user)
    return render(request, 'accounts/profile.html', {'form': form})



@login_required(login_url='/accounts/login/')
def user_predictions(request):
    # Filter predictions for the logged-in user
    predictions_list = Prediction.objects.filter(user=request.user).order_by('-created_at')

    # Pagination: 5 predictions per page
    paginator = Paginator(predictions_list, 5)
    page_number = request.GET.get('page')
    predictions = paginator.get_page(page_number)

    return render(request, "accounts/user_predictions.html", {"predictions": predictions})


@login_required(login_url='/accounts/login/')
def prediction_detail(request, pk):
    # Get the prediction; make sure it's owned by the logged-in user
    pred = get_object_or_404(Prediction, pk=pk, user=request.user)
    
    return render(request, "accounts/prediction_detail.html", {"pred": pred})