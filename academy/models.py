# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
import datetime


class Student(models.Model):
    GENDER_CHOICES = [(True, "남"), (False, "여")]
    ATTEND_METHOD_CHOICES = [(1, "도보"), (2, "통학버스")]

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="academy/student")
    gender = models.BooleanField(choices=GENDER_CHOICES)
    birthday = models.DateField()
    email = models.EmailField()
    address = models.CharField(max_length=200, blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    school = models.CharField(max_length=50, blank=True, null=True)
    attend_method = models.IntegerField(choices=ATTEND_METHOD_CHOICES)
    use_sms = models.BooleanField()
    registered_date = models.DateField(default=datetime.date.today())
    information = models.TextField(blank=True, null=True)
    user = models.OneToOneField(User, blank=True, null=True)


class Guardian(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=20, blank=True, null=True)
    relation = models.CharField(max_length=100)
    student = models.ForeignKey(Student)
    user = models.OneToOneField(User, blank=True, null=True)


class Course(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey("CourseCategory")
    price = models.IntegerField()
    price_info = models.TextField(blank=True, null=True)
    syllabus = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


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