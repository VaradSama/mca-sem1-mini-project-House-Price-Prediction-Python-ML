from django.contrib import admin
from django.urls import path, include
from homes.views import home_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('admin_panel/', include('admin_panel.urls')),
    path('homes/', include('homes.urls')),
    path('', home_view, name="home"),
]
