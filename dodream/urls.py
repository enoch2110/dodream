from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from academy.forms import StaffAuthenticationForm

from dodream import settings
from dodream.helpers import decorated_includes

import academy

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'', include('academy.urls')),
    (r'^api/', include('api.urls')),
    (r'^attendance/', include('attendance.urls')),
    (r'^admin/', include(admin.site.urls)),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html', 'authentication_form': StaffAuthenticationForm}, name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}, name="logout"),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
)