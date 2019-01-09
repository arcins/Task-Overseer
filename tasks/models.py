from django.db import models


class Tasks(models.Model):
    """
    Tasks Model
    Defines the attributes of a task
    """
    title = models.CharField(max_length=255)
    is_done = models.BooleanField()
    description = models.TextField()
    date = models.DateTimeField(blank=True, null=True)

    def get_done(self):
        return self.is_done

    def __repr__(self):
        return self.title + ' is added.'
