from django.shortcuts import render, redirect
from GUSpeedruns.forms import UserForm, UserProfileForm
from GUSpeedruns.forms import UploadGameForm
from GUSpeedruns.forms import CommentForm
from GUSpeedruns.models import Game
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from GUSpeedruns.models import Run
from GUSpeedruns.models import Comment

def homepage(request):
    response = render(request, 'GUSpeedruns/homepage.html')
    return(response)

def about(request):
    response = render(request, 'GUSpeedruns/about.html')
    return(response)

@login_required
def upload_game(request):
    form = UploadGameForm()

    if request.method == 'POST':
        form = UploadGameForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(commit=True)
            return redirect('GUSpeedruns:homepage')
        else:
            print(form.errors)

    return render(request, 'GUSpeedruns/upload_game.html', {'form': form})

def comments(request, game_name_slug, run_id):
    context_dict = {}
    try:
        run = Run.objects.get(id = run_id)
        comments = Comment.objects.filter(run=run)
        
        context_dict['run'] = run
        context_dict['comments'] = comments
        context_dict['game_name_slug'] = game_name_slug # needed for the URL tag for add comment
    
    except Run.DoesNotExist:
        context_dict['run'] = None
        context_dict['comments'] = None
        
    return render(request, 'GUSpeedruns/comments.html', context=context_dict)

@login_required
def add_comment(request, game_name_slug, run_id):
    try:
        run = Run.objects.get(id=run_id)
    except Run.DoesNotExist:
        return redirect('/')
    
    form = CommentForm()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        
        if form.is_valid():
            if run:
                comment = form.save(commit=False)
                comment.run = run
                comment.user = request.user
                comment.save()
                    
                return redirect(reverse('GUSpeedruns:comments',
                        kwargs={'game_name_slug': game_name_slug,
                                'run_id': run_id}))
        
        else:
            print(form.errors)
    
    context_dict = {'form': form, 'run': run}
    return render(request, 'GUSpeedruns/add_comment.html', context=context_dict)

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
                return redirect(reverse('GUSpeedruns:index'))
            else:
                return HttpResponse("Your GUSpeedrun account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'GUSpeedruns/login.html')



def show_run(request, game_name_slug, run_name_slug):
    context_dict = {}

    try:
        run = Run.objects.get(slug_title = run_name_slug)
        context_dict['run'] = run
        assert run.game.slug_name == game_name_slug
        comments = Comment.objects.filter(run = run)
        context_dict['comments'] = comments
    
    except:
        context_dict['run'] = None
        context_dict['comments'] = None

    return render(request, 'GUSpeedruns/run.html', context=context_dict)
            