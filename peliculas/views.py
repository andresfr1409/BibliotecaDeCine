from django.shortcuts import render, redirect
import requests
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
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={termino_busqueda}"
    response = requests.get(url)
    if response.status_code == 200:
      datos = response.json()
      resultados = datos.get("results")
    else:
      resultados = []
    return render(request, "peliculas/buscar_peliculas.html", {"resultados": resultados})
  return render(request, "peliculas/buscar_peliculas.html")

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
