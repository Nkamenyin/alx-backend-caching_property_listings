# properties/utils.py

from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property  # adjust import if your Property model is elsewhere
import logging

logger = logging.getLogger(__name__)


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


def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics and calculate hit ratio.

    Returns:
        dict: {
            "hits": int,
            "misses": int,
            "hit_ratio": float
        }
    """
    try:
        # Get the raw Redis connection
        redis_conn = get_redis_connection("default")
        info = redis_conn.info("stats")

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total = hits + misses

        hit_ratio = hits / total if total > 0 else 0.0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": round(hit_ratio, 2)
        }

        logger.info(f"Redis cache metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Failed to get Redis metrics: {e}")
        return {
            "hits": 0,
            "misses": 0,
            "hit_ratio": 0.0
        }
