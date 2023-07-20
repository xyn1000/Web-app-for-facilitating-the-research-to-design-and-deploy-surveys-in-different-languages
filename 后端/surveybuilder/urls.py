from django.conf.urls import url 
from surveybuilder import views

urlpatterns = [
    # post: duplicates a block
    url(r'^blocks/duplicate/(?P<id>[0-9]+)', views.duplication_block),
    # post: duplicates a question
    url(r'^questions/duplicate/(?P<id>[0-9]+)', views.duplication_question),
    # get/delete/patch/post: multichoice questions by ID, for handling buttons
    url(r'^questions/multi/(?P<id>[0-9]+)', views.choices_data),
    # get/delete/patch/post: buttonrow questions by ID, for handling buttons
    url(r'^questions/buttonrow/(?P<id>[0-9]+)', views.buttonrow_data),
    # get/delete/patch/post: drag and drop questions by ID, for handling cards
    url(r'^questions/draganddrop/(?P<id>[0-9]+)/cards$', views.dragdropcard_data),
    # get/delete/patch/post: drag and drop questions by ID, for handling categories
    url(r'^questions/draganddrop/(?P<id>[0-9]+)/choices$', views.dragdropchoice_data),
    # get/delete/patch/post: 
    url(r'^questions/buttonrow/(?P<id>[0-9]+)', views.buttonrow_data),
    # patch: questions subtype by ID
    url(r'^questions/inner/(?P<id>[0-9]+)', views.question_inner),
    # get/patch/delete: questions by ID
    url(r'^questions/(?P<id>[0-9]+)', views.question_info),
    # post: returns all article information
    url(r'^article', views.article_information),
    # get/post: questions in a block, post should create the type too
    url(r'^blocks/(?P<id>[0-9]+)/questions$', views.question_list),
    # get/delete: find blocks ID
    url(r'^blocks/(?P<id>[0-9]+)$', views.block_info),
    # get/post: blocks in a given survey
    url(r'^surveys/(?P<id>[0-9]+)/blocks$', views.block_list),
    # get: returns a survey with its blocks and questions. 
    url(r'^surveys/(?P<id>[0-9]+)/data$', views.survey_data),
    # get/patch/delete: a survey by its ID
    url(r'^surveys/(?P<id>[0-9]+)$', views.survey_info),
    # get/post: get all surveys in a list
    url(r'^surveys', views.survey_list),
    # get: API documentation
    url(r'^documentation', views.schema_view, name="Survey API"),
]
