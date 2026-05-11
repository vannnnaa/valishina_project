from django.db import models


class Person(models.Model):
    ROLE_CHOICES = [
        ("me", "Я"),
        ("supervisor", "Научный руководитель"),
        ("manager", "Менеджер программы"),
        ("classmate", "Сокурсник"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    fio = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    photo = models.CharField(max_length=255, blank=True)  # путь к картинке в static

    class Meta:
        verbose_name = "Человек"
        verbose_name_plural = "Люди"

    def __str__(self):
        return f"{self.get_role_display()}: {self.fio}"


class EducationProgram(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name = "Образовательная программа"
        verbose_name_plural = "Образовательные программы"

    def __str__(self):
        return self.name


class Review(models.Model):
    nickname = models.CharField(max_length=80)
    text = models.TextField()
    score = models.PositiveSmallIntegerField()  # 1..10 проверим в форме/валидации
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.nickname} ({self.score}/10)"


class SitePage(models.Model):
    slug = models.SlugField(max_length=80, unique=True)  # адрес страницы: about, contacts...
    title = models.CharField(max_length=200)
    content = models.TextField()  # текст/HTML
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Страница сайта"
        verbose_name_plural = "Страницы сайта"
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} ({self.slug})"

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)  # например: паста, соус, салат
    content = models.TextField()
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ["title"]

    def __str__(self):
        return self.title