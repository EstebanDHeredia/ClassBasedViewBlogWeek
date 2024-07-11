from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Author
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView # Importo la clase genérica que me permite hacer una vista de listado
from django.views.generic.detail import DetailView  # Importo la clase genérica que me va a permitir mostrar un post en particular
from django.views.generic.edit import CreateView # Importo la clase que me permite crear un Post
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.base import TemplateView #Esta vista basada en clase solo me renderiza un template, lo voy a utilizar para que me renderice la pagina aboutme
from .forms import PostForm

# Create your views here.
class PostListView(ListView):
    
    model = Post # Me va a listar los objetos de este modelo
    paginate_by = 2 # Me incluye la paginación!!! acá le indico la cant de objetos en cada página
    template_name = "core/home.html" # Le especifico el nombre del template al que debe retornar los datos, 
                                    # ya que sino por defecto me busca el template post_list.html (lo general a partir del model que yo le indiqué) 
                                    # Es decir, o defino este atributo, o cambio el nombre del template a "post_list.html"
    context_object_name = "posts"   # Indico el nombre de la variable de contexto que va a utilizar el template,
                                    # sino en el template tendría que usar la variable de contexto que por defecto 
                                    # me devuelve la clase que es: "object_list"
    
    def get_queryset(self): # Agrego esta función si quiero que el listado de post que me devuelva cumpla
                            # alguna condición, sino me devuelve todos los post
        return Post.objects.filter(published=True)

class PostDetailView(DetailView):
    
    model = Post
    template_name = "core/detail.html"
    
    # Con esta función le agrego variables de contexto al template!!!
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        likes, dislikes = self.object.total_likes()    
        liked = False      
        disliked = False

        if self.object.likes.filter(id=self.request.user.id).exists(): # Averiguo si el usuario logueado le dio like
            liked = True
        if self.object.dislikes.filter(id=self.request.user.id).exists(): # Averiguo si el usuario logueado le dio a "no me gusta"
            disliked = True     
                
        context["liked"] = liked
        context["disliked"] = disliked      
        context["total_likes"] = likes
        context["total_dislikes"] = dislikes     
        
        return context

# FILTRADO DE POSTS POR CATEGORÍA
class CategoryListView(ListView):
    
    model = Category
    template_name = "core/category.html"
    context_object_name = "category"

    def get_queryset(self):
        category_id = self.request.GET['cat'] # Obtengo el id de categoria, recortando lo que está después de 'cat' en la url
        if category_id:
            return Category.objects.filter(id=category_id).first() # Me devuelve un objeto (el primero, 
                                            # aunque siempre debería haber uno solo) de tipo Categoria
        return super().get_queryset()


def custom_404_view(request, exception):
    print(exception)
    return render(request, 'core/404.html', context={'error': exception}, status=404)

# FILTRADO POR AUTOR
class AuthorListView(ListView):
    
    model = User
    context_object_name = "author"
    template_name = "core/author.html"
    allow_empty = False

    def get_queryset(self):
        author_id = self.request.GET['aut']
        if author_id:
            author = get_object_or_404(Author, user=author_id)
            # author = Author.objects.filter(user=author_id).first()
            return author
                
        return super().get_queryset()


# Crear un Post
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm   # Le indico que tiene que utilizar el formulario que creé en forms.py, el cual
                            # contiene los campos del Post. Esto no quiere decir que yo pueda acceder solo
                            # a los campos que me muestra el formulario. Como yo indico en model que el modelo
                            # que voy a utilizar es el de Post, puedo acceder a todos los otros campos,
                            # de hecho en la funcion form_valid, le indico qué valor debe tomar el campo author
    
    def form_valid(self, form):
        author = Author.objects.get(user=self.request.user) # Busco en tabla autores el autor que está logueado
        form.instance.author = author # Le indico que el author del Post va a ser el usuario que está logueado
        return super().form_valid(form)
    
    success_url = reverse_lazy('home') # Le indico a dónde debe volver si el post se creo correctamente


# Actualizar un Post
class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name_suffix = "_update_form"   # el template que va a buscar para renderizar el formulario
                                            # va a set post_update_form.html
    
    # Establezco la url a la que tiene que redirigirse una vez actualizado el post
    # En este caso lo vuelvo a la misma página de update del post que acabo de actualizar
    # y para que se observe que el post se modificó correctamente, lo voy a mostrar con
    # un cartel en el template, si la palabra 'ok' está en la url                   
    def get_success_url(self) -> str:
        return reverse_lazy('update', args=[self.object.id] ) + '?ok'
    
# Eliminar un Post
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('home')
    
# Acerca de...
class AboutPageView(TemplateView):
    template_name = "core/about.html"
    

