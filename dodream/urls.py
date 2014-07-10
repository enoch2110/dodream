from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test

from dodream import settings
from dodream.helper import decorated_includes

import academy

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'', include('academy.urls')),
    (r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    (r'^api/', include('api.urls')),
    (r'^admin/', include(admin.site.urls)),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
)