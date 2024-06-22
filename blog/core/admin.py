from django.contrib import admin
from .models import Category, Post, Tag, About, Link, Author


admin.site.site_header = "Administración del Blog"
admin.site.index_title = 'Panel de Control'
admin.site.site_title = 'Blog'

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    # TODO LO QUE SIGUE FUE GENERADO POR CHATGPT
    list_display = ('get_username', 'get_last_name', 'get_first_name', 'biography')
    
    def get_username(self, obj):
        return obj.user.username
    get_username.admin_order_field = 'user__username'  # Permite ordenar por este campo
    get_username.short_description = 'Nombre de Usuario'
    
    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.admin_order_field = 'user__last_name'
    get_last_name.short_description = 'Apellido'
    
    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.admin_order_field = 'user__first_name'
    get_first_name.short_description = 'Nombre'

class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('name', 'active', 'created')


class TagAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('name', 'active', 'created')


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('title', 'published', 'category', 'author', 'created', 'post_tags')
    ordering = ('author', '-created')
    search_fields = ('title', 'content', 'author__username', 'category__name')
    list_filter = ('author', 'category', 'tags') # AGREGA UNA BARRA LATERAL CON FILTROS AUTOMATICOS

    def post_tags(self, obj):
        return ' - '.join([t.name for t in obj.tags.all().order_by('name')])
    
    post_tags.short_description = "Etiquetas"

# ABOUT
class AboutAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('description','created')
 
# REDES SOCIALES
class LinkAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('name','key', 'url', 'icon')
    
admin.site.register(Link, LinkAdmin)
admin.site.register(About, AboutAdmin)    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Author, AuthorAdmin)
