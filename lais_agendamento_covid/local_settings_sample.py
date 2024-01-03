DEBUG = True
ALLOWED_HOSTS = []
SECRET_KEY = 'django-insecure-s&(zire6i+k9*wmno7*63a808_6tvc&d&d37*3$q#3*9ms@49w'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lais_agendamento_covid',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_URL = '/static/'
