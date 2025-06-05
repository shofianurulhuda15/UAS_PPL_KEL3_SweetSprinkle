# 🧁 SweetSprinkle - Setup Guide untuk Recipe Sharing Platform

# 📽️ Presentasi dan Dokumentasi

Berikut ini adalah link video dan file presentasi dari proyek SweetSprinkle Recipe Sharing Platform.

## 🎥 Link Video Presentasi
[Tonton Video](https://youtu.be/Tq60aUDqeYI)

## 📊 Link PPT Presentasi
[Lihat PPT](https://www.canva.com/design/DAGpeJt6Jpw/uwyZm-bu4Vh2bHnGO2vYhg/edit?utm_content=DAGpeJt6Jpw&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

## 📝 Deskripsi Proyek

SweetSprinkle adalah platform berbagi resep yang memungkinkan pengguna untuk:
- Membuat dan berbagi resep masakan
- Menelusuri resep berdasarkan kategori
- Menyimpan resep favorit
- Mengelola resep yang telah dibuat
- Berinteraksi dengan komunitas pecinta masakan

Aplikasi ini dibangun menggunakan Django framework dengan tampilan modern menggunakan Tailwind CSS.

## Langkah 1: Persiapan File Structure

Pastikan struktur direktori seperti ini:
```
sweetsprinkle/
├── sweetsprinkle/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── recipes/
│   ├── __init__.py
│   ├── admin.py          # ✅ Konfigurasi admin panel
│   ├── apps.py
│   ├── models.py         # ✅ Model data Recipe, Category, dan Favorite
│   ├── forms.py          # ✅ Form untuk CRUD Recipe
│   ├── views.py          # ✅ View functions untuk semua fitur
│   ├── urls.py           # ✅ URL routing untuk recipes app
│   ├── migrations/
│   ├── templatetags/     # ✅ Custom template tags
│   └── templates/        # ✅ Template HTML
│       └── recipes/
│           ├── home.html
│           ├── detail.html
│           ├── add_recipe.html
│           ├── edit_recipe.html
│           ├── delete_recipe.html
│           ├── my_recipes.html
│           ├── favorites.html
│           └── manage_recipes.html
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── forms.py          # ✅ Form untuk registrasi dan profile
│   ├── views.py          # ✅ View untuk autentikasi dan profile
│   ├── urls.py           # ✅ URL routing untuk accounts app
│   ├── migrations/
│   └── templates/
│       └── accounts/
│           ├── profile.html
│           └── register.html
├── templates/            # ✅ Template global
│   ├── base.html         # ✅ Template dasar dengan navbar responsif
│   ├── registration/     # ✅ Template autentikasi
│   │   ├── login.html
│   │   └── password_*.html
├── media/                # ✅ Folder untuk upload gambar
├── static/               # ✅ File statis (CSS, JS, dll)
└── manage.py
```

## Langkah 2: Update Settings

Pastikan di `sweetsprinkle/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'recipes',  # ✅ App recipes terdaftar
    'accounts', # ✅ App accounts terdaftar
]

# Database (SQLite default)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Template settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ✅ Lokasi global templates
        'APP_DIRS': True,  # ✅ Pastikan True untuk template di app
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Static files configuration
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Redirect settings
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Internationalization
LANGUAGE_CODE = 'en-us'  # Bisa diganti 'id' untuk Bahasa Indonesia
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_TZ = True
```

## Langkah 3: URL Configuration

### Main URLs (`sweetsprinkle/urls.py`):

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Recipes URLs (`recipes/urls.py`):

```python
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
```

### Accounts URLs (`accounts/urls.py`):

```python
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]
```

## Langkah 4: Model Configuration

### Recipe Model (`recipes/models.py`):

```python
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
```

## Langkah 5: Migration dan Setup Database

Jalankan command berikut di terminal:

```bash
# 1. Buat migration untuk model
python manage.py makemigrations

# 2. Terapkan migration ke database
python manage.py migrate

# 3. Buat superuser untuk akses admin
python manage.py createsuperuser
```

Ikuti instruksi untuk membuat superuser:
- Username: admin (atau sesuai keinginan)
- Email: admin@sweetsprinkle.com (opsional)
- Password: (pilih password yang aman)

## Langkah 6: Populate Data Sample (Opsional)

Buat file `recipes/management/commands/populate_data.py`:

```python
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Category, Recipe
import random

class Command(BaseCommand):
    help = 'Populate database with sample recipes and categories'
    
    def handle(self, *args, **options):
        # Create categories
        categories = [
            "Dessert", "Cake", "Cookie", "Bread", "Pastry", 
            "Chocolate", "Vegan", "Gluten-Free", "Quick & Easy", "Holiday"
        ]
        
        created_categories = []
        for cat_name in categories:
            category, created = Category.objects.get_or_create(name=cat_name)
            created_categories.append(category)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {cat_name}'))
        
        # Create sample recipes
        sample_recipes = [
            {
                'name': 'Chocolate Chip Cookies',
                'ingredients': '2 cups all-purpose flour\n1 cup butter\n1 cup chocolate chips\n1/2 cup sugar\n2 eggs\n1 tsp vanilla extract\n1/2 tsp baking soda\n1/4 tsp salt',
                'steps': '1. Preheat oven to 350°F (175°C)\n2. Cream butter and sugar\n3. Beat in eggs and vanilla\n4. Mix in dry ingredients\n5. Fold in chocolate chips\n6. Drop spoonfuls onto baking sheet\n7. Bake for 10-12 minutes',
                'categories': ['Cookie', 'Quick & Easy'],
            },
            {
                'name': 'Strawberry Cheesecake',
                'ingredients': '2 cups graham cracker crumbs\n1/2 cup butter, melted\n24 oz cream cheese\n1 cup sugar\n3 eggs\n1 tsp vanilla extract\n2 cups fresh strawberries\n1/4 cup strawberry jam',
                'steps': '1. Mix graham cracker crumbs with melted butter and press into pan\n2. Beat cream cheese and sugar until smooth\n3. Add eggs one at a time\n4. Pour into crust and bake at 325°F for 55 minutes\n5. Cool and refrigerate for 4 hours\n6. Top with fresh strawberries and jam',
                'categories': ['Dessert', 'Cake'],
            },
            {
                'name': 'Vanilla Cupcakes',
                'ingredients': '1 1/2 cups all-purpose flour\n1 cup sugar\n1/2 cup butter\n2 eggs\n2 tsp vanilla extract\n1/2 cup milk\n1 1/2 tsp baking powder\n1/4 tsp salt',
                'steps': '1. Preheat oven to 350°F\n2. Line cupcake pan with paper liners\n3. Cream butter and sugar\n4. Add eggs and vanilla\n5. Alternate adding dry ingredients and milk\n6. Fill liners 2/3 full\n7. Bake for 18-20 minutes',
                'categories': ['Cake', 'Dessert'],
            },
            {
                'name': 'Vegan Banana Bread',
                'ingredients': '3 ripe bananas\n1/3 cup melted coconut oil\n1/2 cup maple syrup\n1 tsp vanilla extract\n2 cups whole wheat flour\n1 tsp baking soda\n1/2 tsp cinnamon\n1/4 tsp salt\n1/2 cup chopped walnuts (optional)',
                'steps': '1. Preheat oven to 350°F\n2. Grease a 9×5-inch loaf pan\n3. Mash bananas in a large bowl\n4. Mix in oil, maple syrup, and vanilla\n5. Add dry ingredients and mix until combined\n6. Fold in walnuts if using\n7. Pour into pan and bake for 55-60 minutes',
                'categories': ['Bread', 'Vegan', 'Quick & Easy'],
            },
            {
                'name': 'Gluten-Free Chocolate Brownies',
                'ingredients': '1/2 cup butter\n6 oz dark chocolate\n3/4 cup sugar\n2 eggs\n1 tsp vanilla extract\n1/2 cup almond flour\n1/4 cup cocoa powder\n1/4 tsp salt',
                'steps': '1. Preheat oven to 350°F\n2. Line an 8×8-inch pan with parchment paper\n3. Melt butter and chocolate together\n4. Whisk in sugar, eggs, and vanilla\n5. Fold in almond flour, cocoa, and salt\n6. Pour into pan and bake for 25-30 minutes',
                'categories': ['Dessert', 'Chocolate', 'Gluten-Free'],
            }
        ]
        
        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'is_staff': True,
                'is_superuser': True,
                'email': 'admin@sweetsprinkle.com',
            }
        )
        
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user'))
        
        # Create recipes
        for recipe_data in sample_recipes:
            recipe, created = Recipe.objects.get_or_create(
                name=recipe_data['name'],
                defaults={
                    'ingredients': recipe_data['ingredients'],
                    'steps': recipe_data['steps'],
                    'created_by': admin_user,
                    'is_approved': True,
                }
            )
            
            if created:
                # Add categories
                for cat_name in recipe_data['categories']:
                    category = Category.objects.get(name=cat_name)
                    recipe.categories.add(category)
                
                self.stdout.write(self.style.SUCCESS(f'Created recipe: {recipe.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Recipe already exists: {recipe.name}'))
        
        self.stdout.write(self.style.SUCCESS('Finished populating data!'))
```

Untuk menggunakan command ini:
```bash
# Buat direktori management
mkdir -p recipes/management/commands
touch recipes/management/__init__.py
touch recipes/management/commands/__init__.py

# Jalankan populate command
python manage.py populate_data
```

## Langkah 7: Testing Website

Jalankan development server:
```bash
python manage.py runserver
```

### Test URLs:
- **Homepage**: http://127.0.0.1:8000/
- **Detail Resep**: http://127.0.0.1:8000/recipe/1/
- **Tambah Resep**: http://127.0.0.1:8000/add/
- **Resep Saya**: http://127.0.0.1:8000/my-recipes/
- **Favorit**: http://127.0.0.1:8000/favorites/
- **Login**: http://127.0.0.1:8000/accounts/login/
- **Register**: http://127.0.0.1:8000/accounts/register/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Fitur yang Tersedia:

### ✅ User Authentication:
- **Register**: Pendaftaran pengguna baru
- **Login/Logout**: Autentikasi pengguna
- **Profile**: Halaman profil pengguna

### ✅ CRUD Operations untuk Resep:
- **Create**: Form tambah resep dengan validasi
- **Read**: List resep dan detail resep
- **Update**: Edit resep yang sudah ada
- **Delete**: Hapus resep dengan konfirmasi

### ✅ Fitur Sosial:
- **Favorite**: Menyimpan resep favorit
- **Filtering**: Filter resep berdasarkan kategori
- **Search**: Pencarian resep berdasarkan nama atau bahan

### ✅ Admin Panel:
- **Manage Recipes**: Dashboard admin untuk mengelola resep
- **Approve/Archive**: Menyetujui atau mengarsipkan resep
- **Category Management**: Mengelola kategori resep

### ✅ User Interface:
- **Responsive Design**: Tampilan yang responsif untuk semua perangkat
- **Mobile Menu**: Menu navigasi khusus untuk perangkat mobile
- **Modern UI**: Desain modern dengan Tailwind CSS
- **Success/Error Messages**: Notifikasi untuk aksi pengguna

## Struktur Database:

### Recipe Model:
- **name**: Nama resep
- **ingredients**: Bahan-bahan yang dibutuhkan
- **steps**: Langkah-langkah pembuatan
- **image**: Gambar resep (opsional)
- **categories**: Kategori resep (many-to-many)
- **created_by**: Pengguna yang membuat resep
- **is_approved**: Status persetujuan resep
- **is_archived**: Status arsip resep
- **created_at**: Waktu pembuatan resep

### Category Model:
- **name**: Nama kategori

### Favorite Model:
- **user**: Pengguna yang menyukai resep
- **recipe**: Resep yang disukai
- **added_at**: Waktu penambahan ke favorit

## Troubleshooting:

1. **Template not found**: Pastikan struktur direktori template benar dan `APP_DIRS` diset `True` di settings.py
2. **No reverse match**: Cek nama URL di urls.py dan pastikan parameter yang dibutuhkan sudah disediakan
3. **Database error**: Jalankan `python manage.py migrate` untuk memastikan skema database sudah diupdate
4. **Media files tidak tampil**: Pastikan `MEDIA_URL` dan `MEDIA_ROOT` sudah dikonfigurasi dengan benar
5. **Static files tidak tampil**: Jalankan `python manage.py collectstatic` untuk production
6. **Form validation errors**: Cek definisi form dan model untuk memastikan validasi sudah benar

## Pengembangan Selanjutnya:

- **Rating System**: Menambahkan fitur rating dan ulasan untuk resep
- **Social Sharing**: Integrasi dengan media sosial untuk berbagi resep
- **Recipe Collections**: Fitur untuk mengelompokkan resep dalam koleksi
- **Advanced Search**: Pencarian lanjutan berdasarkan bahan, waktu memasak, dll
- **Nutrition Information**: Informasi nutrisi untuk setiap resep
- **Meal Planning**: Fitur perencanaan makanan mingguan
- **Shopping List**: Generate daftar belanja dari resep yang dipilih
- **API Endpoints**: REST API untuk integrasi dengan aplikasi mobile
- **Internationalization**: Dukungan multi-bahasa

## Teknologi yang Digunakan:

- **Backend**: Django 5.2
- **Database**: SQLite (development), PostgreSQL (production recommended)
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Media Storage**: Local storage (development), AWS S3 (production recommended)
- **Deployment**: Heroku, PythonAnywhere, atau VPS

## Kontributor:

- Shofia Nurul Huda 2208107010015
- Nisa Rianti 2208107010018
- Jihan Nabilah 2208107010035

## Lisensi:

© 2025 SweetSprinkle. All Rights Reserved. 