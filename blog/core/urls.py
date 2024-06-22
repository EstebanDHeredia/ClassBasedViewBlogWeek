from django.urls import path
from .views import home, post, category, author, dates, likeView, disLikeView

urlpatterns = [
    path("", home, name="home"),
    path("post/<int:post_id>", post, name="post"),
    path("category/<int:category_id>", category, name="category"),
    path("author/<int:author_id>", author, name="author"),
    path("dates/<int:month>/<int:year>", dates, name="dates"),
    # likes de un post
    path("like/<int:pk>", likeView, name="like_post"),
    # dislikes de un post
    path("dislike/<int:pk>", disLikeView, name="dislike_post"),

]