from .settings import BASE_DIR

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DB_NAME',
        'USER': 'DB_USER', 
        'PASSWORD': 'DB_PASS',
        'PORT': 3306,
        'HOST': 'localhost',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}

STATIC_ROOT = '/home/username/domai/static/'

MEDIA_ROOT = '/home/username/domain/media/'