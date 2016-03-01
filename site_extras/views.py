# -*- coding: utf-8 -*-

import datetime
import re
from django.contrib.auth import authenticate as auth_authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, CreateView, RedirectView
from site_extras.forms import InquiryForm
from site_extras.libraries.coolsms import send_sms
from site_extras.models.sitemodels import get_setting
from site_extras.models.utilmodels import SMSVerification


class SMSVerify(View):
    """
    error code
    0: success
    1: warning but show timer
    2: warning and do not show timer
    3: error
    """

    def post(self, request, *args, **kwargs):
        phone_number = request.POST.get("phone_number")
        no_duplicates = "no_duplicates" in request.POST
        now = datetime.datetime.now()

        if SMSVerification.active_objects.filter(phone_number=phone_number).exists():
            verification = SMSVerification.active_objects.get(phone_number=phone_number)
            result = "인증번호가 이미 전송되었습니다."
            remaining = (datetime.timedelta(minutes=3)-(now - verification.datetime)).seconds
            error_code = 1
        elif SMSVerification.is_verified_number(phone_number) and no_duplicates:
            result = "해당 번호는 이미 인증되었습니다."
            remaining = 0
            error_code = 2
        else:
            verification, result = SMSVerification.create(phone_number)
            if verification:
                message_format = get_setting("인증문자", defaults={"type": "문자", "content": "{code}"})
                message = message_format.encode('utf8').format(code=verification.code)
                send_sms(message, str(phone_number))
            remaining = 180 if verification else 0
            error_code = 0 if verification else 2
        return JsonResponse({"result": result, "remaining": remaining, "error_code": error_code})

    @csrf_exempt
    def dispatch(self, request,  *args, **kwargs):
        return super(SMSVerify, self).dispatch(request, *args, **kwargs)


class InquiryCreate(CreateView):
    form_class = InquiryForm
    success_url = reverse_lazy("contact")
    template_name = "site_extras/contact.html"

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, '문의가 접수되었습니다.')
        return super(InquiryCreate, self).form_valid(form)


class UsernameDuplicateCheck(View):

    def get(self, request):
        username = request.GET.get("username", None)
        if username:
            if User.objects.filter(username=username).exists():
                return JsonResponse({"result": 1, "message": "중복된 아이디입니다."})
            elif not re.search(r'^\w+$', username):
                return JsonResponse({"result": 1, "message": "사용 불가능한 아이디입니다."})
            else:
                return JsonResponse({"result": 0, "message": "등록가능한 아이디입니다."})
        else:
            return JsonResponse({"result": 1, "message": "아이디를 입력하세요."})


class OAuth2Authentication(RedirectView):
    url = "/"

    def get(self, request, *args, **kwargs):
        csrf_token = unicode(csrf(request)['csrf_token'])
        if csrf_token == request.GET.get('state'):
            code = request.GET.get("code")
            source = self.kwargs['source']
            user = auth_authenticate(code=code, source=source)
            if user:
                if user.is_active:
                    auth_login(request, user)
                else:
                    error = 'AUTH_DISABLED'
            else:
                error = 'AUTH_FAILED'
        return super(OAuth2Authentication, self).get(request, *args, **kwargs)


class PopupDisable(View):

    def post(self, request):
        if request.is_ajax():
            import datetime
            today = datetime.date.today()
            request.session['popup-%s' % today] = True
            return HttpResponse('ok')
        else:
            return HttpResponseNotAllowed(['POST'])
