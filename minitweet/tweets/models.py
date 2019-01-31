from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from .validator import validate_content


# Create your models here.
class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=140, validators=[validate_content])
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.content)

    def get_absolute_url(self):
        return reverse("tweets:detail", kwargs={"pk": self.pk})
