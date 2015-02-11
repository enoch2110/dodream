# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group
from django.db import models
import datetime
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver


class Academy(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="academy")
    address = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    def get_students(self):
        return Student.objects.filter(academy=self)

    def get_staffs(self):
        return Staff.objects.filter(academy=self)

    def get_subjects(self):
        return Subject.objects.filter(academy=self)

    # def get_courses(self):
    #     return Course.objects.filter(academy=self)


class Setting(models.Model):
    name = models.CharField(max_length=100)
    value = models.TextField()
    academy = models.ForeignKey(Academy)


class Profile(models.Model):
    user = models.OneToOneField(User, blank=True, null=True)
    phone_id = models.CharField(max_length=500, blank=True, null=True)

    def __unicode__(self):
        return self.get_name() + "(" + self.get_username() + ")"

    def get_name(self):
        instance = self.get_instance()
        user = self.user
        if instance:
            name = instance.__class__.__name__ +": "+instance.name
        elif user:
            user_fullname = user.last_name + user.first_name
            name = user_fullname if user_fullname else "no name"
        else:
            name = "no name"
        return name

    def get_username(self):
        username = self.user.username if self.user else "no user"
        return username

    def can_use_admin(self):
        return Staff.objects.filter(profile__user=self.user).exists()

    def get_instance(self):
        if Student.objects.filter(profile=self).exists():
            instance = self.student
        elif Staff.objects.filter(profile=self).exists():
            instance = self.staff
        elif Guardian.objects.filter(profile=self).exists():
            instance = self.guardian
        else:
            instance = None
        return instance

    def get_type(self):
        instance = self.get_instance()
        return instance.__class__.__name__.lower() if instance else ""

    def get_academy(self):
        if self.get_type() in ["student", "staff"]:
            academy = self.get_instance().academy
        elif self.get_type() in ["guardian"]:
            academy = self.get_instance().student.academy
        else:
            academy = None
        return academy


# class Textbook(models.Model):
#     name = models.CharField(max_length=100)
#     is_paid = models.BooleanField(default=False)


class Student(models.Model):
    GENDER_CHOICES = [(True, "남"), (False, "여")]
    ATTEND_METHOD_CHOICES = [(0, "정보없음"), (1, "도보"), (2, "통학버스")]

    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    image = models.ImageField(upload_to="academy/student", default="defaults/avatar.png")
    gender = models.BooleanField(choices=GENDER_CHOICES, default=False)
    birthday = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    school = models.CharField(max_length=50, blank=True, null=True)
    attend_method = models.IntegerField(choices=ATTEND_METHOD_CHOICES)
    use_sms = models.BooleanField(default=False)
    registered_date = models.DateField(default=datetime.date.today())
    information = models.TextField(blank=True, null=True)
    profile = models.OneToOneField(Profile)
    academy = models.ForeignKey(Academy)
    textbook = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_subjects(self):
        return StudentSubject.objects.filter(student=self)

    # def get_total_fees(self):
    #     total_fees = 0
    #     for lecture in StudentLecture.objects.filter(student=self):
    #         total_fees += lecture.get_fee()
    #     return total_fees
    #
    # def get_total_payments(self):
    #     total_payments = self.payment_set.aggregate(total_payments=Sum('amount'))['total_payments']
    #     if not total_payments:
    #         total_payments = 0
    #     return total_payments
    #
    # def is_paid(self):
    #     return self.get_total_fees() - self.get_total_payments() <= 0
    #
    # def get_total_unpaid_amount(self):
    #     return self.get_total_fees() - self.get_total_payments()
    #
    # def get_total_unpaid_entries(self):
    #     if not self.is_paid():
    #         total_unpaid_amount = self.get_total_unpaid_amount()
    #         lectures = StudentLecture.objects.filter(student=self).order_by('-date', '-fee')      #descending(최신순), descending(큰금액순)
    #         total_unpaid_entries = []
    #         for lecture in lectures:
    #             lecture_price = lecture.get_fee()
    #             if total_unpaid_amount > 0:
    #                 total_unpaid_amount -= lecture_price
    #                 status = 'unpaid' if total_unpaid_amount >= 0 else 'partially paid'
    #                 unpaid_amount = lecture_price if total_unpaid_amount >= 0 else lecture_price + total_unpaid_amount
    #                 total_unpaid_entries.append({'lecture': lecture.lecture, 'date': lecture.date, 'fee': lecture.fee,
    #                                              'status': status, 'amount': unpaid_amount})
    #         total_unpaid_entries.reverse()      #unpaid-detail에서 오래된 순으로 출력하기 위해서
    #     return total_unpaid_entries
    #
    # def get_last_unpaid_lecture(self):
    #     total_unpaid_entries = self.get_total_unpaid_entries()
    #     print total_unpaid_entries.index[total_unpaid_entries.count()-1]
    #     return total_unpaid_entries.index[total_unpaid_entries.count()-1]


