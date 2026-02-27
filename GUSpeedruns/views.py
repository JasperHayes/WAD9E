from django.shortcuts import render

def homepage(request):
    response = render(request, 'GUSPeedruns/homepage.html')
    return(response)

def about(request):
    response = render(request, 'GUSpeedruns/about.html')
    return(response)
