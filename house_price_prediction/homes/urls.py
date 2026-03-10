from django.urls import path
from . import views
urlpatterns = [
    path('predict/', views.predict_view, name='predict'),
    path('result/<int:pk>/', views.result_view, name='result'),
]
