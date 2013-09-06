from django.db import models


class Job(models.Model):
    """An individual Job."""

    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    data = models.TextField(blank=True, null=True)

    created = models.DateTimeField()

    def __unicode__(self):
        return self.title
