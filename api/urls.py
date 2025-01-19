# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
path('fetch_data/', views.fetch_data, name='fetch_data'),
]