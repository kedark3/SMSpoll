# Create your views here.
from django.http import HttpResponse
from django.template import Template, Context
from file_read import read

def home(request):
    return HttpResponse("Welcome to Home for SMS based polling system!!")

def login(request):
    code = read('/home/ssdiprojectfall2015/SMSpoll/templates/login.html')
    t= Template(code)
    c = Context()
    return HttpResponse(t.render(c))