import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-c4=8+h3!nl)l-!g*=so#ren#i7ap5880+htec&_hwb4mhskj)8')

DEBUG = False
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')


# Application definition

INSTALLED_APPS = [
    'jazzmin',              # must be BEFORE django.contrib.admin
    # Default Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    'drf_spectacular',
    'corsheaders',
    'django_filters',
    'django_celery_results',
    'django_celery_beat',
    
    'common',
    'domains.pages',
    'domains.academic',
    'domains.international',
    'domains.students',
    'domains.news',
    'domains.tenders',
    'domains.contact',
    'domains.activities',
    'domains.axborot',
    'domains.infra',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True, 
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

WSGI_APPLICATION = 'config.wsgi.application'






# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'



MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DRF Settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# CORS — Frontend ulanishi uchun
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')
    if origin.strip()
]

# Swagger UI — title, description, version, tags
# ── Jazzmin — Django Admin UI ──────────────────────────────────────────────────
JAZZMIN_SETTINGS = {
    # ── Brend ────────────────────────────────────────────────────────────────
    "site_title":        "USAS Admin",
    "site_header":       "O'zbekiston Davlat Sport Akademiyasi",
    "site_brand":        "USAS",
    "site_logo":         None,
    "site_logo_classes": "img-circle",
    "site_icon":         None,
    "welcome_sign":      "USAS boshqaruv paneliga xush kelibsiz",
    "copyright":         "O'zbekiston Davlat Sport Akademiyasi © 2025",

    # ── Qidiruv ──────────────────────────────────────────────────────────────
    "search_model": ["auth.User", "auth.Group"],

    # ── Top menyusi ──────────────────────────────────────────────────────────
    "topmenu_links": [
        {"name": "Bosh sahifa",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "API Docs",     "url": "/api/schema/swagger-ui/", "new_window": True},
        {"name": "Sayt",         "url": "/",           "new_window": True},
    ],

    # ── Foydalanuvchi menyusi (o'ng yuqori) ──────────────────────────────────
    "usermenu_links": [
        {"name": "API Hujjatlar", "url": "/api/schema/swagger-ui/", "new_window": True},
    ],

    # ── Sidebar navigatsiyasi ─────────────────────────────────────────────────
    "show_sidebar":       True,
    "navigation_expanded": True,
    "hide_apps":          [],
    "hide_models":        [],

    "order_with_respect_to": [
        "auth",
        "pages",
        "students",
        "academic",
        "news",
        "activities",
        "axborot",
        "tenders",
        "contact",
        "international",
        "infra",
        "common",
        "django_celery_beat",
        "django_celery_results",
    ],

    "icons": {
        # Auth
        "auth":                             "fas fa-users-cog",
        "auth.user":                        "fas fa-user",
        "auth.Group":                       "fas fa-users",
        # Pages
        "pages":                            "fas fa-globe",
        "pages.SiteConfig":                 "fas fa-cog",
        "pages.NavbarItem":                 "fas fa-bars",
        "pages.NavbarSubItem":              "fas fa-list",
        "pages.Banner":                     "fas fa-images",
        "pages.SocialLink":                 "fas fa-share-alt",
        "pages.ContactInfo":                "fas fa-address-card",
        "pages.OrgStructure":               "fas fa-sitemap",
        "pages.AboutAcademy":               "fas fa-university",
        # Students / People
        "students":                         "fas fa-user-graduate",
        "students.PersonCategory":          "fas fa-folder",
        "students.Person":                  "fas fa-id-card",
        "students.PersonContent":           "fas fa-file-alt",
        "students.PersonImage":             "fas fa-image",
        "students.StudentInfoCategory":     "fas fa-folder-open",
        "students.StudentInfo":             "fas fa-info-circle",
        "students.OlimpiyaChempion":        "fas fa-medal",
        "students.MagistrGroup":            "fas fa-chalkboard-teacher",
        "students.MagistrStudent":          "fas fa-user-tie",
        "students.Stipendiya":              "fas fa-money-bill-wave",
        # Academic
        "academic":                         "fas fa-graduation-cap",
        "academic.AcademyStat":             "fas fa-chart-bar",
        "academic.AcademyDetailPage":       "fas fa-book-open",
        "academic.FakultetKafedra":         "fas fa-building",
        "academic.KafedraPublication":      "fas fa-book",
        "academic.KafedraXodim":            "fas fa-user-tie",
        # News
        "news":                             "fas fa-newspaper",
        "news.NewsCategory":                "fas fa-tags",
        "news.News":                        "fas fa-file-alt",
        "news.Event":                       "fas fa-calendar-alt",
        # Activities
        "activities":                       "fas fa-running",
        # Axborot
        "axborot":                          "fas fa-bullhorn",
        "axborot.AxborotSection":           "fas fa-layer-group",
        "axborot.AxborotVazifa":            "fas fa-tasks",
        # Tenders
        "tenders":                          "fas fa-file-contract",
        # Contact
        "contact":                          "fas fa-envelope",
        # International
        "international":                    "fas fa-globe-europe",
        # Infra
        "infra":                            "fas fa-building",
        # Common
        "common":                           "fas fa-database",
        "common.Tag":                       "fas fa-tag",
        # Celery
        "django_celery_beat":               "fas fa-clock",
        "django_celery_results":            "fas fa-check-circle",
    },

    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    # ── Related modals ────────────────────────────────────────────────────────
    "related_modal_active": True,

    # ── Custom CSS/JS ─────────────────────────────────────────────────────────
    "custom_css": None,
    "custom_js":  None,

    # ── Boshqa ───────────────────────────────────────────────────────────────
    "show_ui_builder":      False,   # productioneda False
    "changeform_format":    "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user":  "collapsible",
        "auth.group": "vertical_tabs",
    },
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text":    False,
    "footer_small_text":    False,
    "body_small_text":      False,
    "brand_small_text":     False,
    "brand_colour":         "navbar-success",   # yashil — sport akademiyasi rangi
    "accent":               "accent-success",
    "navbar":               "navbar-dark",
    "no_navbar_border":     True,
    "navbar_fixed":         True,
    "layout_boxed":         False,
    "footer_fixed":         False,
    "sidebar_fixed":        True,
    "sidebar":              "sidebar-dark-success",
    "sidebar_nav_small_text":  False,
    "sidebar_disable_expand":  False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style":  False,
    "sidebar_nav_flat_style":    False,
    "theme":                "default",
    "dark_mode_theme":      "darkly",
    "button_classes": {
        "primary":   "btn-primary",
        "secondary": "btn-secondary",
        "info":      "btn-info",
        "warning":   "btn-warning",
        "danger":    "btn-danger",
        "success":   "btn-success",
    },
    "actions_sticky_top": True,
}

SPECTACULAR_SETTINGS = {
    'TITLE': "O'ZDSA University — Backend API",
    'DESCRIPTION': (
        "O'ZDSA universiteti rasmiy backend API hujjatnamasi.\n\n"
        "**Mavjud bo'limlar:**\n"
        "- `pages` — Sayt konfiguratsiyasi (aloqa, ijtimoiy tarmoqlar, prezident iqtibosi)\n"
        "- `news` — Yangiliklar, tadbirlar va blog\n\n"
        "**Til parametri:** `?lang=uz|ru|en`"
    ),
    'VERSION': '1.0.0',
    'CONTACT': {
        'name': "O'ZDSA IT Bo'limi",
        'email': 'dev@ozdsa.uz',
    },
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATIONS': False,
}
