import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-c4=8+h3!nl)l-!g*=so#ren#i7ap5880+htec&_hwb4mhskj)8')

DEBUG = True
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
    
    'django_summernote',
    'django_quill',
    'tinymce',
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
    'domains.tracker',
    'domains.qabul',
    'domains.ilmiy_tadqiqot',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

X_FRAME_OPTIONS = 'SAMEORIGIN'

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
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'



MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {
    'default': {
        'BACKEND':  'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'usas-api-cache',
        'TIMEOUT':  300,
    }
}

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
CORS_ALLOW_ALL_ORIGINS = True

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
    "search_model": [
        "auth.User",
        "students.Person",
        "news.News",
        "academic.FakultetKafedra",
        "pages.NavbarSubItem",
    ],

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

    # Menyu tartibi saytdagi navbar oqimiga moslangan:
    # Akademiya → Faoliyat → Xalqaro aloqalar → Talabalarga → Matbuot xizmati
    # → Aloqa/Rektorga murojaat → Reyting → texnik.
    "order_with_respect_to": [
        "auth",

        # ── App-guruhlar tartibi (navbar top-menyu bo'yicha) ──
        "pages",          # Akademiya (asosiy), Aloqa, ... (Sayt sozlamalari)
        "academic",       # Akademiya: fakultet, kafedra, huzuridagi tashkilotlar
        "infra",          # Akademiya: o'quv binolari va sport inshootlari
        "activities",     # Faoliyat: sport / ilmiy
        "international",   # Xalqaro aloqalar + Reyting
        "students",       # Talabalarga + Faxrlarimiz (shaxslar)
        "news",           # Matbuot xizmati
        "contact",        # Aloqa / Rektorga murojaat
        "axborot",
        "qabul",
        "tenders",
        "ilmiy_tadqiqot",
        "tracker",
        "common",
        "django_celery_beat",
        "django_celery_results",

        # ── "Sayt sozlamalari" (pages) ichidagi bo'limlar tartibi (navbar bo'yicha) ──
        # Akademiya
        "pages.aboutacademy", "pages.aboutacademysection", "pages.aboutacademyprogram",
        "pages.akademiyamissiya", "pages.homepagehaqida", "pages.presidentquote", "pages.herovideo",
        "pages.rekvizit", "pages.meyoriyhujjat", "pages.markaz",
        "pages.orgsection", "pages.orgnode", "pages.partner",
        # Faoliyat
        "pages.ilmiybolim",
        # Talabalarga
        "pages.iqtidorlitalabalar", "pages.kampusxizmati", "pages.interaktivxizmat",
        "pages.aboutsocial", "pages.aboutsocialsection",
        # Aloqa
        "pages.contactconfig", "pages.contactlocation",
        "pages.savoljavobcategory", "pages.savoljavob",
        # Texnik (navbar/bloklar)
        "pages.navbarcategory", "pages.navbarsubitem",
        "pages.contentblock", "pages.linkblock", "pages.sociallink",
    ],

    # ── Sidebar qo'shimcha havolalar ─────────────────────────────────────────
    "custom_links": {
        "pages": [
            {
                "name":        "🔗 Navbar menyusini tahrirlash",
                "url":         "admin:pages_navbarcategory_changelist",
                "icon":        "fas fa-bars",
                "permissions": ["pages.view_navbarcategory"],
            },
            {
                "name":        "📄 Sahifalar va bloklar",
                "url":         "admin:pages_contentblock_changelist",
                "icon":        "fas fa-th-large",
                "permissions": ["pages.view_contentblock"],
            },
            {
                "name":        "🏛️ Markazlar va Bo'limlar",
                "url":         "admin:pages_markaz_changelist",
                "icon":        "fas fa-building",
                "permissions": ["pages.view_markaz"],
            },
        ],
        "news": [
            {
                "name":        "📰 Yangiliklar",
                "url":         "admin:news_news_changelist",
                "icon":        "fas fa-newspaper",
                "permissions": ["news.view_news"],
            },
            {
                "name":        "📅 Tadbirlar",
                "url":         "admin:news_event_changelist",
                "icon":        "fas fa-calendar-alt",
                "permissions": ["news.view_event"],
            },
            {
                "name":        "✍️ Blog",
                "url":         "admin:news_blog_changelist",
                "icon":        "fas fa-pen",
                "permissions": ["news.view_blog"],
            },
        ],
        "students": [
            {
                "name":        "👤 Shaxslar (Rektorat, xodimlar)",
                "url":         "admin:students_person_changelist",
                "icon":        "fas fa-id-card",
                "permissions": ["students.view_person"],
            },
            {
                "name":        "🏅 Olimpiya chempionlari",
                "url":         "admin:students_olimpiyachempion_changelist",
                "icon":        "fas fa-medal",
                "permissions": ["students.view_olimpiyachempion"],
            },
        ],
        "contact": [
            {
                "name":        "📬 Kirgan murojaatlar",
                "url":         "admin:contact_rectorappeal_changelist",
                "icon":        "fas fa-inbox",
                "permissions": ["contact.view_rectorappeal"],
            },
            {
                "name":        "💬 Aloqa xabarlari",
                "url":         "admin:contact_contactmessage_changelist",
                "icon":        "fas fa-envelope",
                "permissions": ["contact.view_contactmessage"],
            },
        ],
    },

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
        # Qabul
        "qabul":                            "fas fa-door-open",
        "qabul.QabulBolim":                 "fas fa-list-alt",
        "qabul.QabulKomissiyaTarkibi":      "fas fa-users",
        "qabul.QabulKuni":                  "fas fa-calendar-check",
        "qabul.CallCenter":                 "fas fa-phone",
        "qabul.QabulYangilik":              "fas fa-newspaper",
        "qabul.QabulNarx":                  "fas fa-money-bill",
        "qabul.QabulHujjat":                "fas fa-file-alt",
        "qabul.QabulNavbar":                "fas fa-bars",
        # International
        "international":                    "fas fa-globe-europe",
        "international.XorijlikProfessor":  "fas fa-chalkboard-teacher",
        "international.AkademikAlmashinuv": "fas fa-exchange-alt",
        "international.XalqaroReytingBolim":"fas fa-trophy",
        "international.PartnerOrganization":"fas fa-handshake",
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
    "default_theme_mode":   "light",
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

