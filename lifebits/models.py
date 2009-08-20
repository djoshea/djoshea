from django.db import models
from django.contrib.contenttypes.models import ContentType
from utils import QuerySet

class Bit(models.Model):

    active = models.BooleanField(default=False)

    dt = models.DateTimeField(auto_now_add=True, 
                              verbose_name='Display Date')
    dt_created = models.DateTimeField(auto_now_add=True, editable=False)
    dt_modified = models.DateTimeField(auto_now=True, editable=False)

    slug = models.SlugField(prepopulate_from='title', 
                            max_length=200)

    title = models.CharField(max_length=200)
    abstract = models.TextField(blank=True)

    excerpt_html = models.TextField(editable=False, blank=True)
    body_html = models.TextField(editable=False, blank=True)

    # child type tracking
    content_type = models.ForeignKey(ContentType, editable=False, null=True)

    # Managers
    bits = BitQuerySet.as_manager(as_leaves=False) # as type Bit, default
    leafbits = BitQuerySet.as_manager(as_leaves=True) # as leaf class type

    def save(self, *args, **kwargs):
        "Saves reference to actual leaf subclass in content_type"
        if(not self.content_type):
            self.content_type = ContentType.objects.get_for_model(self.__class__)
            super(Meal, self).save(*args, **kwargs)

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

class BitQuerySet(QuerySet):
    """
    Base for QuerySets on Bit class, optionally returns
    as_leaf_class for each item if as_leaves True in __init__
    Call BitQuerySet.as_manager(as_leaves=...) to get Manager instance
    """

    def __init__(as_leaves=False, *args, **kwargs):
        self.as_leaves = as_leaves

    def __getitem__(self, k):
        result = super(LeafClassQuerySet, self).__getitem__(k)

        if self.as_leaves and isinstance(result, models.Model):
            return result.as_leaf_class()
        else :
            return result

    def __iter__(self):
        supiter = super(SubclassingQuerySet, self).__iter__()
        for item in supiter:
            if self.as_leaves:
                yield item.as_leaf_class()
            else:
                yield item

    def active(self):
        "Excludes active=False Bit instances"
        return self.filter(active=True)

