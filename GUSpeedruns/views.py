from django.shortcuts import render
from GUSpeedruns.models import Run
from GUSpeedruns.models import Comment

def homepage(request):
    response = render(request, 'GUSpeedruns/homepage.html')
    return(response)

def about(request):
    response = render(request, 'GUSpeedruns/about.html')
    return(response)

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