class Staff(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    image = models.ImageField(upload_to="academy/staff", blank=True, null=True)
    birthday = models.DateField()
    address = models.CharField(max_length=200, blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    group = models.ForeignKey(Group)
    # main_course = models.ForeignKey("Course", blank=True, null=True)
    main_subject = models.ForeignKey("Subject", blank=True, null=True)
    specs = models.TextField(max_length=100, blank=True, null=True)
    registered_date = models.DateField(default=datetime.date.today())
    profile = models.OneToOneField(Profile)
    academy = models.ForeignKey(Academy)

    def __unicode__(self):
        return self.group.name+" "+self.name

    def get_name(self):
        return self.name


class Guardian(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    relation = models.CharField(max_length=100)
    student = models.ForeignKey(Student)
    profile = models.OneToOneField(Profile)
    # phone_id = models.CharField(max_length=50, blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=100)
    academy = models.ForeignKey(Academy)

    def __unicode__(self):
        return self.name

    def get_subjects(self):
        return Subject.objects.filter(category=self, is_active=True)


class Subject(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey("Category")
    price = models.IntegerField()
    information = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return "(" + self.category.name + ") " + self.name


class StudentSubject(models.Model):
    subject = models.ForeignKey("Subject")
    student = models.ForeignKey("Student")
    fee = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.subject.__unicode__() + "-" + self.student.__unicode__()

    def get_fee(self):
        return self.fee

    # def is_first_subject(self):
    #     return self.subject == self.student.get_subjects()
    #
    # def is_last_subject(self):
    #     return self.subject == self.student.get_subjects()[1]


########################################################################################################################
# class LectureDateTime(models.Model):
#     """
#     type
#     1: begin
#     2: end
#     0: exceptional
#     """
#     type = models.IntegerField()
#     value = models.CharField(max_length=20)
#     date = models.DateField()
#     time = models.TimeField()
#     lecture = models.ForeignKey("Lecture")
#
#     def __unicode__(self):
#         return self.lecture.__unicode__()+self.lecture.staff.__unicode__()
#
#
class Course(models.Model):
    name = models.CharField(max_length=100)
#     category = models.ForeignKey("CourseCategory")
#     price = models.IntegerField()
#     price_info = models.TextField(blank=True, null=True)
#     syllabus = models.TextField(blank=True, null=True)
#     is_active = models.BooleanField(default=True)
#     academy = models.ForeignKey(Academy)
#
#     def __unicode__(self):
#         return self.name
#
#     def get_lectures(self):
#         return Lecture.objects.filter(course=self)
#
#
# class CourseCategory(models.Model):
#     name = models.CharField(max_length=100)
#     parent = models.ForeignKey("self", blank=True, null=True)
#
#     def __unicode__(self):
#         if self.parent == self:
#             return self.name + " (incorrect parent)"
#         return self.parent.__unicode__()+" > "+self.name if self.parent else self.name
#
#     def children(self):
#         return CourseCategory.objects.filter(parent=self)
#
#     def is_leaf(self):
#         return not CourseCategory.objects.filter(parent=self).exists()
#
#     def belongs_to(self, ancestor):
#         instance = self
#         while instance:
#             if instance == ancestor:
#                 return True
#             instance = instance.parent
#         return False
#
#     def get_leaves(self):
#         leaves = []
#         for course_category in CourseCategory.objects.filter(parent=self):
#             if course_category.is_leaf():
#                 leaves.append(course_category.id)
#             else:
#                 leaves += course_category.get_leaves()
#         return leaves
#
#     def get_courses(self):
#         return Course.objects.filter(category__id__in=self.get_leaves())
#
#
# class StudentLecture(models.Model):
#     lecture = models.ForeignKey("Lecture")
#     student = models.ForeignKey("Student")
#     date = models.DateField(null=True, blank=True)
#     fee = models.IntegerField(null=True, blank=True)
#
#     def __unicode__(self):
#         return self.lecture.__unicode__()+" "+self.student.__unicode__()
#
#     def get_fee(self):
#         return self.fee
#
#
# class Lecture(models.Model):
#     code = models.CharField(max_length=50)
#     course = models.ForeignKey("Course")
#     staffs = models.ManyToManyField("Staff")
#     students = models.ManyToManyField("Student")
#     is_online = models.BooleanField(default=False)
#
#     def __unicode__(self):
#         return self.course.name
#
#     def get_lecture(self):
#         return Lecture.objects.filter(category__id__in=self.get_leaves())
#
#     def get_stu_num(self):
#         return Lecture.objects.filter(course=self.course, number=self.number).count()
#
#     def get_price(self): #TODO course_price 계산법 수정 (할인률, lecture에 따로 할당된 금액 등등)
#         return self.course.price*(1-self.discount/100)
#
#
# class Payment(models.Model):
#     student = models.ForeignKey(Student)
#     amount = models.IntegerField()
#     datetime = models.DateTimeField(auto_now=True)
#     receipt_number = models.CharField(max_length=100, blank=True, null=True)
#
#     def __unicode__(self):
#         return str(self.datetime)+" "+self.student.name +" "+str(self.amount)
