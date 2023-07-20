from django.contrib import admin
from django.urls import path, include

import django_core.views

urlpatterns = [
    path('api/', include('surveybuilder.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('survey/', include('survey.urls')),
    path('', django_core.views.status),
    path('api/st/', include('surveytaker.urls'))
]
