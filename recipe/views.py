from django.shortcuts import render, get_list_or_404
from recipe.models import Category, Recipe, About, Article
from .forms import SearchForm
from .search_logic import handle_search


def index(request):
    if request.method == "GET" and "search" in request.GET:
        # Здесь мы предполагаем, что поиск выполняется через GET-запрос с каким-то параметром, например 'search'
        search_result = handle_search(request)  # Вызов функции обработки поиска
        # Передаём результат поиска в контекст шаблона
        context = {"search_result": search_result}
    else:
        context = {}
    return render(request, "index.html", context)


# def index(request, handle_search):
#     index_data = {"title": "Пошук рецептів", "body": handle_search}
#     return render(request, "index.html", {"index_data": index_data})


def recipe(request, recipe_id):
    resipe_single = Recipe.objects.get(pk=recipe_id)
    ingredients_data = resipe_single.recipeingredient_set.all()
    ingredients_list = [
        f"{ri.ingredient.name} - {ri.unit if ri.unit else ''} можна замінити на{ri.substitutes if ri.substitutes else '' }"
        for ri in ingredients_data
    ]
    category_name = [category.title for category in resipe_single.category.all()]

    recipe_data = {
        "title": "Пошук рецептів",
        "title_content": resipe_single.title,
        "title_image": resipe_single.title_image,
        "ingredient": ingredients_list,
        "body_image": resipe_single.body_image,
        "preparation": resipe_single.preparation,
        "categories": category_name,
        "reviews": resipe_single.reviews,
    }
    return render(request, "recipe.html", {"recipe_data": recipe_data})


def about(request):
    about_data = {
        "title": "Про що сайт",
        "title_content": "Як тут все працюе",
        "body": "Пока нет ничего",
    }

    return render(request, "about.html", {"about_data": about_data})


def blog(request):
    articles_list = Article.objects.values("title")
    blog_data = {
        "title": "Блог",
        "title_content": "Статті про корисне харчування",
        "body": articles_list,
    }
    return render(request, "blog.html", {"blog_data": blog_data})


def article(request, article_id):
    try:
        article_single = Article.objects.get(pk=article_id)
        article_data = {
            "title": "Стаття",
            "title_content": article_single.title,
            "body": article_single,
        }
    except Article.DoesNotExist:
        return render(
            request, "article.html", {"message": "Якась помилка, спробуйте ще раз"}
        )
    return render(request, "article.html", {"article_data": article_data})
