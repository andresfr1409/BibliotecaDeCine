from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
  path('', views.inicio, name='inicio'),
  path('ayuda', views.ayuda, name='ayuda'),
  path('peliculas', views.peliculas, name='peliculas'),
  path('peliculas/agregar', views.agregar, name='agregar'),
  path('peliculas/editar/<int:id>', views.editar, name='editar'),
  path('eliminar/<int:id>', views.eliminar, name='eliminar'),
  path('buscar', views.buscar_peliculas, name='buscar_peliculas'),
  path('buscar/detalles/<int:pelicula_id>', views.detalles_pelicula, name='detalles_pelicula'),
  path('guardar_pelicula/<int:pelicula_id>', views.guardar_pelicula, name='guardar_pelicula')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)