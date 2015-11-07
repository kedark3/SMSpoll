# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.template import Template, Context
from file_read import read
import MySQLdb as msdb
from models import InstReg,StudReg,InstCourse,Course
from twilio.rest import TwilioRestClient
from django.core.mail import send_mail
import random,string
from datetime import datetime
from django.utils import timezone
from dateutil import parser
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


class CourseList(object):
    def __init__(self,crn,c_id,c_name):
        self.crn=crn
        self.c_id=c_id
        self.c_name=c_name

class StudList(object):
    def __init__(self,s_id,phone):
        self.s_id=s_id
        self.phone=phone

def connect():
    try:
        conn=msdb.connect('mysql.server','ssdiprojectfall2','smspoll','ssdiprojectfall2$default')
        return conn
    except Exception as e:
        return HttpResponse("Error DB")



def home(request):
    #try:
    mail=request.session['email2']
    conn=connect()
    cur=conn.cursor()
    cur.execute("select i.crn,c.c_id,c.course_name from login_instcourse as i, login_course as c  where i.c_id_id=c.id and email_id='%s'"%mail)
    results=[]
    for row in cur.fetchall():
        results.append(CourseList(row[0],row[1],row[2]))
    conn.close()
    code = read('/home/ssdiprojectfall2015/SMSpoll/templates/InstructorHome.html')
    t= Template(code)
    c = Context({'courses':results})
    return HttpResponse(t.render(c))



    '''messages = client.messages.list()
    numbers=[]
    for m in messages:
	    if m.status == "received":
		    numbers.append(m)'''

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


def after_course(request):
    conn=connect()
    cur=conn.cursor()
    crn=request.GET['crn']
    cid=request.GET['c-id']
    course_details=list(Course.objects.filter(c_id=cid))
    cur.execute("select s_id, phone_no from login_studreg as s, login_instcourse as c where s.crn_id=c.crn and crn="+crn)
    students=[]
    for row in cur.fetchall():
        students.append(StudList(row[0],row[1]))
    conn.close()
    code = read('/home/ssdiprojectfall2015/SMSpoll/templates/AfterCourseSelection.html')
    t= Template(code)
    c = Context({'course':course_details,'students':students,'count':len(students)})
    return HttpResponse(t.render(c))


def attendace_string(request):
    random_string=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    request.session['random_string']=random_string
    request.session['time1']= datetime.now().replace(microsecond=0)
    code = read('/home/ssdiprojectfall2015/SMSpoll/templates/AttendaceCounter.html')
    t= Template(code)
    c = Context({'string':random_string})
    return HttpResponse(t.render(c))

def show_attendance(request):
    request.session['time2']= datetime.now(timezone.utc).replace(microsecond=0)
    messages = client.messages.list()
    numbers=[]
    for m in messages:
	    if m.status == "received" and ((request.session['time2']-parser.parse(m.date_sent)).seconds)<=90:
		    numbers.append(m)
    code = read('/home/ssdiprojectfall2015/SMSpoll/templates/comingsoon.html')
    t= Template(code)
    c = Context({'numbers':numbers})
    return HttpResponse(t.render(c))

    #,'diff':str((request.session['time2']-parser.parse(messages[0].date_sent)).seconds)+'.....'+str(messages[0].date_sent)+'...'+str(request.session['time2']) })
    '''naive=parser.parse(messages[0].date_sent).replace(tzinfo=None)
    return HttpResponse(request.session['random_string']+str((request.session['time2']-parser.parse(messages[0].date_sent)).seconds)
    +str(request.session['time2'])+str(parser.parse(messages[0].date_sent)))'''