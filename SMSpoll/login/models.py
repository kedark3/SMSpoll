from django.db import models
from django.contrib import admin
# Create your models here.


class InstReg(models.Model):
    def __str__(self):              # __unicode__ on Python 2
        return self.fname + self.lname
    fname = models.CharField(max_length = 30)
    lname = models.CharField(max_length = 30)
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=30)


class Course(models.Model):
    def __str__(self):              # __unicode__ on Python 2
        return self.course_name
    c_id = models.IntegerField()
    course_name= models.CharField(max_length =50)

class InstCourse(models.Model):
    crn = models.IntegerField(primary_key=True)
    c_id= models.ForeignKey(Course)
    email = models.ForeignKey(InstReg)

class StudReg(models.Model):
    s_id = models.IntegerField(primary_key=True)
    phone_no = models.IntegerField(max_length = 10)
    crn = models.ForeignKey(InstCourse, related_name = 'InstCourse')


admin.site.register(InstReg)
admin.site.register(Course)
admin.site.register(InstCourse)
admin.site.register(StudReg)