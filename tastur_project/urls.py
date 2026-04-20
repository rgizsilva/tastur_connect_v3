from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views
from analise import urls as analise_urls  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('clientes/', include('clientes.urls')),
    path('parceiros/', include('parceiros.urls')),
    path('reservas/', include('reservas.urls')),
    path('select2/', include('django_select2.urls')),
    path('reserva/<int:reserva_id>/pdf/', views.gerar_pdf_reserva, name='gerar_pdf_reserva'),
    path('api/analise/', include(('analise.urls', 'analise'), namespace='analise')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
