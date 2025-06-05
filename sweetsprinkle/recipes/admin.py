from django.contrib import admin
from .models import Category, Recipe, Favorite

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_categories', 'created_by', 'is_approved', 'is_archived', 'created_at']
    list_filter = ['categories', 'is_approved', 'is_archived']
    search_fields = ['name', 'ingredients']
    filter_horizontal = ['categories']
    actions = ['approve_recipes', 'reject_recipes', 'archive_recipes', 'unarchive_recipes']
    
    def get_categories(self, obj):
        return ", ".join([c.name for c in obj.categories.all()])
    get_categories.short_description = 'Categories'

    def approve_recipes(self, request, queryset):
        queryset.update(is_approved=True)
    approve_recipes.short_description = "Approve selected recipes"

    def reject_recipes(self, request, queryset):
        queryset.update(is_approved=False)
    reject_recipes.short_description = "Reject selected recipes"
    
    def archive_recipes(self, request, queryset):
        queryset.update(is_archived=True)
    archive_recipes.short_description = "Archive selected recipes"
    
    def unarchive_recipes(self, request, queryset):
        queryset.update(is_archived=False)
    unarchive_recipes.short_description = "Unarchive selected recipes"

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe', 'added_at']
    list_filter = ['user']