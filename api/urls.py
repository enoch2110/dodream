from django.conf.urls import patterns, url
from api.views import Login, StudentListAPI, AttendanceCreateAPI, CardRegisterAPI, CardDetailAPI

urlpatterns = patterns('',
    url(r'^token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^login$', Login.as_view()),
    url(r'^students', StudentListAPI.as_view()),
    url(r'^attendance-create', AttendanceCreateAPI.as_view()),
    url(r'^card-register', CardRegisterAPI.as_view()),
    url(r'^card-detail', CardDetailAPI.as_view()),
    # url(r'^phone-register', PhoneRegisterAPI.as_view())
)

# auth token : Token e327d6ecff6814ec6bbe37435e8ef3547b76ccbb
# ji-u nfc_id : DBD94755
