# Create your views here.
from __future__ import division
from django.http import HttpResponse,HttpResponseRedirect
from django.template import Template, Context
from file_read import read
from csv_write import csv_write
import MySQLdb as msdb
from models import InstReg,StudReg,InstCourse,Course, ClassTest
from twilio.rest import TwilioRestClient
from django.core.mail import send_mail
import random,string
from datetime import datetime
from django.utils import timezone
from dateutil import parser
import csv
#connecting to twilio account
import os
from urlparse import urlparse
from django.core.urlresolvers import resolve
from django.conf import settings

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

class TestNameList(object):
    def __init__(self,crn,test_id):
        self.crn=crn
        self.test_id=test_id

def connect():
    try:
        conn=msdb.connect('mysql.server','ssdiprojectfall2','smspoll','ssdiprojectfall2$default')
        return conn
    except Exception as e:
        return HttpResponse("Error DB")

questions=()

def home(request):
    try:
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
    except Exception as e:
        error='Please login first!'
        code = read('/home/ssdiprojectfall2015/SMSpoll/templates/login.html')
        t= Template(code)
        c = Context({'error':error,'questions':questions})
        return HttpResponse(t.render(c))


def logout(request):
    request.session['email2']=''
    return HttpResponseRedirect("/auth/login")

def login(request):
    global error
    code = read('/home/ssdiprojectfall2015/SMSpoll/templates/login.html')
    t= Template(code)
    c = Context()
    return HttpResponse(t.render(c))

def login_check(request):

    mail= request.POST['email2']
    pswd = request.POST['pswd2']
    try:
        l=InstReg.objects.get(email=mail)

        if l.password==pswd:
            request.session['email2']=mail
            return HttpResponseRedirect("/auth")
    except Exception:
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
    tests=[]
    cur.execute("select distinct crn_id,test_id from login_classtest where crn_id="+ crn)
    for row in cur.fetchall():
        tests.append(TestNameList(row[0],row[1]))
    conn.close()

    code = read('/home/ssdiprojectfall2015/SMSpoll/templates/AfterCourseSelection.html')
    t= Template(code)
    c = Context({'course':course_details,'students':students,'count':len(students), 'crn':crn, 'tests':tests})
    return HttpResponse(t.render(c))


def attendace_string(request):
    random_string=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    request.session['random_string']=random_string
    #request.session['time1']= datetime.now().replace(microsecond=0)
    request.session['count']=request.GET['count']
    code = read('/home/ssdiprojectfall2015/SMSpoll/templates/AttendaceCounter.html')
    t= Template(code)
    c = Context({'string':random_string,'count':request.GET['count']})
    return HttpResponse(t.render(c))

def show_attendance(request):
    request.session['time2']= datetime.now(timezone.utc).replace(microsecond=0)
    messages = client.messages.list()
    numbers=[]
    for m in messages:
        #==================================Change or to and in statement below later====================================================================
	    if m.status == "received" and ((request.session['time2']-parser.parse(m.date_sent)).seconds)\
	    <=request.session['count'] and m.body==request.session['random_string']:
		        numbers.append(m.from_)


    numbers=list(set(numbers)) # remove duplicates

    code = read('/home/ssdiprojectfall2015/SMSpoll/templates/Attendance.html')
    t= Template(code)
    c = Context({'numbers':numbers})
    return HttpResponse(t.render(c))

def download_attendance(request):
    numbers=request.GET.getlist('numbers')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance'+str(datetime.now())+'.csv"'

    writer = csv.writer(response)
    for n in numbers:
        writer.writerow([n])

    return response

#View for Add Classes
def addrem(request):
    courses=Course.objects.all()
    code = read('/home/ssdiprojectfall2015/SMSpoll/templates/AddRemove.html')
    t= Template(code)
    c = Context({'courses':courses,'email':request.session['email2']})
    return HttpResponse(t.render(c))

def add_course(request):
    cid=request.GET['cid']
    crn=request.GET['crn']
    email=request.GET['email']
    email2=request.session['email2']
    if email==email2:
        conn=connect()
        cur=conn.cursor()
        cur.execute("Insert into login_instcourse values ("+crn+","+cid+",'"+email+"')")
        conn.commit()
        conn.close()
    return HttpResponseRedirect("http://ssdiprojectfall2015.pythonanywhere.com/auth")
def remove_course(request):
    CRN=request.GET['crn']
    email=request.GET['email']
    email2=request.session['email2']

    if email==email2:
        InstCourse.objects.filter(crn=CRN).delete()
    return HttpResponseRedirect("http://ssdiprojectfall2015.pythonanywhere.com/auth")

#-------------------------Test related views-------------------------------------------------------

def create_test(request):
    conn=connect()
    cur= conn.cursor()
    cur.execute("select c_id from login_course where id=(select c_id_id from login_instcourse where crn="+request.GET['crn']+")")
    cid=cur.fetchone()[0]
    conn.close()
    code = read('/home/ssdiprojectfall2015/SMSpoll/templates/CreateTest.html')
    t= Template(code)
    c = Context({'TestName':request.GET['test_id'], 'crn': request.GET['crn'], 'cid':cid,'qid':request.GET['qid']})
    return HttpResponse(t.render(c))

