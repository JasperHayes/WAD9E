from django.shortcuts import render, redirect
from GUSpeedruns.forms import UploadGameForm
from GUSpeedruns.models import Game
from django.contrib.auth.decorators import login_required

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
