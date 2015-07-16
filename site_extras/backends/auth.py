# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
import requests
import xmltodict


class OAuth(object):
    source = ""
    access_token = ""

    access_token_request_url = ""
    access_token_request_params = {}
    info_request_url = ""
    info_request_params = {}
    info_request_headers = {}

    def render_response(self, response):
        return None

    def get_info_request_headers(self):
        return self.info_request_headers

    def get_info_request_params(self):
        return self.info_request_params

    def get_user(self, code):
        params = self.access_token_request_params
        params['code'] = code
        r = requests.get(self.access_token_request_url, params=params)
        response = r.json()
        self.access_token = response['access_token']

        r = requests.get(self.info_request_url, headers=self.get_info_request_headers(), params=self.get_info_request_params())
        profile = self.render_response(r)
        if profile:
            user, created = User.objects.get_or_create(username="%s-%s" % (self.source, profile['id']))
            if created:
                user.set_unusable_password()
                if profile.get("email"):
                    user.email = profile.get("email")
                user.save()
            return user
        else:
            return None


class FacebookOAuth(OAuth):
    source = "facebook"
    access_token_request_url = "https://graph.facebook.com/v2.3/oauth/access_token"
    access_token_request_params = {
        'client_id': settings.SITE_EXTRAS_FACEBOOK_CLIENT_ID,
        'client_secret': settings.SITE_EXTRAS_FACEBOOK_CLIENT_SECRET,
        'redirect_uri': settings.SITE_EXTRAS_FACEBOOK_REDIRECT_URI
    }
    info_request_url = "https://graph.facebook.com/me"

    def get_info_request_params(self):
        return {'access_token': self.access_token}

    def render_response(self, response):
        profile = response.json()
        return None if 'error' in profile else profile


class NaverOAuth(OAuth):
    source = "naver"
    access_token_request_url = "https://nid.naver.com/oauth2.0/token"
    access_token_request_params = {
        'grant_type': 'authorization_code',
        'client_id': settings.SITE_EXTRAS_NAVER_CLIENT_ID,
        'client_secret': settings.SITE_EXTRAS_NAVER_CLIENT_SECRET
    }
    info_request_url = "https://apis.naver.com/nidlogin/nid/getUserProfile.xml"

    def get_info_request_headers(self):
        return {'Authorization': u"Bearer " + self.access_token}

    def render_response(self, response):
        xml = response.text
        obj = xmltodict.parse(xml)
        if obj['data']['result']['resultcode'] == '00':
            return obj['data']['response']
        else:
            return None


class KakaoOAuth(OAuth):
    source = "kakao"
    access_token_request_url = "https://kauth.kakao.com/oauth/token"
    access_token_request_params = {
        'grant_type': 'authorization_code',
        'client_id': settings.SITE_EXTRAS_KAKAO_CLIENT_ID,
        'client_secret': settings.SITE_EXTRAS_KAKAO_CLIENT_SECRET
    }
    info_request_url = "https://kapi.kakao.com/v1/user/me"

    def get_info_request_headers(self):
        return {'Authorization': u"Bearer " + self.access_token}

    def render_response(self, response):
        profile = response.json()
        return None if 'code' in profile else profile



class OAuth2Backend(object):
    SOURCES = {
        'facebook': FacebookOAuth,
        'naver': NaverOAuth,
        'kakao': KakaoOAuth
    }

    def authenticate(self, code=None, source=None):
        if not code or not source:
            return None

        oauth = self.SOURCES[source]()
        return oauth.get_user(code)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None