# ── TinyMCE ──────────────────────────────────────────────────────────────────
TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'width': '100%',
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'silver',
    'plugins': 'link image preview codesample table code lists paste',
    'toolbar': (
        'undo redo | bold italic underline strikethrough | '
        'fontsize | forecolor backcolor | '
        'alignleft aligncenter alignright alignjustify | '
        'bullist numlist | table link image | code'
    ),
    'menubar': False,
    'statusbar': True,
    'relative_urls': False,
    'remove_script_host': False,
    'convert_urls': True,
    # Word paste cleanup
    'paste_as_text': False,
    'paste_word_valid_elements': 'b,strong,i,em,h1,h2,h3,h4,h5,h6,p,ul,ol,li,a[href],br,table,thead,tbody,tr,td,th',
    'paste_retain_style_properties': 'none',
    'paste_strip_class_attributes': 'all',
    'paste_remove_styles_if_webkit': True,
}
TINYMCE_SPELLCHECKER = False
TINYMCE_COMPRESSOR = False

# ── Summernote ────────────────────────────────────────────────────────────────
SUMMERNOTE_THEME = 'lite'
SUMMERNOTE_CONFIG = {
    'iframe': False,
    'lazy': True,
    'summernote': {
        'width':  '100%',
        'height': '350px',
        'toolbar': [
            ['style',   ['bold', 'italic', 'underline', 'strikethrough', 'clear']],
            ['font',    ['fontsize']],
            ['color',   ['color']],
            ['para',    ['ul', 'ol', 'paragraph']],
            ['table',   ['table']],
            ['insert',  ['link', 'picture', 'hr']],
            ['view',    ['fullscreen', 'codeview']],
            ['misc',    ['clean']],
        ],
        'lang': 'uz-UZ',
        # Strip Word/Office HTML junk (mso- styles, <o:p> tags) on paste
        'cleanPastedHTML': True,
    },
    'attachment_upload_to': 'summernote/',
    'attachment_filesize_limit': 5 * 1024 * 1024,
    'disable_attachment': False,
}
