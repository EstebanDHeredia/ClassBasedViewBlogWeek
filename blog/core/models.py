from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="nombre", unique=True)
    active = models.BooleanField(default=True, verbose_name="Activo")
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de modificación")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Tag (models.Model):
    name = models.CharField(max_length=200, verbose_name="nombre", unique=True)
    active = models.BooleanField(default=True, verbose_name="Activo")
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de modificación")

    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

# MODELO DE AUTOR = USUARIOS REGISTRADOS EN LA APP ===> importamos la tabla de usuarios de contrib.models
class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    biography = models.TextField(verbose_name="Biografía")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True, verbose_name="Foto de Perfil")

    def __str__(self):
        return self.user.username 

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ['user']


# MODELO DE POSTS
class Post(models.Model):
    title = models.CharField(max_length=250, verbose_name="Título")
    excerpt = models.TextField(verbose_name="Bajada")
    # content = models.TextField(verbose_name="Contenido")
    content = RichTextField(verbose_name="Contenido")
    image = models.ImageField(
        upload_to="posts", verbose_name="Imagen", null=True, blank=True)
    published = models.BooleanField(default=False, verbose_name="Publicado")
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de modificación")
    # Campos con relaciones con otros modelos
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Categoría", related_name="get_posts")
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, verbose_name="Autor", related_name="get_posts")
    tags = models.ManyToManyField(Tag, verbose_name="Etiquetas")
    likes = models.ManyToManyField(User, related_name="blog_posts", verbose_name="Me gusta")
    dislikes = models.ManyToManyField(User, verbose_name="No me gusta")
    
    def total_likes(self):
        me_gusta = self.likes.count()
        no_me_gusta = self.dislikes.count()
        return me_gusta, no_me_gusta
    
    class Meta:
        verbose_name = "Publicación"
        verbose_name_plural = "Publicaciones"
        ordering = ['title']

    def __str__(self) -> str:
        return self.title

# MODELO ABOUT
class About(models.Model):
    description = models.CharField(max_length=350, verbose_name="Descripción")
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de modificación")

    class Meta:
        verbose_name = "Acerca de"
        verbose_name_plural = "Acerca de nosotros"
        ordering = ['created']

    def __str__(self) -> str:
        return self.description

# MODELO LINK (REDES SOCIALES)
class Link(models.Model):
    key = models.CharField(max_length=100, verbose_name="Key Link")
    name = models.CharField(max_length=120, verbose_name="Red Social")
    url = models.URLField(max_length=350, blank=True,
                          null=True, verbose_name="Enlace")
    icon = models.CharField(max_length=100, blank=True,
                            null=True, verbose_name="Icono")
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de Creación")
    updated = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de modificación")

    class Meta:
        verbose_name = "Red Social"
        verbose_name_plural = "Redes Sociales"
        ordering = ['name']

    def __str__(self) -> str:
        return self.name
