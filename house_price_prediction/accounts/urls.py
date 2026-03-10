from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('profile/', views.profile_view, name='profile'),
     path('password-change/', 
         auth_views.PasswordChangeView.as_view(template_name='accounts/change_password.html', 
                                               success_url='/accounts/password-change-done/'), 
         name='password_change'),

    path('password-change-done/', 
         auth_views.PasswordChangeDoneView.as_view(template_name='accounts/change_password_done.html'), 
         name='password_change_done'),
    path('my-predictions/', views.user_predictions, name='user_predictions'),
    path('prediction/<int:pk>/', views.prediction_detail, name='prediction_detail'),
]
