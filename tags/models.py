from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class TaggedItemManager(models.Manager):
    """Custom manager to easily get tags applied to an Object."""

    def get_tags_for(self, obj_type, obj_id):
        # Get tags applied to an object of type: obj_type & id: obj_id
        content_type = ContentType.objects.get_for_model(obj_type)

        return Tag.objects.filter(
            id__in=TaggedItem.objects.filter(
                content_type=content_type, object_id=obj_id
            ).values("tag_id")
        )


class Tag(models.Model):
    """A tag to be applied on objects."""

    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class TaggedItem(models.Model):
    """An item tagged by a label."""

    objects = TaggedItemManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)  # what tag applied
    # we need type and id of the object where the tag is applied
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
