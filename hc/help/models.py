from django.db import models

class Faq(models.Model):
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=500)
