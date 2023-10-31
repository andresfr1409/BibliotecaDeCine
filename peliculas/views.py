from django.shortcuts import render, redirect
import requests
from datetime import datetime 
import locale
from .models import Pelicula
from .forms import PeliculaForm

# Create your views here.
def inicio(request):
  return render(request, 'paginas/inicio.html')

def ayuda(request):
  return render(request, 'paginas/ayuda.html')

def peliculas(request):
  peliculas = Pelicula.objects.all()
  return render(request, 'peliculas/index.html', {'peliculas':peliculas})

def buscar_peliculas(request):
  if request.method == "POST":
    termino_busqueda = request.POST.get("termino_busqueda")
    api_key = "85efd76158e2b80a6a3d456beb14f93c"
    idioma = "es-mx"
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={termino_busqueda}&language={idioma}"
    response = requests.get(url)
    if response.status_code == 200:
      datos = response.json()
      resultados = datos.get("results")
      for resultado in resultados:
        if resultado.get("release_date"):
          fecha_str = resultado["release_date"]
          fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d")
          resultado["release_date"] = fecha_obj.strftime("%d %B %Y")
    else:
      resultados = []
    return render(request, "paginas/buscar_peliculas.html", {"resultados": resultados})
  return render(request, "paginas/buscar_peliculas.html")

def detalles_pelicula(request, pelicula_id):
    api_key = "85efd76158e2b80a6a3d456beb14f93c"
    idioma = "es-mx"
    url = f"https://api.themoviedb.org/3/movie/{pelicula_id}?api_key={api_key}&language={idioma}"
    response = requests.get(url)
    if response.status_code == 200:
        pelicula = response.json()
        return render(request, 'paginas/detalles_pelicula.html', {'pelicula': pelicula})
    else:
        return render(request, 'error.html', {'mensaje': 'La película no se encontró.'})

def agregar(request):
  formulario = PeliculaForm(request.POST or None, request.FILES or None)
  if formulario.is_valid():
    formulario.save()
    return redirect('peliculas')
  return render(request, 'peliculas/agregar.html', {'formulario': formulario})

def editar(request, id):
  pelicula = Pelicula.objects.get(id=id)
  formulario = PeliculaForm(request.POST or None, request.FILES or None, instance=pelicula)
  if formulario.is_valid() and request.POST:
    formulario.save()
    return redirect('peliculas')
  return render(request, 'peliculas/editar.html', {'formulario': formulario})

def eliminar(request, id):
  pelicula = Pelicula.objects.get(id=id)
  pelicula.delete()
  return redirect('peliculas')
