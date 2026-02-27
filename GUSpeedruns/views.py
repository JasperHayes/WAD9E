from django.shortcuts import render

def homepage(request):
    response = render(request, 'GUSPeedruns/homepage.html')
    return (response)
