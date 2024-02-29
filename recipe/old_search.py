from recipe.models import Category, Recipe, Ingredient
from recipe.forms import SearchForm
from django.db.models import Q, Count
from .forms import get_frequent_ingredients_names


def get_check_ingredients(form):
    """Функция для получения проверки суммарного количеества ингредиентов."""
    input_ingredient = form.cleaned_data.get("ingredient", [])
    frequent_ingredients_selected = form.cleaned_data.get("frequent_ingredients", [])
    all_ingredients = list(input_ingredient) + list(frequent_ingredients_selected)
    print(all_ingredients)  # check
    if len(all_ingredients) <= 4:
        return Q(ingredient__in=all_ingredients) if all_ingredients else None, None

    else:
        return None, "Будь ласка, виберіть не більше 4х інгредієнтів."


def get_selected_categories(form):
    """Функция для получения и проверки правильного выбора категории."""
    selected_categories = form.cleaned_data.get("category")
    if selected_categories and selected_categories.count() == 1:
        print(selected_categories, " и также ", len(selected_categories))  # check
        return Q(category=selected_categories.first()), None
    elif selected_categories and selected_categories.count() > 1:
        return None, "Будь ласка, виберіть лише одну категорію."
    return None, None


def handle_search(request):
    form = SearchForm(request.GET)
    errors = []
    recipes = None

    if form.is_valid():
        title_recipe = form.cleaned_data.get("title")
        if title_recipe:
            recipes = Recipe.objects.filter(title__icontains=title_recipe.lower())

        else:
            category_filter, category_filter_error = get_selected_categories(form)
            ingredient_filter, ingredient_filter_error = get_check_ingredients(form)
            print(
                "Categori is: ", category_filter, "Ingedients are: ", ingredient_filter
            )
            filters = Q()
            print(filter_query)

            filter_query = [get_check_ingredients, get_selected_categories]
            if filter_query:
                for query in filter_query:
                    filter_result, filter_error = query(form)
                    if filter_result:
                        filters &= filter_result
                    if filter_error:
                        errors.append(filter_error)
                        
            else:
                if category_filter:
                    filters &= category_filter
                if category_filter_error:
                    errors.append(category_filter_error)
                    # print(Recipe.objects.filter(filters).query)

                if not errors:
                    print("Filters before applying:", filters)  # check

                    recipes = Recipe.objects.filter(filters).distinct()
                else:
                    recipes = Recipe.objects.none()
                print("Final queryset:", recipes.query)  # check
    return {
        "form": form,
        "recipes": recipes,
        "categories": Category.objects.all(),
        "frequent_ingredients": get_frequent_ingredients_names(),
    }




from recipe.models import Category, Recipe, Ingredient
from recipe.forms import SearchForm
from django.db.models import Q, Count
from .forms import get_frequent_ingredients_names


def get_check_ingredients(form):
    """Функция для получения проверки суммарного количеества ингредиентов."""
    input_ingredient = form.cleaned_data.get("ingredient", [])
    frequent_ingredients_selected = form.cleaned_data.get("frequent_ingredients", [])
    summ_ingredients = len(input_ingredient) + len(frequent_ingredients_selected)
    all_ingredients = list(input_ingredient) + list(frequent_ingredients_selected)

    if summ_ingredients <= 4:
        return Q(ingredient__in=all_ingredients) if all_ingredients else None, None

    else:
        return None, "Будь ласка, виберіть не більше 4х інгредієнтів."


def get_selected_categories(form):
    """Функция для получения и проверки правильного выбора категории."""
    selected_categories = form.cleaned_data.get("category")
    if selected_categories and selected_categories.count() == 1:
        return Q(category=selected_categories.first()), None
    elif selected_categories and selected_categories.count() > 1:
        return None, "Будь ласка, виберіть лише одну категорію."
    return None, None


def handle_search(request):
    form = SearchForm(request.GET)
    errors = []
    recipes = None

    if form.is_valid():
        title_recipe = form.cleaned_data.get("title")
        if title_recipe:
            recipes = Recipe.objects.filter(title__icontains=title_recipe.lower())

        else:
            filters = Q()
            ingredient_filters_applied = False

            ingredient_filter, ingredient_filter_error = get_check_ingredients(form)
            if ingredient_filter_error:
                errors.append(ingredient_filter_error)
            if ingredient_filter:
                filters &= ingredient_filter
                ingredient_filters_applied = True

                if not ingredient_filters_applied:
                    category_filter, category_filter_error = get_selected_categories(
                        form
                    )
                    if category_filter_error:
                        errors.append(category_filter_error)
                    if category_filter:
                        filters &= category_filter
                    # print(Recipe.objects.filter(filters).query)

            if not errors:
                print("Filters before applying:", filters)

                if filters:
                    recipes = Recipe.objects.filter(filters).distinct()
                else:
                    recipes = Recipe.objects.none()

    return {
        "form": form,
        "recipes": recipes,
        "categories": Category.objects.all(),
        "frequent_ingredients": get_frequent_ingredients_names(),
    }
