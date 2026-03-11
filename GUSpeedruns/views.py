from django.shortcuts import render, redirect
from GUSpeedruns.forms import UploadGameForm
from GUSpeedruns.forms import CommentForm
from GUSpeedruns.models import Game
from django.contrib.auth.decorators import login_required
from GUSpeedruns.models import Run
from GUSpeedruns.models import Comment
from django.urls import reverse

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
                    
                return redirect(reverse('GUSpeedruns:show_comments',
                        kwargs={'game_name_slug': game_name_slug,
                                'run_id': run_id}))
        
        else:
            print(form.errors)
    
    context_dict = {'form': form, 'run': run}
    return render(request, 'GUSpeedruns/add_comment.html', context=context_dict)