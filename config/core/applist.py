# Application definition

BEFORE_DJANGO_APPS = [
    # before django
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites'
]
SITE_ID = 1
THIRD_PART_APPS = [
    'django_filters',
    'rest_framework',
    'corsheaders',    
    'drf_yasg',
    'django_celery_results',
    'celery'
]

LOCAL_APPS = [
    # local apps
    'apps.accounts',
    'apps.sensors',
    'apps.company',
    'apps.memberships',
]

INSTALLED_APPS = BEFORE_DJANGO_APPS + DJANGO_APPS + THIRD_PART_APPS + LOCAL_APPS