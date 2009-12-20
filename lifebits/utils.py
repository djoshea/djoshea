from django.db import models

# Manager with custom QuerySet
# http://adam.gomaa.us/blog/2009/feb/16/subclassing-django-querysets/
class QuerySetManager(models.Manager):

    #http://docs.djangoproject.com/en/dev/topics/db/managers/#using-managers-for-related-object-access    
    use_for_related_fields = True

    def __init__(self, queryset_class=models.query.QuerySet,
                 *args, **kwargs):
        "Pass in extra arguments to be sent to the QuerySet"
        self.queryset_class = queryset_class
        self.qs_args = args
        self.qs_kwargs = kwargs
        super(QuerySetManager, self).__init__()

    def get_query_set(self):
        "Instantiates a QuerySet with the args passed to __init__"
        return self.queryset_class(model=self.model,
                                   *self.qs_args,
                                   **self.qs_kwargs)

    # try locally, then defer to query set's methods
    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args) 

# Auto conversion to Manager class
class QuerySet(models.query.QuerySet):

    @classmethod
    def as_manager(cls, ManagerClass=QuerySetManager, *args, **kwargs):
        return ManagerClass(cls, *args, **kwargs)

