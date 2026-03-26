from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from GUSpeedruns.models import Game, Run, Comment, UserProfile
from GUSpeedruns.forms import UserForm, UserProfileForm, UploadGameForm, CommentForm, RunForm
from datetime import timedelta
from urllib.parse import urlparse, parse_qs
from django.core.paginator import Paginator
import re
import requests
import isodate
from django.http import JsonResponse

#for youtube API
API_KEY = "AIzaSyCOa_I-kpQZIJXISS5aQ0WrkyGPrz9tvEI"

def homepage(request):
    query = request.GET.get('q', '').strip()

    if query:
        game_list = Game.objects.filter(name__icontains=query).order_by('name')
        page_title = 'Search Results'
    else:
        game_list = Game.objects.order_by('-views', 'name')
        page_title = 'Trending Games'

    paginator = Paginator(game_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context_dict = {
        'games': page_obj.object_list,
        'page_obj': page_obj,
        'query': query,
        'page_title': page_title,
    }

    return render(request, 'GUSpeedruns/homepage.html', context=context_dict)

def about(request):
    response = render(request, 'GUSpeedruns/about.html')
    return(response)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        
    return render(request,
                  'GUSpeedruns/register.html',
                  context = {'user_form': user_form,
                             'profile_form': profile_form,
                             'registered': registered})
    
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username,password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('GUSpeedruns:homepage'))
            else:
                return HttpResponse("Your GUSpeedrun account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'GUSpeedruns/login.html')

@login_required
def user_logout(request):
    logout(request)
    return(redirect(reverse('GUSpeedruns:homepage')))

@staff_member_required
def upload_game(request):
    form = UploadGameForm()

    if request.method == 'POST':
        form = UploadGameForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/GUSpeedruns/')
        else:
            print(form.errors)

    return render(request, 'GUSpeedruns/upload_game.html', {'form': form})

def show_game(request, game_name_slug):
    context_dict = {}

    try:
        game = Game.objects.get(slug_name = game_name_slug)
        context_dict['game'] = game
        context_dict['game_name_slug'] = game_name_slug
        runs = Run.objects.filter(game = game).order_by('time')[:10]
        context_dict['runs'] = runs
    
    except:
        context_dict['game'] = None
        context_dict['runs'] = None
        
    return render(request, 'GUSpeedruns/game.html', context=context_dict)

def show_user(request, user_name_slug):
    context_dict = {}

    try:
        user = Game.objects.get(slug_name = user_name_slug)
        context_dict['user'] = user
        context_dict['user_name_slug'] = user_name_slug
    
    except:
        context_dict['user'] = None
        
    return render(request, 'GUSpeedruns/profile.html', context=context_dict)

def comment_detail(request, game_name_slug, run_name_slug, slug_title):
    context_dict = {}
    try:
        comment = Comment.objects.get(slug_title=slug_title)
        
        context_dict['comment'] = comment
        context_dict['game_name_slug'] = game_name_slug
        context_dict['run_name_slug'] = run_name_slug
    
    except Comment.DoesNotExist:
        context_dict['comment'] = None
    
    return render(request, 'GUSpeedruns/comment_detail.html', context=context_dict)

@login_required
def add_comment(request, game_name_slug, run_name_slug):
    context_dict = {}
    try:
        run = Run.objects.get(slug_title=run_name_slug)
    except Run.DoesNotExist:
        return redirect(reverse('GUSpeedruns:homepage'))
    
    form = CommentForm()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        
        if form.is_valid():
            if run:
                comment = form.save(commit=False)
                comment.run = run
                comment.user = UserProfile.objects.get(user = request.user)
                comment.save()
                context_dict['game_name_slug'] = game_name_slug
                context_dict['run_name_slug'] = run_name_slug
                    
                return redirect(reverse('GUSpeedruns:show_run', kwargs={
                    'game_name_slug': game_name_slug,
                    'run_name_slug': run_name_slug
                    }))
        
        else:
            print(form.errors)
    
    context_dict = {'form': form, 'run': run, 'game_name_slug':game_name_slug}
    return render(request, 'GUSpeedruns/add_comment.html', context=context_dict)

@staff_member_required
def delete_comment(request, game_name_slug, run_name_slug, slug_title):
    if request.method == 'POST':
        context_dict = {}
        try:
            comment = Comment.objects.get(slug_title=slug_title)
            context_dict['comment'] = comment
            context_dict['game_name_slug'] = game_name_slug
            context_dict['run_name_slug'] = run_name_slug
            comment.delete()
        
        except Comment.DoesNotExist:
            context_dict['comment'] = None
            

    return redirect(reverse('GUSpeedruns:show_run', kwargs={
        'game_name_slug': game_name_slug,
        'run_name_slug': run_name_slug
    }))


def show_run(request, game_name_slug, run_name_slug):
    context_dict = {}

    try:
        run = Run.objects.get(slug_title = run_name_slug)
        game = Game.objects.get(slug_name = game_name_slug)
        context_dict['run'] = run
        context_dict['game'] = game
        assert run.game.slug_name == game_name_slug
        comments = Comment.objects.filter(run = run)
        context_dict['comments'] = comments
        context_dict['game_name_slug'] = game_name_slug
        context_dict['run_name_slug'] = run_name_slug
        
    
    except:
        context_dict['run'] = None
        context_dict['comments'] = None

    return render(request, 'GUSpeedruns/run.html', context=context_dict)

def add_run(request, game_name_slug):
    form = RunForm()

    if request.method == 'POST':
        form = RunForm(request.POST)

        if form.is_valid():
            run = form.save(commit=False)

            hours = form.cleaned_data['hours']
            minutes = form.cleaned_data['minutes']
            seconds = form.cleaned_data['seconds']
            milliseconds = form.cleaned_data['milliseconds']

            run.user = UserProfile.objects.get(user = request.user)
            run.game = Game.objects.get(slug_name=game_name_slug)
            run.video_url_id = get_youtube_id(form.cleaned_data['video'])
            run.time = timedelta(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)

            run.save()
            return redirect(reverse('GUSpeedruns:show_game', kwargs={'game_name_slug': game_name_slug}))
        
        else:
            print(form.errors)

    return render(request, 'GUSpeedruns/add_run.html', {'form': form, 'game_name_slug': game_name_slug})

def get_youtube_id(url):
    parsed_url = urlparse(url)

    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        return parse_qs(parsed_url.query).get('v', [None])[0]

    elif parsed_url.hostname == 'youtu.be':
        return parsed_url.path.lstrip('/')

    return None
            
@staff_member_required
def delete_run(request, game_name_slug, run_name_slug):
    if request.method == 'POST':
        try:
            run = Run.objects.get(slug_title = run_name_slug)
            run.delete()
            
        except Run.DoesNotExist:
            return redirect(reverse('GUSpeedruns:homepage'))
        
    return redirect(reverse('GUSpeedruns:show_game', kwargs={'game_name_slug': game_name_slug}))



def get_video_data(video_id):
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,contentDetails",
        "id": video_id,
        "key": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    if not data["items"]:
        return None
    item = data["items"][0]
    duration = isodate.parse_duration(item["contentDetails"]["duration"])
    return {
        "description": item["snippet"]["description"],
        "duration": int(duration.total_seconds())
    }


def fetch_youtube_data(request):
    url = request.GET.get("url")
    video_id = get_youtube_id(url)
    if not video_id:
        return JsonResponse({"error": "Invalid URL"}, status=400)
    video_data = get_video_data(video_id)
    if not video_data:
        return JsonResponse({"error": "Video not found"}, status=404) 
    return JsonResponse(video_data)


