from django.urls import path

from survey.views import test_view, export_survey, metadata_info_view

urlpatterns = [
    path('response/<int:survey_id>/', test_view),
    path('export/<int:survey_id>/', export_survey),
    path('metadata_info/<int:survey_id>/', metadata_info_view),
]
