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
    def __str__(self):              # __unicode__ on Python 2
        return str(self.crn)
    crn = models.IntegerField(primary_key=True)
    c_id= models.ForeignKey(Course)
    email = models.ForeignKey(InstReg)
    class Meta:
        unique_together = (("crn","c_id"))

class StudReg(models.Model):
    def __str__(self):              # __unicode__ on Python 2
        return str(self.s_id) + str(self.crn)
    s_id = models.IntegerField()
    phone_no = models.CharField(max_length = 20)
    crn = models.ForeignKey(InstCourse, related_name = 'InstCourse')
    class Meta:
        unique_together = (("s_id","phone_no", "crn"),)

class ClassTest(models.Model):
    def __str__(self):              # __unicode__ on Python 2
        return str(self.crn) + self.test_id + self.question_string

    crn = models.ForeignKey(InstCourse, related_name = 'CrnTest')
    test_id = models.CharField(max_length = 50)
    qid= models.IntegerField(default=1)
    question_string = models.CharField(max_length = 200)
    value_A = models.CharField(max_length = 100)
    value_B = models.CharField(max_length = 100)
    value_C = models.CharField(max_length = 100)
    value_D = models.CharField(max_length = 100)
    correct_ans = models.CharField(max_length = 1)
    timer_value = models.IntegerField()
    class Meta:
        unique_together = (("crn","test_id", "question_string"),)

admin.site.register(InstReg)
admin.site.register(Course)
admin.site.register(InstCourse)
admin.site.register(StudReg)
admin.site.register(ClassTest)