from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg, Count
from django.utils import timezone
from .models import Person, EducationProgram, Review, SitePage, Recipe

def index(request):
    return render(request, "Valishina_response/index.html")

def page1(request):
    return render(request, "Valishina_response/page1.html")

def gdp_filter(request):
    if request.method != "POST":
        return render(request, "Valishina_response/gdp.html", {"result": [], "error": ""})

    countries = request.POST.get("countries", "").split()
    gdps_text = request.POST.get("gdps", "").split()
    threshold_text = request.POST.get("threshold", "").strip()

    try:
        gdps = [float(x) for x in gdps_text]
        threshold = float(threshold_text)
    except:
        return render(request, "Valishina_response/gdp.html", {"result": [], "error": "Проверь числа."})

    if len(countries) != len(gdps):
        return render(request, "Valishina_response/gdp.html", {"result": [], "error": "Число стран и чисел не совпадает."})

    result = [countries[i] for i in range(len(countries)) if gdps[i] >= threshold]
    return render(request, "Valishina_response/gdp.html", {"result": result, "error": ""})
    

def program_page(request):
    program = EducationProgram.objects.first()

    me = Person.objects.filter(role="me").first()
    supervisor = Person.objects.filter(role="supervisor").first()
    manager = Person.objects.filter(role="manager").first()
    classmates = Person.objects.filter(role="classmate").order_by("fio")

    # отзывы (пока просто показываем)
    reviews = Review.objects.all().order_by("-created_at")

    # агрегированная статистика по оценкам (пункт 5 в будущем)
    stats = reviews.aggregate(avg_score=Avg("score"), count=Count("id"))

    return render(
        request,
        "Valishina_response/program.html",
        {
            "program": program,
            "me": me,
            "supervisor": supervisor,
            "manager": manager,
            "classmates": classmates,
            "reviews": reviews,
            "stats": stats,
        },
    )

def add_review(request):
    if request.method == "GET":
        return render(request, "Valishina_response/add_review.html", {"error": ""})

    nickname = request.POST.get("nickname", "").strip()
    text = request.POST.get("text", "").strip()
    score_text = request.POST.get("score", "").strip()

    if not nickname or not text or not score_text:
        return render(request, "Valishina_response/add_review.html", {"error": "Заполни все поля."})

    try:
        score = int(score_text)
    except:
        return render(request, "Valishina_response/add_review.html", {"error": "Оценка должна быть числом."})

    if score < 1 or score > 10:
        return render(request, "Valishina_response/add_review.html", {"error": "Оценка должна быть от 1 до 10."})

    Review.objects.create(nickname=nickname, text=text, score=score)
    return redirect("Valishina_response:program")

def reviews_list(request):
    qs = Review.objects.all()

    # фильтр
    min_score_text = request.GET.get("min_score", "").strip()
    if min_score_text:
        try:
            min_score = int(min_score_text)
            qs = qs.filter(score__gte=min_score)
        except:
            min_score = None
    else:
        min_score = None

    # сортировка
    sort = request.GET.get("sort", "new")  # new / old / score_desc / score_asc
    if sort == "old":
        qs = qs.order_by("created_at")
    elif sort == "score_desc":
        qs = qs.order_by("-score", "-created_at")
    elif sort == "score_asc":
        qs = qs.order_by("score", "-created_at")
    else:
        qs = qs.order_by("-created_at")

    stats = qs.aggregate(avg_score=Avg("score"), count=Count("id"))

    by_score = (
    qs.values("score")
      .annotate(cnt=Count("id"))
      .order_by("-score")
    )

    return render(
        request,
        "Valishina_response/reviews_list.html",
        {"reviews": qs, "stats": stats, "by_score": by_score, "min_score": min_score_text, "sort": sort},
    )


def site_page(request, slug):
    page = get_object_or_404(SitePage, slug=slug, is_published=True)
    return render(request, "Valishina_response/site_page.html", {"page": page})


def site_index(request):
    qs = SitePage.objects.all()

    # фильтр опубликованных
    only_published = request.GET.get("published", "1")
    if only_published == "1":
        qs = qs.filter(is_published=True)

    # поиск по названию
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(title__icontains=q)

    # сортировка
    sort = request.GET.get("sort", "title")  # title / updated_desc / updated_asc
    if sort == "updated_desc":
        qs = qs.order_by("-updated_at")
    elif sort == "updated_asc":
        qs = qs.order_by("updated_at")
    else:
        qs = qs.order_by("title")

    return render(
        request,
        "Valishina_response/site_index.html",
        {"pages": qs, "q": q, "sort": sort, "published": only_published},
    )

def recipes_list(request):
    qs = Recipe.objects.all()

    # фильтр: опубликованные
    only_published = request.GET.get("published", "1")
    if only_published == "1":
        qs = qs.filter(is_published=True)

    # фильтр: категория
    category = request.GET.get("category", "").strip()
    if category:
        qs = qs.filter(category__icontains=category)

    # сортировка
    sort = request.GET.get("sort", "title")  # title / new / old
    if sort == "new":
        qs = qs.order_by("-created_at")
    elif sort == "old":
        qs = qs.order_by("created_at")
    else:
        qs = qs.order_by("title")

    return render(request, "Valishina_response/recipes_list.html", {
        "recipes": qs, "category": category, "sort": sort, "published": only_published
    })