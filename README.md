# Django-caching

**Caching is one of the method which make websites faster. It is cost efficient and saves CPU processing time.**

# A) Caching?

- **Caching is the process of storing recently generated results in memory. Those results can then be used in future when requested again.**

# B) Django Caching Types:

- **1- Memcached:** Memcached is a memory-based, key-value store for small chunks of data. It supports distributed caching across multiple servers.

- **2- Database:** The cache fragments are stored in a database. A table for that purpose can be created with one of the Django's admin commands. This isn't the most performant caching type, but it can be useful for storing complex database queries.

- **3- File system:** The cache is saved on the file system, in separate files for each cache value. This is the slowest of all the caching types, but it's the easiest to set up in a production environment.

- **4- Local memory:** Local memory cache, which is best-suited for your local development or testing environments. While it's almost as fast as Memcached, it cannot scale beyond a single server, so it's not appropriate to use as a data cache for any app that uses more than one web server.

**BACKEND field in CACHES dictionary means <which caching engine to use.>**

**LOCATION field in CACHES dictionary means <the location of Cache Space. Tells the server where or on which machine it will be storing cache.>**

# 1- Setting Up Cache in Memory:
- This is the most efficient way of caching. 
- we can use memcached which is a memory-based cache framework
- how to use it:
    - Install Memcached framework on your system
    - Install Python connectors for Memcached Framework
    - Edit our Settings.py file
        - CACHES = {
            - 'default': {
                - 'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
                - 'LOCATION': '127.0.0.1:11211',
            - }
        - }

# 2- Setting Up Cache in Database:
- in settings.py add this:
    - CACHES = {
        - 'default': {
            - 'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            - 'LOCATION': 'my_table_name',
        - }
    - }

- now we need to create the cache table 'my_table_name'. so enter it on terminal:
    - python manage.py createcachetable

# 3- Setting Up Cache in File System:
- the File-based Caching means storing caches as individual files.
- we can cache our data on our file system or any directory on the server, it is the most cost-efficient of all as it requires no hardware upgrades at all.
- this caching is slowest of all Cache Spaces. 
- in settings.py add this:
    - CACHES = {
        - 'default': {
            - 'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            - 'LOCATION': '/var/tmp/django_cache',
        - }
    - }
- **important points:**
    - the server should have access to this directory.
    - the directory should exist before running this code.
    - LOCATION should contain the absolute directory path. Django searches from the root of your file-system.

# 4- Setting Up Cache in local-memory:
- it is very powerful and robust.
- this system can handle multi-threaded processes and is efficient.
- it is best for those projects which cannot use Memcached framework.
- add this to settings.py
    - CACHES = {
        - 'default': {
            - 'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            - 'LOCATION': 'DataFlair',
        - }
    - }

# C) Django Caching Levels:

- **1- Per-site cache:** This is the easiest way to implement caching in Django.

- **2- Per-view cache:** Rather than wasting precious memory space on caching static pages or dynamic pages that source data from a rapidly changing API, you can cache specific views.

- **3- Low-level cache API:** If Django's per-site or per-view cache aren't granular enough for your application's needs, then you may want to leverage the low-level cache API to manage caching at the object level.

# 1- Caching the Per-Site:
- The simplest way of using cache in Django is to cache the entire site.
- this is done by editing the MIDDLEWARE_CLASSES option in the project settings.py. 
    - MIDDLEWARE_CLASSES = []
        - 'django.middleware.cache.UpdateCacheMiddleware', # NEW
        - 'django.middleware.common.CommonMiddleware',
        - 'django.middleware.cache.FetchFromCacheMiddleware', # NEW
    - ]
- then add these tow:
    - CACHE_MIDDLEWARE_ALIAS = 'default' –> The cache alias to use for storage.
    - CACHE_MIDDLEWARE_SECONDS = '600' –> The number of seconds each page should be cached.
    - CACHE_MIDDLEWARE_KEY_PREFIX = '' –> should be used if the cache is shared across multiple sites that use the same Django instance

# 2- Caching Per-View
- If you don’t want to cache the entire site you can cache a specific view. This is done by using the cache_page decorator that comes with Django.
- cache_page takes the number of seconds you want the view result to be cached as parameter.
- for example we want to cache the result of the viewArticles view:
    - from django.views.decorators.cache import cache_page
    - @cache_page(60 * 15)
    - def viewArticles(request, year, month):
        - text = "Displaying articles of : %s/%s"%(year, month)
        - return HttpResponse(text)

- As we have seen before the above view was map to:
- Since the URL is taking parameters, each different call will be cached separately. For example, request to /myapp/articles/02/2007 will be cached separately to /myapp/articles/03/2008.
    - urlpatterns = patterns('myapp.views', url(r'^articles/(?P<month>\d{2})/(?P<year>\d{4})/', 'viewArticles', name = 'articles'),)

- Caching a view can also directly be done in the url.py file. Then the following has the same result as the above. Just edit your myapp/url.py file and change the related mapped URL (above) to be. it's no longer needed in myapp/views.py.
    - urlpatterns = patterns('myapp.views', url(r'^articles/(?P<month>\d{2})/(?P<year>\d{4})/', cache_page(60 * 15)('viewArticles'), name = 'articles'),)

# IMP -> Redis vs Memcached:
- **Memcached and Redis** are in-memory, key-value data stores. They are easy to use and optimized for high-performance lookups. You probably won't see much difference in performance or memory usage between the two. 
- **Memcached** is slightly easier to configure since it's designed for simplicity and ease of use.
- **Redis** has a richer set of features so it has a wide range of use cases beyond caching. For example, it's often used to store user sessions or as message broker in a pub/sub system. Because of its flexibility Redis is much better solution.

# 3- Low-level cache API:
- for this caching level we can use Redis.
- you may want to leverage the low-level cache API to manage caching at the object level.
- You may want to use the low-level cache API if you need to cache different:
    - Model objects that change at different intervals
    - Logged-in users' data separate from each other
    - External resources with heavy computing load
    - External API calls
- Django's low-level cache is good when you need more granularity and control over the cache. It can store any object that can be pickled safely.
- To use the low-level cache, you can use either the built-in django.core.cache.caches or, if you just want to use the default cache defined in the settings.py file, via django.core.cache.cache.

**Cache Backend:**
- Download and install Redis.
- after that in a new terminal window start the Redis server (enter this command on terminal -> redis-server) and make sure that it's running on its default port, 6379.
- For Django to use Redis as a cache backend, the django-redis dependency is required. add the custom backend to the settings.py file:
    - CACHES = {
        - 'default': {
            - 'BACKEND': 'django_redis.cache.RedisCache',
            - 'LOCATION': 'redis://127.0.0.1:6379/1',
            - 'OPTIONS': {
                - 'CLIENT_CLASS': 'django_redis.client.- DefaultClient',
            - }
        - }
    - }
- Now, when you run the server again, Redis will be used as the cache backend: **python manage.py runserver**
- Turn to the code. 
    - First, add the import to the top of yorapp/views.py: **from django.core.cache import cache**
    - Then, add the code for caching whatever to the view, for exapmle in a function it's like that:
        - def get(self, request):
            - product_objects = cache.get('product_objects')      # NEW

            - if product_objects is None:                         # NEW
                - product_objects = Product.objects.all()
                - cache.set('product_objects', product_objects)   # NEW
            - context = {
                - 'products': product_objects
            - }
            - return context

