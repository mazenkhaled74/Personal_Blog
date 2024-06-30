from django.urls import path
from auth_manager.views import RegisterView,LogInView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LogInView.as_view(), name='login')
]