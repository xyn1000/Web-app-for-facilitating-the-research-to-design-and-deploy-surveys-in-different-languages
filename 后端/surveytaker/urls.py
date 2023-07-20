from django.conf.urls import url
from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt

from surveytaker import views

urlpatterns = [
   url(r'^survey/$', csrf_exempt(views.ResponseView.as_view())),
   re_path(r'^survey/(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{10}$', csrf_exempt(views.SurveyAPIView.as_view()))
]
