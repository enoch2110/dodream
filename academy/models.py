# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group, AbstractBaseUser
from django.db import models
import datetime


class Academy(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="academy")
    address = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, blank=True, null=True)

    def __unicode__(self):
        name = "No Name"

        return name + "'s profile (" + (self.user.username if self.user else "No User") +")"

    def get_name(self):
        return self.user.last_name+" "+self.user.first_name

    def can_use_admin(self):
        return Staff.objects.filter(user=self.user).exists()


class Student(models.Model):
    GENDER_CHOICES = [(True, "남"), (False, "여")]
    ATTEND_METHOD_CHOICES = [(1, "도보"), (2, "통학버스")]

    name = models.CharField(max_length=100)
    email = models.EmailField(help_text="계정명으로 사용됩니다.")
    image = models.ImageField(upload_to="academy/student")
    gender = models.BooleanField(choices=GENDER_CHOICES)
    birthday = models.DateField()
    address = models.CharField(max_length=200, blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    school = models.CharField(max_length=50, blank=True, null=True)
    attend_method = models.IntegerField(choices=ATTEND_METHOD_CHOICES)
    use_sms = models.BooleanField()
    registered_date = models.DateField(default=datetime.date.today())
    information = models.TextField(blank=True, null=True)
    user = models.OneToOneField(User)
    academy = models.ForeignKey(Academy)

    def __unicode__(self):
        return self.name


class Staff(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(help_text="계정명으로 사용됩니다.")
    image = models.ImageField(upload_to="academy/staff", blank=True, null=True)
    birthday = models.DateField()
    address = models.CharField(max_length=200, blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    group = models.ForeignKey(Group)
    main_course = models.ForeignKey("Course", blank=True, null=True)
    specs = models.TextField(max_length=100, blank=True, null=True)
    registered_date = models.DateField(default=datetime.date.today())
    user = models.OneToOneField(User)
    academy = models.ForeignKey(Academy)

    def __unicode__(self):
        return self.group.name+" "+self.name

    def get_name(self):
        return self.name


class Guardian(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=20, blank=True, null=True)
    relation = models.CharField(max_length=100)
    student = models.ForeignKey(Student)
    user = models.OneToOneField(User)


class Course(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey("CourseCategory")
    price = models.IntegerField()
    price_info = models.TextField(blank=True, null=True)
    syllabus = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class CourseCategory(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey("self", blank=True, null=True)

    def __unicode__(self):
        return self.parent.__unicode__()+" > "+self.name if self.parent else self.name

    def children(self):
        return CourseCategory.objects.filter(parent=self)

    def is_leaf(self):
        return not CourseCategory.objects.filter(parent=self).exists()

    def belongs_to(self, ancestor):
        instance = self
        while instance:
            if instance == ancestor:
                return True
            instance = instance.parent
        return False

    def get_leaves(self):
        leaves = []
        for course_category in CourseCategory.objects.filter(parent=self):
            if course_category.is_leaf():
                leaves.append(course_category.id)
            else:
                leaves += course_category.get_leaves()
        return leaves

    def get_courses(self):
        return Course.objects.filter(category__id__in=self.get_leaves())


class Lecture(models.Model):
    number = models.CharField(max_length=50)
    course = models.ForeignKey("Course")
    staff = models.ManyToManyField("Staff")
    student = models.ManyToManyField("Student")
    is_online = models.BooleanField()

    def __unicode__(self):
        return self.course.name

    def get_lecture(self):
        return Lecture.objects.filter(category__id__in=self.get_leaves())

    def get_stu_num(self):
        return Lecture.objects.filter(course=self.course, number=self.number).count()


class Payment(models.Model):
    student = models.ForeignKey(Student)
    amount = models.IntegerField()
    datetime = models.DateTimeField(default=datetime.datetime.today())
    receipt_number = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return str(self.datetime)+" "+self.student.name+" "+str(self.amount)
