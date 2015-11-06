# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.template import Template, Context,RequestContext
from django.shortcuts import render_to_response
from file_read import read
import MySQLdb as msdb
from models import InstReg,StudReg,InstCourse
from twilio.rest import TwilioRestClient
from django.core.mail import send_mail

#connecting to twilio account
import os
from urlparse import urlparse

from twilio.rest.resources import Connection
from twilio.rest.resources.connection import PROXY_TYPE_HTTP
from twilio import twiml
from django.views.decorators.csrf import csrf_exempt

proxy_url = os.environ.get("http_proxy")
host, port = urlparse(proxy_url).netloc.split(":")
Connection.set_proxy_info(host, int(port), proxy_type=PROXY_TYPE_HTTP)
ACCOUNT_SID = "AC5d22427eb1a348f92d96e38ac7f77b6f"
AUTH_TOKEN = "de92cc787190562f371eebf5971d0a2a"
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)




def connect():
    try:
        conn=msdb.connect('mysql.server','ssdiprojectfall2','smspoll','ssdiprojectfall2$default')
        return conn
    except Exception as e:
        return HttpResponse("Error DB")



def home(request):
    #try:
    mail=request.session['email2']
    messages = client.messages.list()
    numbers=[]
    for m in messages:
	    if m.status == "received":
		    numbers.append(m)
    code = read('/home/ssdiprojectfall2015/SMSpoll/templates/comingsoon.html')
    t= Template(code)
    c = Context({'numbers':numbers})
    return HttpResponse(t.render(c))
    #except Exception as e:
    #    error='Please login first!'
    #    code = read('/home/ssdiprojectfall2015/SMSpoll/templates/login.html')
    #    t= Template(code)
    #    c = Context({'error':error})
    #    return HttpResponse(t.render(c))

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
    rememberMe=request.POST.getlist('checkbox')
    if l.password==pswd:
        request.session['email2']=mail
        if rememberMe==1:
            request.session.set_expiry(0)
            return HttpResponseRedirect("http://www.google.com")
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


def recover_pswd(request):
    pname=request.POST['pname']
    pmail=request.POST['pmail']
    l=InstReg.objects.get(email=pmail)
    if pname == (l.fname+" "+l.lname):
        send_mail('Your Password for SMS Poll' , 'Here is your password for your account on SMSpoll:'+ l.password, 'ssdiprojectfall2015@gmail.com',[pmail], fail_silently=False)
        error="Please Check your email for Password."
    else:
        error="Please check your name or email you entered."
    code = read('/home/ssdiprojectfall2015/SMSpoll/templates/login.html')
    t= Template(code)
    c = Context({'error': error})
    return HttpResponse(t.render(c))

def contact_us(request):
    cname=request.POST['cname']
    cmail=request.POST['cmail']
    message=request.POST['message']
    send_mail('Message from'+ cname , 'Here is message:'+ message, cmail,['ssdiprojectfall2015@gmail.com'], fail_silently=False)
    error="Thank you for Contacting us, we will get back to you shortly!"
    code = read('/home/ssdiprojectfall2015/SMSpoll/templates/login.html')
    t= Template(code)
    c = Context({'error': error})
    return HttpResponse(t.render(c))

@csrf_exempt
def student_reg(request):
    r = twiml.Response()
    try:
        sid=int(request.POST['Body'].split()[0])
        crnn=int(request.POST['Body'].split()[1])
        inst= InstCourse(crn=crnn)
        s= StudReg(s_id=sid,phone_no=request.POST['From'],crn=inst)
        s.save()

        #r.message('Registered successfully!')
    except Exception as e:
        #r.message('Registration error, format should be your 800 ID and CRN. E.g. 800891239 25145.')
        sid=0
    return HttpResponse(r.toxml(), content_type='text/xml')
