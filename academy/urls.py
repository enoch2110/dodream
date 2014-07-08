from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from academy.views import StudentRegistration, StudentList, CourseCreate, CourseCategoryCreate, CourseCategoryList

urlpatterns = patterns('academy.views',
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^student-list$', StudentList.as_view(), name="student-list"),
    url(r'^student-registration', StudentRegistration.as_view(), name="student-registration"),
    url(r'^course-list$', CourseCategoryList.as_view(), name="course-list"),
    url(r'^course-add', CourseCreate.as_view(), name="course-add"),
    url(r'^course-category', CourseCategoryCreate.as_view(), name="course-category"),
)
