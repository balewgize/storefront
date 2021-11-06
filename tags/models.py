from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Tag(models.Model):
    """A tag to be applied on objects."""

    label = models.CharField(max_length=255)


class TaggedItem(models.Model):
    """An item tagged by a label."""

    # what tag applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # we need type and id of the object
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