def add_question(request):
    crn=request.GET['crn']
    test_id= request.GET['test_id']
    question= request.GET['question']
    A=request.GET['A']
    B=request.GET['B']
    C=request.GET['C']
    D=request.GET['D']
    correct=request.GET['correct']
    timer= request.GET['timer']
    qid = int(request.GET['qid'])

    conn=connect()
    cur=conn.cursor()
    cur.execute("select max(id) from login_classtest")
    max_id= cur.fetchone()[0]
    if max_id is None:
        max_id=0
    i= ClassTest(max_id+1,crn,test_id,qid,question,A,B,C,D,correct,timer)
    i.save()
    conn.close()
    qid=str(qid+1)
    return HttpResponseRedirect('/auth/create-test/?crn='+crn+'&test_id='+test_id+'&qid='+ qid)


def conduct_test(request):
    request.session['time3']= datetime.now(timezone.utc).replace(microsecond=0)
    code = read('/home/ssdiprojectfall2015/SMSpoll/templates/Test.html')

    try:
        request.sesssion['random_string']
    except Exception:
        random_string=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        request.session['random_string']=random_string
    qid=str(int(request.GET['qid']))
    conn=connect()
    cur=conn.cursor()


    try:
        cur.execute("SELECT * FROM login_classtest WHERE qid='"+qid+"' AND test_id='"+request.GET['test_id']+"' AND crn_id='"+request.GET['crn']+"'")
        question_data=cur.fetchone()

        request.session['test_id']=request.GET['test_id']
        request.session['timer']=question_data[10]
        request.session['ans']=question_data[9]
        conn.close()
        t= Template(code)
        c = Context({'question':question_data[4],'A':question_data[5],'B':question_data[6],
        'C':question_data[7],'D':question_data[8],
        'timer':question_data[10], 'qid':qid, 'crn':request.GET['crn'],
        'random':request.session['random_string']})


        return HttpResponse(t.render(c))
    except Exception:

        cur.execute("select c_id from login_course where id=(select c_id_id from login_instcourse where crn="+request.GET['crn']+")")
        cid=cur.fetchone()[0]
        conn.close()
        return HttpResponseRedirect("/auth/after-course/?crn="+request.GET['crn']+"&c-id="+str(cid))

def show_stats(request):
    request.session['time4']= datetime.now(timezone.utc).replace(microsecond=0)
    messages = client.messages.list()
    messages.sort()
    numbers=[]
    A=[]
    B=[]
    C=[]
    D=[]
    for m in messages:
        #==================================Change or to and in statement below later====================================================================
        if len(m.body)==7:
	        if m.status == "received" and ((request.session['time4']-parser.parse(m.date_sent)).seconds)<=request.session['timer']:
	            if m.body[0:5]== request.session['random_string']:
	                if m.body[6]=='A':
	                    A.append(m.from_)
    	            if m.body[6]=='B':
	    		        B.append(m.from_)
                    if m.body[6]=='C':
			            C.append(m.from_)
                    if m.body[6]=='D':
			            D.append(m.from_)
                    if m.body[6]==request.session['ans']:
                    	numbers.append(m.from_)


    numbers=list(set(numbers))

    csv_write(numbers,str(request.GET['qid']),str(request.session['test_id']),str(request.GET['crn'])) #Writing to csv file

    count=len(A)+len(B)+len(C)+len(D)
    totalStudents= []
    totalStudents.append(A)
    totalStudents.append(B)
    totalStudents.append(C)
    totalStudents.append(D)
    totalStudents= [item for sublist in totalStudents for item in sublist]
    total= len(list(set(totalStudents)))

    if count>0:
        percentA=(len(A)*100/count)
        percentB=(len(B)*100/count)
        percentC=(len(C)*100/count)
        percentD=(len(D)*100/count)
    code = read('/home/ssdiprojectfall2015/SMSpoll/templates/Stats.html')
    t= Template(code)
    c = Context({'numbers':numbers,'countA':percentA,'countB':percentB,'countC':percentC,'countD':percentD,'count':total,
    'crn':request.GET['crn'],'qid':int(request.GET['qid'])+1,'test_id':request.session['test_id']})
    return HttpResponse(t.render(c))

#Download results view===================================
def download(request):
    try:
        os.stat(settings.MEDIA_ROOT+'/result/result'+request.GET['test_id']+request.GET['crn']+'.csv')
        return HttpResponseRedirect('/media/result/result'+request.GET['test_id']+request.GET['crn']+'.csv')
    except OSError:
        conn=connect()
        cur=conn.cursor()
        cur.execute("select c_id from login_course where id=(select c_id_id from login_instcourse where crn="+request.GET['crn']+")")
        cid=cur.fetchone()[0]
        conn.close()
        return HttpResponseRedirect("/auth/after-course/?crn="+request.GET['crn']+"&c-id="+str(cid))