from django.shortcuts import render, reverse

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

def home(request):
    template_name = 'calculator/home.html'
    pages = {
        'Омлет': reverse('omlet'),
        'Паста': reverse('pasta'),
        'Бутер': reverse('buter')
    }

    context = {
        'pages': pages
    }
    return render(request, template_name, context)

def omlet(request):
    servings = int(request.GET.get('servings', 1))
    context = {
      'recipe': {
        'яйца, шт': round(2*servings, 1),
        'молоко, л': round(0.1*servings, 1),
        'соль, ч.л.': round(0.5*servings, 1),
        },
    }
    return render(request, 'calculator/index.html', context)

def pasta(request):
    servings = int(request.GET.get('servings', 1))
    context = {
      'recipe': {
        'макароны, г': round(0.3*servings, 1),
        'сыр, г': round(0.05*servings, 1),
        },
    }
    return render(request, 'calculator/index.html', context)

def buter(request):
    servings = int(request.GET.get('servings', 1))
    context = {
      'recipe': {
        'хлеб, ломтик': round(1*servings, 1),
        'колбаса, ломтик': round(1*servings, 1),
        'сыр, ломтик': round(1*servings, 1),
        'помидор, ломтик': round(1*servings, 1),
        },
    }
    return render(request, 'calculator/index.html', context)