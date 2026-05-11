from django.urls import path
from . import views

app_name = "Valishina_response"

urlpatterns = [
    path("", views.index, name="index"),
    path("page1/", views.page1, name="page1"),
    path("gdp/", views.gdp_filter, name="gdp"),
    path("program/", views.program_page, name="program"),
    path("reviews/add/", views.add_review, name="add_review"),
    path("reviews/", views.reviews_list, name="reviews_list"),
    path("site/", views.site_index, name="site_index"),
    path("site/<slug:slug>/", views.site_page, name="site_page"),
    path("recipes/", views.recipes_list, name="recipes_list"),
    path("recipes/<int:recipe_id>/", views.recipe_detail, name="recipe_detail"),
]