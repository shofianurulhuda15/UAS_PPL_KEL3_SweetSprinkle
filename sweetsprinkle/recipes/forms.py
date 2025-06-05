from django import forms
from .models import Recipe, Category

class RecipeForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-checkbox h-5 w-5 text-pink-500 rounded focus:ring-pink-400'
        }),
        help_text='Select one or more categories for your recipe'
    )
    
    class Meta:
        model = Recipe
        fields = ['name', 'ingredients', 'steps', 'image', 'categories']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400 transition-colors',
                'placeholder': 'Enter recipe name'
            }),
            'ingredients': forms.Textarea(attrs={
                'rows': 4, 
                'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400 transition-colors',
                'placeholder': 'Enter ingredients, one per line'
            }),
            'steps': forms.Textarea(attrs={
                'rows': 6, 
                'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400 transition-colors',
                'placeholder': 'Enter preparation steps'
            }),
            'image': forms.FileInput(attrs={
                'class': 'hidden',
                'id': 'recipe-image',
                'accept': 'image/*'
            }),
        }
        labels = {
            'name': 'Recipe Name',
            'ingredients': 'Ingredients',
            'steps': 'Preparation Steps',
            'image': 'Recipe Photo',
            'categories': 'Categories'
        }
        help_texts = {
            'ingredients': 'List all ingredients with quantities',
            'steps': 'Explain the preparation process step by step',
            'image': 'Upload a photo of your recipe (recommended size: 800x600 pixels)'
        }