def dates(request, month, year):
    try:
        posts = Post.objects.filter(published = True, created__month = month, created__year =year)
        date = datetime.date(year, month, 1)
        return render(request, "core/dates.html", {'posts': posts,
                                                   'date': date})
    except:
        return render(request, "core/404.html")

def likeView(request, pk):
    try:
        post = get_object_or_404(Post, id=pk) # Busco el post con el pk de acuerdo a lo que recibo del formulario
        
        if post.dislikes.filter(id=request.user.id).exists() : # Pregunto si el usuario logueado le dio dislike al post
            post.dislikes.remove(request.user.id) # Si es así lo elimino, porque le dio al botón "me gusta"
 
        post.likes.add(request.user.id) # Con el metodo add agrego al usuario logueado a la lista de many to many del campo likes del post

        return HttpResponseRedirect(reverse('post', args=[post.id])) # Vuelvo a la pagina del detalle del post con utlizando reverse para obtner la url del mismo y agregando el paramentro del id del post
    except:
        return HttpResponseRedirect(reverse('post', args=[post.id]))

def disLikeView(request, pk):
    try:
        post = get_object_or_404(Post, id=pk) # Busco el post con el pk de acuerdo a lo que recibo del formulario
        
        if post.likes.filter(id=request.user.id).exists() : # Pregunto si el usuario logueado ya le dio like al post
            post.likes.remove(request.user.id) # Si es así lo elimino, porque le dio al botón "no me gusta"
        
        post.dislikes.add(request.user.id) # Con el metodo add agrego al usuario logueado a la lista de many to many del campo dislikes del post

        return HttpResponseRedirect(reverse('post', args=[post.id])) # Vuelvo a la pagina del detalle del post con utlizando reverse para obtner la url del mismo y agregando el paramentro del id del post
    except:
        return HttpResponseRedirect(reverse('post', args=[post.id]))



# def home(request):
#     # posts = Post.objects.filter(published = True)
#     if not request.session.get('items_per_page'): # Cuando el usuario abre la pagina por 1era vez y no hay seleccionado nada en el combo, por defecto pongo la paginacion en 2
#         request.session['items_per_page'] = 2
    
#     if request.method == 'GET' and 'items_per_page' in request.GET: # Si el metodo del formulario es GET y existe la variable items_per_page en el GET del request, la almaceno en la variable items_per_page de la sesion del usuario
#         request.session['items_per_page'] = int(request.GET['items_per_page'])
    
#     items_per_page = request.session['items_per_page']

#     # posts_page = Paginator(Post.objects.filter(published = True), 2) # 2 es el nro de posts que quiero que entren en cada pagina
#     posts_page = Paginator(Post.objects.filter(published = True), items_per_page) # 2 es el nro de posts que quiero que entren en cada pagina
#     page = request.GET.get('page') # me devuelve el nro actual de pagina en la que estoy
#     posts = posts_page.get_page(page) # pido que me devuelva los posts que están en la pagina actual

#     aux = "x" * posts.paginator.num_pages # me va a generar una variable con tantas x como nros de pagina haya,
#                                             # esto me va a servir en el template para generar los nros de pagina en el paginador
    
#     return render(request, 'core/home.html', {'posts': posts, 'aux': aux})

# def post(request, post_id):
#     # post = Post.objects.get(id=post_id)
#     try:
#         post = get_object_or_404(Post, id=post_id)
#         likes, dislikes = post.total_likes()
#         liked = False      
#         disliked = False

#         if post.likes.filter(id=request.user.id).exists(): # Averiguo si el usuario logueado le dio like
#             liked = True
#         if post.dislikes.filter(id=request.user.id).exists(): # Averiguo si el usuario logueado le dio a "no me gusta"
#             disliked = True
            
#         print("-----------------------------------------------------")
#         print(f"Me gusta: {liked}")
#         print(f"NO Me gusta: {disliked}")
#         print("-----------------------------------------------------")

#         return render(request, "core/detail.html", {"post": post,
#                                                     "total_likes": likes,
#                                                     "total_dislikes": dislikes,
#                                                     "liked": liked,
#                                                     "disliked": disliked})
#     except:
#         return render(request, "core/404.html")

# # FILTRADO POR CATEGORIA
# def category(request, category_id):
#     try:
#         category = get_object_or_404(Category, id=category_id)
        
#         # posts = Post.objects.filter(category=category)

#         return render(request, "core/category.html", {"category": category})
#     except:
#         return render (request, "core/404.html")

# def author(request, author_id):
#     try:
#         author = get_object_or_404(Author, id = author_id)
#         return render(request, "core/author.html", {"author": author})
#     except:
#         return render(request, "core/404.html")


