from django.conf.urls.static import static
from django.urls import path
from .views import CapturaView


urlpatterns = [
    path("", CapturaView.as_view(), name="capturaweb"),
]
#if settings.DEBUG:
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
