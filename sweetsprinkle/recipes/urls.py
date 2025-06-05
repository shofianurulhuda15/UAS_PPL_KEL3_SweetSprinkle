from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipe/<int:recipe_id>/', views.detail, name='detail'),
    path('add/', views.add_recipe, name='add_recipe'),
    path('recipe/<int:recipe_id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipe/<int:recipe_id>/delete/', views.delete_recipe, name='delete_recipe'),
    path('my-recipes/', views.my_recipes, name='my_recipes'),
    path('favorites/', views.favorites, name='favorites'),
    path('recipe/<int:recipe_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('manage/', views.manage_recipes, name='manage_recipes'),
]