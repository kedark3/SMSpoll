# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.template import Template, Context
from file_read import read
import MySQLdb as msdb
from models import InstReg


def connect():
    try:
        conn=msdb.connect('mysql.server','ssdiprojectfall2','smspoll','ssdiprojectfall2$default')
        return conn
    except Exception as e:
        return HttpResponse("Error DB")



def home(request):
    code = read('/home/ssdiprojectfall2015/SMSpoll/templates/comingsoon.html')
    t= Template(code)
    c = Context()
    return HttpResponse(t.render(c))

def login(request):
    global error
    code = read('/home/ssdiprojectfall2015/SMSpoll/templates/login.html')
    t= Template(code)
    c = Context()
    return HttpResponse(t.render(c))

def login_check(request):

    mail= request.POST['email2']
    pswd = request.POST['pswd2']

    l=InstReg.objects.get(email=mail)
    if l.password==pswd:
        return HttpResponseRedirect("/auth")
    else:
        code = read('/home/ssdiprojectfall2015/SMSpoll/templates/login.html')
        t= Template(code)
        error="Wrong email or password"
        c = Context({'error':error})
        return HttpResponse(t.render(c))



def signup(request):
    global error
    fname= request.POST['fname']
    lname= request.POST['lname']
    email= request.POST['email']
    password = request.POST['pswd']
    cnfm_pswd=request.POST['cnfm_pswd']

    if password == cnfm_pswd:
        i = InstReg(fname,lname,email,password)
        i.save()
        error="Signed up Successfully,You may login now!!"
        return HttpResponseRedirect('/auth/login')
    else:
        error="Password and Confirm password didn't match!!"
    code = read('/home/ssdiprojectfall2015/SMSpoll/templates/login.html')
    t= Template(code)
    c = Context({'error': error})
    return HttpResponse(t.render(c))