import os
from pathlib import Path

# ==================== НЕГИЗГИ ЖӨНДӨӨЛӨР ====================
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-a$k7$&_rpi(heh+=a=#!e9@q7*^!j+fj-q&!jiolbzgc-)4k+y'  # Productionдо өзгөртүңүз!

# ==================== КООПСУЗДУК ====================
DEBUG = True  # Productionдо сөзсүз False кылыңыз!

ALLOWED_HOSTS = ['*']  # Productionдо конкреттүү домендерди гана жазыңыз

# ==================== INSTALLED_APPS ====================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Үчүнчү тараптын пакеттери
    'cloudinary_storage',
    'cloudinary',
    'shop',
]

# ==================== MIDDLEWARE ====================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# ==================== ТЕМПЛЕЙТТЕР ====================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# ==================== БАЗА ====================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==================== АВТОРИЗАЦИЯ ЖАНА КООПСУЗДУК ====================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 10}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Session жана CSRF коопсуздугу
SESSION_COOKIE_SECURE = False          # Localhostто False, Productionдо True
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

# ==================== СТАТИКА ЖАНА МЕДИА ====================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] if os.path.exists(os.path.join(BASE_DIR, 'static')) else []

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Cloudinary
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dtuyalp6m',
    'API_KEY': '636667862685854',
    'API_SECRET': 'PgRp9Z7dBhdkoVTk0K1sa1I1390'
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# ==================== TELEGRAM ЖАНА AI ====================
TELEGRAM_BOT_TOKEN = '8266512637:AAE2LxxouGBmhJLT9BrrAYbx7z4vWxLGZ0g'
TELEGRAM_CHAT_ID = '5106658401'
ADMIN_PHONE = '+996995519951'
GEMINI_API_KEY = 'AIzaSyALVs4GXxDZgc-z3oO_RZTPWHPQoE4CUVE'

# ==================== БАШКА ====================
LANGUAGE_CODE = 'ru'      # Кыргыз тилин кааласаңыз 'ky' койсоңуз болот
TIME_ZONE = 'Asia/Bishkek'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'