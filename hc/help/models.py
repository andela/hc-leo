from django.db import models

class Faq(models.Model):
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=500)
    media = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.question
