from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    ingredients = models.TextField()
    steps = models.TextField()
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='recipes')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def primary_category(self):
        """Return the first category for backward compatibility"""
        return self.categories.first()

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'recipe')