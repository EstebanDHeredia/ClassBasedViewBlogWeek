from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Author
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def home(request):
    # posts = Post.objects.filter(published = True)
    if not request.session.get('items_per_page'): # Cuando el usuario abre la pagina por 1era vez y no hay seleccionado nada en el combo, por defecto pongo la paginacion en 2
        request.session['items_per_page'] = 2
    
    if request.method == 'GET' and 'items_per_page' in request.GET: # Si el metodo del formulario es GET y existe la variable items_per_page en el GET del request, la almaceno en la variable items_per_page de la sesion del usuario
        request.session['items_per_page'] = int(request.GET['items_per_page'])
    
    items_per_page = request.session['items_per_page']

    # posts_page = Paginator(Post.objects.filter(published = True), 2) # 2 es el nro de posts que quiero que entren en cada pagina
    posts_page = Paginator(Post.objects.filter(published = True), items_per_page) # 2 es el nro de posts que quiero que entren en cada pagina
    page = request.GET.get('page') # me devuelve el nro actual de pagina en la que estoy
    posts = posts_page.get_page(page) # pido que me devuelva los posts que están en la pagina actual

    aux = "x" * posts.paginator.num_pages # me va a generar una variable con tantas x como nros de pagina haya,
                                            # esto me va a servir en el template para generar los nros de pagina en el paginador
    
    return render(request, 'core/home.html', {'posts': posts, 'aux': aux})

def post(request, post_id):
    # post = Post.objects.get(id=post_id)
    try:
        post = get_object_or_404(Post, id=post_id)
        likes, dislikes = post.total_likes()
        liked = False      
        disliked = False

        if post.likes.filter(id=request.user.id).exists(): # Averiguo si el usuario logueado le dio like
            liked = True
        if post.dislikes.filter(id=request.user.id).exists(): # Averiguo si el usuario logueado le dio a "no me gusta"
            disliked = True
            
        print("-----------------------------------------------------")
        print(f"Me gusta: {liked}")
        print(f"NO Me gusta: {disliked}")
        print("-----------------------------------------------------")

        return render(request, "core/detail.html", {"post": post,
                                                    "total_likes": likes,
                                                    "total_dislikes": dislikes,
                                                    "liked": liked,
                                                    "disliked": disliked})
    except:
        return render(request, "core/404.html")

# FILTRADO POR CATEGORIA
def category(request, category_id):
    try:
        category = get_object_or_404(Category, id=category_id)
        
        # posts = Post.objects.filter(category=category)
        
        return render(request, "core/category.html", {"category": category})
    except:
        return render (request, "core/404.html")

def author(request, author_id):
    try:
        author = get_object_or_404(Author, id = author_id)
        return render(request, "core/author.html", {"author": author})
    except:
        return render(request, "core/404.html")

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
