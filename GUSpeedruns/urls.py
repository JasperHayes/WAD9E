from django.urls import path
from GUSpeedruns import views

app_name = 'GUSpeedruns'

urlpatterns = [
    path('', views.homepage, name = "homepage"),
    path('about/', views.about, name = "about"),
    path('game/upload/', views.upload_game, name='upload_game'),
    path('game/<slug:game_name_slug>/<slug:run_name_slug>/', views.show_run, name='show_run'),
    path('<slug:game_name_slug>/<int:run_id>/comments/', views.comments, name = "comments"),
    path('<slug:game_name_slug>/<int:run_id>/comments/add_comment', views.add_comment, name = "add_comment"),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
]
