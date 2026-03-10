from django.urls import path
from . import views

urlpatterns = [
    path('admin_dashboard/', views.index, name="admin_dashboard"),
    path('users/', views.users_list, name="admin_users"),
    path('predictions/', views.predictions_list, name="admin_predictions"),
    path('predictions/<int:pk>/', views.prediction_detail, name='admin_prediction_detail'),
    path('predictions/delete/<int:pk>/', views.prediction_delete, name='admin_prediction_delete'),
    path("reports/", views.prediction_reports, name="admin_reports"),
    path("search_users/", views.search_users, name="search_users"),
    path("users/<int:pk>/", views.user_detail, name="user_detail"),
    path("users/<int:pk>/delete/", views.user_delete, name="user_delete"),
    path("users/<int:pk>/predictions/", views.user_predictions, name="user_predictions"),
    path("reset-password", views.reset_password, name="reset_password"),
]

