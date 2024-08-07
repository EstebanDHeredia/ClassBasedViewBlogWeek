from django.urls import path
from .views import dates, likeView, disLikeView, PostListView, PostDetailView, CategoryListView, AuthorListView, PostCreateView, PostUpdateView, PostDeleteView, AboutPageView


urlpatterns = [
    # path("", home, name="home"),
    path("", PostListView.as_view(), name="home"),
    path("post/<pk>", PostDetailView.as_view(), name="post"),
    path("category/", CategoryListView.as_view(), name="category"),
    # path('category/<int:category_id>', category, name="category"),
    # path("author/<int:author_id>", author, name="author"),
    path("author/", AuthorListView.as_view(), name="author"),
    path("dates/<int:month>/<int:year>", dates, name="dates"),
    # likes de un post
    path("like/<int:pk>", likeView, name="like_post"),
    # dislikes de un post
    path("dislike/<int:pk>", disLikeView, name="dislike_post"),
    # Crear post:
    path('create/', PostCreateView.as_view(), name='create'),
    # Editar post:
    path('update/<int:pk>', PostUpdateView.as_view(), name='update'),
    # Eliminar un Post
    path('delete/<int:pk>', PostDeleteView.as_view(), name='delete'),
    # About - Acerca de..
    path('about/', AboutPageView.as_view(), name='about'),
]

