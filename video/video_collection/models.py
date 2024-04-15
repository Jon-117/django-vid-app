from urllib import parse
from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.

class Video(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    notes = models.TextField(blank=True, null=True)  # blank acceptable, null in db acceptable
    video_id = models.CharField(max_length=40, unique=True)

    def save(self, *args, **kwargs):
        url_components = parse.urlparse(self.url)
        query_string = url_components.query
        if not query_string:
            raise ValidationError('Invalid YouTube URL')
        parameters = parse.parse_qs(query_string, strict_parsing=True)
        v_parameters_list = parameters.get('v')  # return None if not found (looking for '?')
        if not v_parameters_list:
            raise ValidationError('Invalid YouTube URL')
        self.video_id = v_parameters_list[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}\nNotes: {self.notes[:200]} '
