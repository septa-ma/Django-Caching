from django.http import JsonResponse
from django.core import serializers
from app.models import Product
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
 
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def cached_sample(request):
    if 'sample' in cache:
        json = cache.get('sample')
        return JsonResponse(json, safe=False)
    else:
        objs = Product.objects.all()
        json = serializers.serialize('json', objs)
        # store data in cache
        cache.set('sample', json, timeout=CACHE_TTL)
        return JsonResponse(json, safe=False)