from django.urls import path
from .views import profile_view

urlpatterns = [
    path('me', profile_view, name='me'),
]
