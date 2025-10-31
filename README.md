Overview
This project implements a Django-based property listing application with Redis caching at multiple levels. The system demonstrates various caching strategies including view-level caching, low-level queryset caching, and proper cache invalidation techniques. The application uses Docker to containerize PostgreSQL for data persistence and Redis for caching, providing a realistic development environment that mirrors production setups.

Learning Objectives
Implement multi-level caching strategies in Django applications
Configure and integrate Redis as a cache backend
Set up containerized services (PostgreSQL and Redis) using Docker
Understand cache invalidation techniques using Django signals
Analyze cache performance metrics
Develop efficient database query patterns with caching
Structure Django projects for maintainability and scalability
Key Concepts
Multi-level Caching: Implementing both view-level and low-level caching
Cache Invalidation: Using Django signals to maintain cache consistency
Containerization: Managing dependencies with Docker containers
Cache Metrics: Monitoring and analyzing Redis cache performance
Database Optimization: Reducing database load through intelligent caching
Tools and Libraries
Django: Web framework for building the property listing application
PostgreSQL: Relational database for persistent storage
Redis: In-memory data store used for caching
Docker: Containerization platform for service management
django-redis: Django cache backend for Redis integration
psycopg2: PostgreSQL adapter for Python
Python’s logging: For tracking cache metrics and performance
Real-World Use Case
This project models a real estate listing platform where: 1. Property listings are frequently accessed but rarely modified 2. Database load needs to be minimized during peak traffic 3. Data consistency must be maintained despite caching 4. Performance metrics are monitored to optimize cache effectiveness

Such caching implementations are crucial for: - High-traffic listing platforms (real estate, e-commerce) - Applications with expensive database queries - Systems requiring sub-second response times - Platforms needing to scale efficiently under load

The techniques demonstrated provide a blueprint for building performant web applications while maintaining data consistency and reducing infrastructure costs.

0. Set Up Django Project with Dockerized PostgreSQL and Redis
mandatory
Objective
Initialize a Django project for the property listing app, configure PostgreSQL and Redis in Docker, and set up the cache backend.

Instructions
1. Create the Django Project:

Initialize a Django project named alx-backend-caching_property_listings.
Create a Django app named properties inside the project.
Create a Property model in properties/models.py with fields:
title (CharField, max_length=200)
description (TextField)
price (DecimalField, maxdigits=10, decimalplaces=2)
location (CharField, max_length=100)
created_at (DateTimeField, autonowadd=True)
Run migrations to create the database schema.
Set Up Dockerized PostgreSQL and Redis:
Create a docker-compose.yml file in the project root to define two services:
PostgreSQL: Use the official postgres:latest image, expose port 5432, and set environment variables for database configuration.
Redis: Use the official redis:latest image, expose port 6379.
Ensure both services are accessible from the Django app (e.g., PostgreSQL via postgres:5432, Redis viaredis:6379).
3. Configure Django Settings:

Install required Python packages: django, django-redis, psycopg2-binary.
Add django-redis to INSTALLED_APPS in alx-backend-caching_property_listings/settings.py.
Configure the database to use PostgreSQL in alx-backend-caching_property_listings/settings.py
Configure Redis as the cache backend in alx-backend-caching_property_listings/settings.py
Repo:

GitHub repository: alx-backend-caching_property_listings
File: alx-backend-caching_property_listings/settings.py, docker-compose.yaml, properties/models.py,

1. Cache Property List View
mandatory
Objective
Cache the property list view’s response in Redis for 15 minutes.

Instructions
Create a property_list view in properties/views.py to return all properties.
Apply @cache_page(60 * 15)to cache the response in Redis.
Map the view to /properties/ via URL configuration.
Repo:

GitHub repository: alx-backend-caching_property_listings
File: properties/views.py, properties/urls.py, alx_backend_caching_property_listings/urls.py

 Low-Level Caching for Property Queryset
mandatory
Objective
Cache the Property queryset in Redis for 1 hour using Django’s low-level cache API.

Instructions
Create properties/utils.py with a getallproperties() function that:
Checks Redis for all_properties using cache.get('all_properties').
FetchesProperty.objects.all() if not found.
Stores the queryset in Redis with cache.set('all_properties', queryset, 3600).
Returns the queryset.
Update property_list to useget_all_properties().
Repo:

GitHub repository: alx-backend-caching_property_listings
File: properties/utils.py, properties/views.py

3. Cache Invalidation Using Signals
mandatory
Objective
Invalidate the all_properties Redis cache on Property create/update/delete using Django signals.

Instructions
Create properties/signals.py with post_save and post_delete signal handlers that call cache.delete('all_properties').
In properties/apps.py, override ready() to import signals.py.
Update properties/__init__.py for the app config.
Repo:

GitHub repository: alx-backend-caching_property_listings
File: properties/signals.py, properties/apps.py, properties/__init__.py

4. Cache Metrics Analysis
mandatory
Objective
Retrieve and analyze Redis cache hit/miss metrics.

Instructions
1.In properties/utils.py, add get_redis_cache_metrics() to:

Connect to Redis via django_redis.
Get keyspace_hits and keyspace_misses from INFO.
Calculate hit ratio (hits / (hits + misses)).
Log metrics and return a dictionary.
Repo:

GitHub repository: alx-backend-caching_property_listings
File: properties/utils.py