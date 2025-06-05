from django import template
from django.utils.safestring import mark_safe
from recipes.models import Category

register = template.Library()

@register.filter
def dict_item(dictionary, key):
    """
    Get an item from a dictionary by key.
    Used to get category name from ID in templates.
    """
    try:
        key = int(key)
        category = Category.objects.get(id=key)
        return category.name
    except (ValueError, Category.DoesNotExist):
        return '' 