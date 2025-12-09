# properties/utils.py

from django.core.cache import cache
from .models import Property  # adjust import if your Property model is elsewhere

def get_all_properties():
    """
    Retrieve all Property objects from cache, or query the database and cache them.
    Cache duration: 1 hour (3600 seconds)
    """
    # Check if queryset is in cache
    all_properties = cache.get('all_properties')
    if all_properties is None:
        # Not in cache, fetch from DB
        all_properties = Property.objects.all()
        # Store queryset in cache for 1 hour
        cache.set('all_properties', all_properties, 3600)
    return all_properties
