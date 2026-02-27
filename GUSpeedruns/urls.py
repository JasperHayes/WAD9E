from django.urls import path
from GUSpeedruns import views

app_name = 'GUSpeedruns'

url_patterns = [
    path('', views.homepage, name = "homepage"),
]