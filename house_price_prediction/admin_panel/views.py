from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import datetime
from homes.models import Prediction
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password
def admin_required(user):
    return user.is_superuser  # only superusers can access

@user_passes_test(admin_required, login_url="/accounts/login/")
def index(request):
    users_count = User.objects.count()
    predictions_count = Prediction.objects.count()
    return render(request, "admin_panel/index.html", {
        "users_count": users_count,
        "predictions_count": predictions_count,
    })

@user_passes_test(admin_required, login_url="/accounts/login/")
def users_list(request):
    users_list = User.objects.all().order_by('id')
    paginator = Paginator(users_list, 10)  # 10 users per page
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    return render(request, "admin_panel/users.html", {"users": users})

@user_passes_test(admin_required, login_url="/accounts/login/")
def predictions_list(request):
    predictions_list = Prediction.objects.all().order_by('-created_at')
    paginator = Paginator(predictions_list, 10)  # 10 predictions per page
    page_number = request.GET.get('page')
    predictions = paginator.get_page(page_number)
    return render(request, "admin_panel/predictions.html", {"predictions": predictions})

@user_passes_test(admin_required, login_url="/accounts/login/")
def prediction_detail(request, pk):
    pred = get_object_or_404(Prediction, pk=pk)
    return render(request, "admin_panel/prediction_detail.html", {"pred": pred})

@user_passes_test(admin_required, login_url="/accounts/login/")
def prediction_delete(request, pk):
    pred = get_object_or_404(Prediction, pk=pk)
    pred.delete()
    messages.success(request, f"Prediction ID {pk} has been deleted successfully.")
    return redirect('admin_predictions')

@user_passes_test(admin_required, login_url="/accounts/login/")
def prediction_reports(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    predictions = Prediction.objects.select_related("user").all().order_by("-created_at")

    # 🔹 Filter by date range
    if start_date and end_date:
        predictions = predictions.filter(
            created_at__date__range=[start_date, end_date]
        )

    # Pagination
    paginator = Paginator(predictions, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "admin_panel/reports.html", {
        "page_obj": page_obj,
        "start_date": start_date,
        "end_date": end_date,
    })


@user_passes_test(admin_required, login_url="/accounts/login/")
def search_users(request):
    predictions = Prediction.objects.all().order_by("-created_at")

    # 🔍 Search filter
    search = request.GET.get("search", "")
    if search:
        predictions = predictions.filter(
            Q(user__username__icontains=search) |
            Q(input_features__location__icontains=search) |
            Q(input_features__bhk__icontains=search) |
            Q(input_features__bath__icontains=search)
        )

    # 📄 Pagination
    paginator = Paginator(predictions, 5)  # Show 5 per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "admin_panel/search.html", {
        "page_obj": page_obj,
        "search": search,
    })


def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, "admin_panel/user_detail.html", {"user": user})

# Delete User
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.success(request, f"User {user.username} deleted successfully.")
    return redirect("admin_users")

# View Predictions by User
def user_predictions(request, pk):
    user = get_object_or_404(User, pk=pk)
    predictions = Prediction.objects.filter(user=user).order_by("-created_at")
    return render(request, "admin_panel/user_predictions.html", {
        "user": user,
        "predictions": predictions,
    })

def reset_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        new_password = request.POST.get('newpassword')
        confirm_password = request.POST.get('confirmpassword')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('reset_password')

        try:
            user = User.objects.get(email=email) 
            user.password = make_password(new_password)
            user.save()
            messages.success(request, "Password changed successfully.")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "Invalid email or not an admin.")
    
    return render(request, "admin_panel/reset_password.html")