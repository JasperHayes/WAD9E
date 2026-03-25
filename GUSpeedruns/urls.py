from django.urls import path
from GUSpeedruns import views

app_name = 'GUSpeedruns'

urlpatterns = [
    path('', views.homepage, name = "homepage"),
    path('about/', views.about, name = "about"),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('game/upload/', views.upload_game, name='upload_game'),
    path('<slug:user_name_slug>/', views.show_user, name='show_user'),
    path('game/<slug:game_name_slug>/', views.show_game, name='show_game'),
    path('game/<slug:game_name_slug>/add-run/', views.add_run, name='add_run'),
    path('game/<slug:game_name_slug>/<slug:run_name_slug>/', views.show_run, name='show_run'),
    path('game/<slug:game_name_slug>/<slug:run_name_slug>/delete/', views.delete_run, name='delete_run'),
    path('game/<slug:game_name_slug>/<slug:run_name_slug>/<slug:slug_title>/delete/', views.delete_comment, name='delete_comment'),
    path('game/<slug:game_name_slug>/<slug:run_name_slug>/add-comment/', views.add_comment, name = "add_comment"),
    path('game/<slug:game_name_slug>/<slug:run_name_slug>/<slug:slug_title>/', views.comment_detail, name='comment_detail'),
]
