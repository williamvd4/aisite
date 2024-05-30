from django.db import models

class MyModel(models.Model):
    """
    A model representing some kind of object with a name, description,
    creation time, and last modification time.
    """
    # Fields
    name = models.CharField(
        max_length=200,
        help_text='The name of the object.'
    )
    description = models.TextField(
        help_text='A detailed description of the object.'
    )
    creation_time = models.DateTimeField(
        auto_now_add=True,
        help_text='The time when the object was first created.'
    )
    last_modified_time = models.DateTimeField(
        auto_now=True,
        help_text='The time when the object was last modified.'
    )
