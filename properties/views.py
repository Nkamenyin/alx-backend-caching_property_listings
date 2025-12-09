from django.http import JsonResponse
from django.core.cache import cache
from .models import Property
from .utils import get_all_properties  # import the helper function


def property_list(request):
    """
    Returns all properties as JSON.
    Cached in Redis for 1 hour using low-level cache API.
    """
    # Try to get cached queryset
    properties = cache.get('all_properties')
    
    if properties is None:
        # Not in cache, fetch from DB and convert to list of dicts
        properties = list(
            Property.objects.all().values(
                'id', 'title', 'description', 'price', 'location', 'created_at'
            )
        )
        # Cache the list for 1 hour
        cache.set('all_properties', properties, 3600)

    return JsonResponse({
        "data": properties
    })
