from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path( 'admin/', admin.site.urls ),
    path( '', include('core.urls') ),
]

if settings.DEBUG:
    from django.conf.urls import url
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns