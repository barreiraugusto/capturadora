from django.conf.urls.static import static
from django.urls import path
from .views import CapturaView, ProgramarGrabacion, BorrarGrabacionView, UpdateGrabacionView
from core.capturaweb.tiempo import get_tiempo


urlpatterns = [
    path("", CapturaView.as_view(), name="capturaweb"),
    path("programar/", ProgramarGrabacion.as_view(), name="programar"),
    path("borrar/<pk>/", BorrarGrabacionView.as_view(), name="borrar"),
    path("editar/<pk>/", UpdateGrabacionView.as_view(), name="editar"),
    path("get_tiempo", get_tiempo, name="get_tiempo"),
]
#if settings.DEBUG:
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
