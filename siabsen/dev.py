from .settings import BASE_DIR

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['https://sailfish-dominant-purely.ngrok-free.app']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_ROOT = BASE_DIR / 'website/static/'

MEDIA_ROOT = BASE_DIR / 'website/media/'