from django.urls import path
from GUSpeedruns import views

app_name = 'GUSpeedruns'

urlpatterns = [
    path('', views.homepage, name = "homepage"),
    path('about/', views.about, name = "about"),
]