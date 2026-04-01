import os
from pathlib import Path

# Долбоордун негизги папкасы
BASE_DIR = Path(__file__).resolve().parent.parent

# Коопсуздук жөндөөлөрү
SECRET_KEY = 'django-insecure-a$k7$&_rpi(heh+=a=#!e9@q7*^!j+fj-q&!jiolbzgc-)4k+y'
DEBUG = True
ALLOWED_HOSTS = ['*']

# Колдонмолордун тизмеси
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',  # Бул staticfiles'тан жогору болушу керек
    'django.contrib.staticfiles',
    'cloudinary',
    'shop',
]

# Ортоңку программалар (Middleware)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Статикалык файлдар үчүн
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# Шаблондор (Templates)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Шаблондор папкасы
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Маалымат базасы
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Тил жана убакыт
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- СТАТИКАЛЫК ФАЙЛДАР (CSS, JS, Images) ---
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_DIR = os.path.join(BASE_DIR, 'static')
if os.path.exists(STATIC_DIR):
    STATICFILES_DIRS = [STATIC_DIR]
else:
    STATICFILES_DIRS = []

# Whitenoise жөндөөлөрү
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
WHITENOISE_MIME_TYPES = {
    '.mp4': 'video/mp4',
}

# --- CLOUDINARY ЖАНА MEDIA ---
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dtuyalp6m',
    'API_KEY': '636667862685854',
    'API_SECRET': 'PgRp9Z7dBhdkoVTk0K1sa1I1390'
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- TELEGRAM BOT ---
TELEGRAM_BOT_TOKEN = '8587802085:AAELrMSN0WH1crYaKVqb3RzWLTloS5nAICU'
TELEGRAM_CHAT_ID = '1304389999'

# --- AI GEMINI KEY ---
# Жаңыланган ачкыч: image_669d9d.png
GEMINI_API_KEY = 'AIzaSyALVs4GXxDZgc-z3oO_RZTPWHPQoE4CUVE'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'