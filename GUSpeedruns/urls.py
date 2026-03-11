from django.urls import path
from GUSpeedruns import views

app_name = 'GUSpeedruns'

urlpatterns = [
    path('', views.homepage, name = "homepage"),
    path('about/', views.about, name = "about"),
    path('/game/upload/', views.upload_game, name='upload_game'),
    path('<slug:game_name_slug>/<int:run_id>/comments/', views.comments, name = "comments")
]
