from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers


def cached_list(timeout=120):
    """
    Class decorator: caches the list endpoint for `timeout` seconds.
    Varies on Accept-Language so different languages get separate cache entries.

    Usage:
        @cached_list(120)
        class MyListView(generics.ListAPIView): ...
    """
    def decorator(cls):
        cls = method_decorator(cache_page(timeout), name='list')(cls)
        cls = method_decorator(vary_on_headers('Accept-Language'), name='list')(cls)
        return cls
    return decorator
