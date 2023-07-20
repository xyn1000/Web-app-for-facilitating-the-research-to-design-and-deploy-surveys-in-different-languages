from django.db import models
from django.utils.timezone import now


class Response(models.Model):
    id = models.BigAutoField(primary_key=True)
    survey_id = models.IntegerField(null=False)
    question_id = models.IntegerField(null=False)
    create_date = models.DateTimeField(default=now)
    contact_info = models.CharField(null=True, max_length=255)
    content = models.JSONField(null=True)
    identifier = models.CharField(blank=True, max_length=100)


class LinkGeneration(models.Model):
    link = models.CharField(max_length=255, primary_key=True)
    survey_id = models.IntegerField()
