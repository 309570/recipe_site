from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:recipe_id>", views.recipe, name="recipe"),
    path("about", views.about, name="about"),
    path("blog", views.blog, name="blog"),
    path("blog/<int:article_id>", views.article, name="article")
]