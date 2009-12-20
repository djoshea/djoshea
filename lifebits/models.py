from django.db import models
from django.contrib.contenttypes.models import ContentType

class Bit(models.Model):
    active = models.BooleanField(default=False)

    dt = models.DateTimeField(auto_now_add=True, 
                              verbose_name='Display Date')
    dt_created = models.DateTimeField(auto_now_add=True, editable=False)
    dt_modified = models.DateTimeField(auto_now=True, editable=False)

    slug = models.SlugField(max_length=200)

    title = models.CharField(max_length=200)
    abstract = models.TextField(blank=True)

    excerpt_html = models.TextField(editable=False, blank=True)
    body_html = models.TextField(editable=False, blank=True)

    # child type tracking
    content_type = models.ForeignKey(ContentType, editable=False, null=True)

    # Managers
    from query import BitQuerySet
    bits = BitQuerySet.as_manager(as_leaves=False) # as type Bit, default
    leafbits = BitQuerySet.as_manager(as_leaves=True) # as leaf class type

    def save(self, *args, **kwargs):
        "Saves reference to actual leaf subclass in content_type"
        if(not self.content_type):
            self.content_type = ContentType.objects\
                                           .get_for_model(self.__class__)
            super(Bit, self).save(*args, **kwargs)

    def as_leaf_class(self):
        "Returns the corresponding instance in the leaf subclass type"
        content_type = self.content_type
        model = content_type.model_class()
        if (model == Bit):
            return self
        return model.objects.get(id=self.id)

    class Meta:
        get_latest_by = 'dt'
        ordering = ['-dt']

