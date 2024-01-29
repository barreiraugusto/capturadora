from django.conf.urls.static import static
from django.urls import path
from .views import CapturaView
from core.capturaweb.tiempo import get_tiempo


urlpatterns = [
    path("", CapturaView.as_view(), name="capturaweb"),
    path("get_tiempo", get_tiempo, name="get_tiempo"),
]
#if settings.DEBUG:
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
