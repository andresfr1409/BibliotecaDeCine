from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
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
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    duracion = pelicula.get("runtime")
    calificacion = pelicula.get("vote_average")
    presupuesto = pelicula.get("budget")
    ingresos = pelicula.get("revenue")
    estado = pelicula.get("status")
    idioma_original = pelicula.get("original_language")
    paises_produccion = pelicula.get("production_countries")
    if pelicula.get("release_date"):
      fecha_lanzamiento = datetime.strptime(pelicula["release_date"], "%Y-%m-%d")
      pelicula["release_date_year"] = fecha_lanzamiento.year
    if pelicula.get("release_date"):
      fecha_lanzamiento = datetime.strptime(pelicula["release_date"], "%Y-%m-%d")
      pelicula["release_date_formatted"] = fecha_lanzamiento.strftime("%d/%m/%Y")
    if pelicula.get("genres"):
      generos = [genero["name"] for genero in pelicula["genres"]]
      pelicula["generos"] = ",".join(generos)
    if duracion:
      horas = duracion // 60
      minutos = duracion % 60
      pelicula["horas"] = horas
      pelicula["minutos"] = minutos
    if calificacion:
      calificacion_redondeada = round(calificacion,1)
      pelicula["calificacion"] = f"{calificacion_redondeada}"
    if presupuesto:
      pelicula["presupuesto"] = locale.currency(presupuesto, grouping=True)
    if ingresos:
      pelicula["ingresos"] = locale.currency(ingresos, grouping=True)
    else:
      pelicula["ingresos"] = '$0,0'
    if estado:
      if estado == "Released":
        pelicula["estado"] = "Estrenada"
      else:
        pelicula["estado"] = "Sin estrenar"
    if idioma_original:
      if idioma_original == "en":
        pelicula["idioma_original"] = "Inglés"
    if paises_produccion:
      paises = [pais["iso_3166_1"] for pais in paises_produccion]
      pelicula["paises_produccion"] = ", ".join(paises)
    return render(request, 'paginas/detalles_pelicula.html', {'pelicula': pelicula})
  else:
    raise Http404("La película no se encontró.")

def guardar_pelicula(request,pelicula_id):
  api_key = "85efd76158e2b80a6a3d456beb14f93c"
  idioma = "es-mx"
  url = f"https://api.themoviedb.org/3/movie/{pelicula_id}?api_key={api_key}&language={idioma}"
  response = requests.get(url)
  
  if response.status_code == 200:
    pelicula_data = response.json()
    nueva_pelicula = Pelicula(
      titulo = pelicula_data['title'],
      descripcion = pelicula_data['overview']
    )
    if 'poster_path' in pelicula_data:
      nueva_pelicula.imagen_url = f"https://image.tmdb.org/t/p/w500{pelicula_data['poster_path']}"
    nueva_pelicula.save()
    return HttpResponseRedirect(reverse('peliculas'))
  else:
    raise Http404("No se pudo guardar la pelicula.")

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
