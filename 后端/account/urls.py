from django.conf.urls import url
from django.urls import path, include
from rest_auth.views import PasswordResetConfirmView, PasswordResetView

from account.views import *

urlpatterns = [
    url(r'^password/reset/confirm/$', PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),

    url(r'^register/', include('rest_auth.registration.urls')),
    url(r'^update/$', update_user),
    url(r'^', include('rest_auth.urls')),
    path('password/reset/', PasswordResetView.as_view(), name='reset_password'),
    url(r'^verification/email/$', send_verification_email),
    url(r'^delete/$', delete_user),
    url(r'^allauth/', include('allauth.urls')),
]
