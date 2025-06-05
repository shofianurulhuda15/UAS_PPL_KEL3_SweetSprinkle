from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q, Count
from .models import Recipe, Category, Favorite
from .forms import RecipeForm
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.http import Http404

def home(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    query = request.GET.get('q')
    sort = request.GET.get('sort', 'newest')  # Default sort by newest
    
    # Base queryset - only approved and non-archived recipes
    recipes = Recipe.objects.filter(is_approved=True, is_archived=False)
    
    # Apply search filter if query exists
    if query:
        recipes = recipes.filter(
            Q(name__icontains=query) | 
            Q(ingredients__icontains=query) |
            Q(categories_name_icontains=query)
        ).distinct()
    
    # Apply category filter if selected
    if selected_category:
        recipes = recipes.filter(categories__id=selected_category)
    
    # Apply sorting
    if sort == 'oldest':
        recipes = recipes.order_by('created_at')
    elif sort == 'a-z':
        recipes = recipes.order_by('name')
    elif sort == 'z-a':
        recipes = recipes.order_by('-name')
    else:  # newest (default)
        recipes = recipes.order_by('-created_at')
    
    # Get popular recipes (non-archived only)
    popular_recipes = Recipe.objects.filter(is_approved=True, is_archived=False).annotate(
        favorite_count=Count('favorite')
    ).order_by('-favorite_count')[:3]
    
    context = {
        'recipes': recipes,
        'categories': categories,
        'popular_recipes': popular_recipes,
        'selected_category': selected_category,
        'query': query,
        'sort': sort
    }
    
    return render(request, 'recipes/home.html', context)

def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # If recipe is archived and user is not the owner or admin, return 404
    if recipe.is_archived and not (request.user.is_authenticated and (request.user == recipe.created_by or request.user.is_superuser)):
        raise Http404("Recipe not found")
    
    # If recipe is not approved and user is not the owner or admin, return 404
    if not recipe.is_approved and not (request.user.is_authenticated and (request.user == recipe.created_by or request.user.is_superuser)):
        raise Http404("Recipe not found")
    
    is_favorite = Favorite.objects.filter(user=request.user, recipe=recipe).exists() if request.user.is_authenticated else False
    return render(request, 'recipes/detail.html', {'recipe': recipe, 'is_favorite': is_favorite})

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.created_by = request.user
            # Auto-approve recipes for admin users
            if request.user.is_superuser:
                recipe.is_approved = True
            recipe.save()
            
            # Save the many-to-many relationships
            form.save_m2m()
            
            if recipe.is_approved:
                message = "Your recipe has been added successfully!"
            else:
                message = "Your recipe has been submitted and is awaiting approval."
            messages.success(request, message)
            return redirect('home')
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})

@login_required
def favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('recipe')
    return render(request, 'recipes/favorites.html', {'favorites': favorites})

@login_required
def toggle_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, is_approved=True)
    favorite, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    if not created:
        favorite.delete()
    return redirect('detail', recipe_id=recipe_id)

@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Check if the user is the owner of the recipe or an admin
    if recipe.created_by != request.user and not request.user.is_superuser:
        messages.error(request, "You don't have permission to edit this recipe.")
        return HttpResponseForbidden("You don't have permission to edit this recipe.")
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            
            # Handle image removal if requested
            if request.POST.get('remove_image') == 'true':
                # Delete the old image file
                if recipe.image:
                    recipe.image.delete(save=False)
                recipe.image = None
            
            # If a regular user is editing, set approval status to false
            if not request.user.is_superuser:
                recipe.is_approved = False
                message = "Your recipe has been updated and is awaiting approval."
            else:
                message = "Recipe has been updated successfully."
                
            recipe.save()
            form.save_m2m()  # Save the many-to-many data
            
            messages.success(request, message)
            
            # Redirect to appropriate page
            if request.user.is_superuser:
                return redirect('manage_recipes')
            return redirect('my_recipes')
    else:
        form = RecipeForm(instance=recipe)
    
    return render(request, 'recipes/edit_recipe.html', {
        'form': form,
        'recipe': recipe
    })

@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'recipes/my_recipes.html', {'recipes': recipes})

@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Check if the user is the owner of the recipe or an admin
    if recipe.created_by != request.user and not request.user.is_superuser:
        messages.error(request, "You don't have permission to delete this recipe.")
        return HttpResponseForbidden("You don't have permission to delete this recipe.")
    
    if request.method == 'POST':
        recipe_name = recipe.name
        recipe.delete()
        messages.success(request, f'Recipe "{recipe_name}" has been deleted.')
        
        # Redirect to appropriate page
        if request.user.is_superuser:
            return redirect('manage_recipes')
        return redirect('my_recipes')
    
    return render(request, 'recipes/delete_recipe.html', {'recipe': recipe})

@user_passes_test(lambda u: u.is_superuser)
def manage_recipes(request):
    pending_recipes = Recipe.objects.filter(is_approved=False).order_by('-created_at')
    active_recipes = Recipe.objects.filter(is_approved=True, is_archived=False).order_by('-created_at')
    archived_recipes = Recipe.objects.filter(is_approved=True, is_archived=True).order_by('-created_at')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        recipe_id = request.POST.get('recipe_id')
        
        if recipe_id:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            
            if action == 'approve':
                recipe.is_approved = True
                recipe.save()
                messages.success(request, f'Recipe "{recipe.name}" has been approved.')
            elif action == 'reject':
                recipe.delete()
                messages.success(request, f'Recipe "{recipe.name}" has been rejected and deleted.')
            elif action == 'archive':
                recipe.is_archived = True
                recipe.save()
                messages.success(request, f'Recipe "{recipe.name}" has been archived.')
            elif action == 'unarchive':
                recipe.is_archived = False
                recipe.save()
                messages.success(request, f'Recipe "{recipe.name}" has been restored from archive.')
                
        return redirect('manage_recipes')
    
    return render(request, 'recipes/manage_recipes.html', {
        'pending_recipes': pending_recipes,
        'active_recipes': active_recipes,
        'archived_recipes': archived_recipes
    })
