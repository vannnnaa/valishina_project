from django.contrib import admin
from .models import Person, EducationProgram, Review, SitePage, Recipe


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("role", "fio", "email", "phone")
    list_filter = ("role",)
    search_fields = ("fio", "email")


@admin.register(EducationProgram)
class EducationProgramAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("nickname", "score", "created_at")
    list_filter = ("score", "created_at")
    search_fields = ("nickname", "text")
    ordering = ("-created_at",)

@admin.register(SitePage)
class SitePageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_published", "updated_at")
    list_filter = ("is_published",)
    search_fields = ("title", "slug", "content")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("title",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_published", "created_at")
    list_filter = ("category", "is_published")
    search_fields = ("title", "content")
    ordering = ("title",)