from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.static import serve
from django.contrib.auth.decorators import user_passes_test
from academy.forms import StaffAuthenticationForm

from dodream import settings
from dodream.helpers import decorated_includes

import academy

admin.autodiscover()

urlpatterns = [
    url(r'', include('academy.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^website/', include('website.urls')),
    url(r'^attendance/', include('attendance.urls')),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login,
        {'template_name': 'academy/login.html', 'authentication_form': StaffAuthenticationForm}, name="login"),
    url(r'^logout/$', logout, {'template_name': 'academy/logout.html'}, name="logout"),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),
    ]
