from django.shortcuts import render, redirect
from GUSpeedruns.forms import UploadGameForm
from GUSpeedruns.models import Game
from django.contrib.auth.decorators import login_required
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
        form = UploadGameForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('')
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
    
    except Run.DoesNotExist:
        context_dict['run'] = None
        context_dict['comments'] = None
        
    response = render(request, 'GUSpeedruns/comments.html')