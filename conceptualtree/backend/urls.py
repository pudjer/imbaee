from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers

from .views import *

noderouter = routers.DefaultRouter()
noderouter.register('node', NodeViewSet, basename='node')
urlpatterns = [
    # path('', index , name='home' )
    path('', include(noderouter.urls)),
]




if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)