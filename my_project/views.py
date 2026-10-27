from django.http import HttpResponse



def home(request):
    return HttpResponse("<h1>Welcome to home page</h1>")

def homeWithName(request, nom):
    return HttpResponse(f"<h1>Welcome to home page {nom}</h1>")