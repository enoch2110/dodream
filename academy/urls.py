from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import TemplateView
from academy.views import *
from dodream.helpers import decorated_includes

urlpatterns = patterns('academy.views',
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^student-list$', StudentList.as_view(), name="student-list"),
    url(r'^student-registration', StudentRegistration.as_view(), name="student-registration"),
    url(r'^student-update/(?P<pk>[0-9]+)$', StudentUpdate.as_view(), name="student-update"),
    url(r'^staff-list$', StaffList.as_view(), name="staff-list"),
    url(r'^staff-detail/(?P<pk>\d+)$', StaffDetail.as_view(), name="staff-detail"),
    url(r'^staff-add$', StaffCreate.as_view(), name="staff-add"),
    url(r'^staff-update/(?P<pk>\d+)$', StaffUpdate.as_view(), name="staff-update"),
    url(r'^staff-delete/(?P<pk>\d+)$', StaffDelete.as_view(), name="staff-delete"),
    url(r'^course-list$', CourseCategoryList.as_view(), name="course-list"),
    url(r'^course-add', CourseCreate.as_view(), name="course-add"),
    url(r'^course-category', CourseCategoryCreate.as_view(), name="course-category"),
)

urlpatterns = patterns('',
    (r'', decorated_includes(
        user_passes_test(lambda u: u.is_authenticated() and u.profile.can_use_admin(), login_url='/login'),
        include(urlpatterns))
    ),
)