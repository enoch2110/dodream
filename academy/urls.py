from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import TemplateView
from academy.views import *
from dodream.helpers import decorated_includes

urlpatterns = patterns('academy.views',
    # url(r'^$', TemplateView.as_view(template_name="academy/index.html")),
    url(r'^$', StudentList.as_view()),
    url(r'^setting$', AcademySetting.as_view(), name="academy-setting"),
    url(r'^student-list$', StudentList.as_view(), name="student-list"),
    url(r'^student-registration', StudentRegistration.as_view(), name="student-registration"),
    url(r'^student-update/(?P<pk>[0-9]+)$', StudentUpdate.as_view(), name="student-update"),
    url(r'^staff-list$', StaffList.as_view(), name="staff-list"),
    url(r'^staff-detail/(?P<pk>\d+)$', StaffDetail.as_view(), name="staff-detail"),
    url(r'^staff-add$', StaffCreate.as_view(), name="staff-add"),
    url(r'^staff-update/(?P<pk>\d+)$', StaffUpdate.as_view(), name="staff-update"),
    url(r'^staff-delete/(?P<pk>\d+)$', StaffDelete.as_view(), name="staff-delete"),
    url(r'^category-add$', CategoryCreate.as_view(), name="category-add"),
    url(r'^subject-list$', SubjectList.as_view(), name="subject-list"),
    url(r'^subject-add', SubjectCreate.as_view(), name="subject-add"),
    url(r'^subject-update/(?P<pk>\d+)$', SubjectUpdate.as_view(), name="subject-update"),
    url(r'^subject-delete/(?P<pk>\d+)$', SubjectDelete.as_view(), name="subject-delete"),
    url(r'^student-subject-list$', StudentSubjectList.as_view(), name="student-subject-list"),
    url(r'^student-subject-detail/(?P<pk>\d+)$', StudentSubjectDetail.as_view(), name="student-subject-detail"),
    url(r'^student-subject-add/(?P<pk>\d+)$', StudentSubjectCreate.as_view(), name="student-subject-add"),
    url(r'^student-subject-update/(?P<pk>\d+)$', StudentSubjectUpdate.as_view(), name="student-subject-update"),
    url(r'^student-subject-delete/(?P<pk>\d+)$', StudentSubjectDelete.as_view(), name="student-subject-delete"),

    # url(r'^course-list$', CourseCategoryList.as_view(), name="course-list"),
    # url(r'^course-add', CourseCreate.as_view(), name="course-add"),
    # url(r'^course-category', CourseCategoryCreate.as_view(), name="course-category"),
    # url(r'^course-update/(?P<pk>\d+)$', CourseUpdate.as_view(), name="course-update"),
    # url(r'^course-delete/(?P<pk>\d+)$', CourseDelete.as_view(), name="course-delete"),
    # url(r'^payment-list$', PaymentList.as_view(), name="payment-list"),
    # url(r'^payment-add$', PaymentCreate.as_view(), name="payment-add"),
    # url(r'^payment-update/(?P<pk>\d+)$', PaymentUpdate.as_view(), name="payment-update"),
    # url(r'^payment-delete/(?P<pk>\d+)$', PaymentDelete.as_view(), name="payment-delete"),
    # url(r'^unpaid-list$', UnpaidList.as_view(), name="unpaid-list"),
    # url(r'^unpaid-detail/(?P<pk>\d+)$', UnpaidDetail.as_view(), name="unpaid-detail"),
    # url(r'^send-sms$', sms, name="send-sms"),
    # url(r'^lecture-list', LectureList.as_view(), name="lecture-list"),
    # url(r'^lecture-add', LectureCreate.as_view(), name="lecture-add"),
    # url(r'^lecture-apply/(?P<pk>\d+)$', LectureUpdate.as_view(), name="lecture-apply"),
    # url(r'^textbook-update$', TextbookUpdate.as_view(), name="textbook-update"),
    # url(r'^calendar', TemplateView.as_view(template_name="academy/calendar.html")),
    # #TYPE: student:0, staff:1
    # url(r'^account-create/(?P<type>\d+)/(?P<pk>\d+)$', AccountCreate.as_view(), name="account-create"),
)
    

urlpatterns = patterns('',
    (r'', decorated_includes(
        user_passes_test(lambda u: u.is_authenticated() and u.profile.can_use_admin(), login_url='/login'),
        include(urlpatterns))
    ),
    url(r'^subject-fee$', 'academy.views.subject_fee'),
    url(r'^textbook-save/(?P<stu_id>\d+)$', 'academy.views.textbook_save')
)