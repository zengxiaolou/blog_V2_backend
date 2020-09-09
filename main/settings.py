"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apis'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extract_apps'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=tpgy423n=fhwr*&k9^tk@_^%%z9gm7m+5%6t*0p2r3zw=%fb1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*", ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apis.users',
    'apis.utils',
    'apis.article',
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'django_filters',
    'extract_apps.rest_captcha',
    'django_elasticsearch_dsl',
    # 'django_elasticsearch_dsl_drf'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', #注意顺序，必须放在这儿
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
# 允许所有的请求头
CORS_ALLOW_HEADERS = ('*', )
# 允许所有方法
CORS_ALLOW_METHODS = ('*', )

ROOT_URLCONF = 'main.urls'
AUTH_USER_MODEL = 'users.UserProfile'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# 媒体文件路径
MEDIA_URL = "/media/"

# 媒体文件根路径
MEDIA_ROOT = os.path.join(BASE_DIR, "static/../media")

MEDIAFILES_DIRS = (
    os.path.join(BASE_DIR, "static/../media"),
)

# 内存
CACHES = {
  "default": {
    "BACKEND": "django_redis.cache.RedisCache",
    "LOCATION": "redis://127.0.0.1:6379",
    # "LOCATION": "redis://redis:6379",
    "OPTIONS": {
      "CLIENT_CLASS": "django_redis.client.DefaultClient",
      "CONNECTION_POOL_KWARGS": {"max_connections": 100}
    }
  }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
     # 版本使用的参数名称
    'VERSION_PARAM': 'version',
    # 默认使用的版本
    'DEFAULT_VERSION': 'v1',
    # 分页设置
    'DEFAULT_PAGINATION_CLASS': 'apis.utils.pagination.MyPageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

REST_FRAMEWORK_EXTENSIONS = {
   'DEFAULT_BULK_OPERATION_HEADER_NAME': None
}


AUTHENTICATION_BACKENDS = (
    'apis.users.utils.CustomBackend',
)


JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),  # 生成的token有效期
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'apis.users.utils.jwt_response_payload_handler',  # response中token的payload部分处理函数
    'JWT_SECRET_KEY': 'zzxxyy123',
}

# 手机号正则表达式
REGEX_MOBILE = "^1[354789]\d{9}$|^147\d{8}$|^176\d{8}$"

EMAIL_HOST = 'smtp.163.com'  # 发送邮件的服务器地址
EMAIL_HOST_USER = '18328457630@163.com'  # 不含‘@126.com’的后缀
EMAIL_HOST_PASSWORD = 'xiaolou123'  # 非邮箱登录密码
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = '小楼的破栈<18328457630@163.com>'

# broker配置，使用Redis作为消息中间件
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/1'
# backend配置，这里使用redis
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
# 结果序列化方案
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIME_ZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True

SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {
      'Basic': {
            'type': 'basic'
      },
      'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
      }
   }
}


# 七牛云设置
# 需要填写你的Access_key 和 Secret_key
ACCESS_KEY = '3hbl1YOcVTeyYsHOxvT73OpT-zK5jRBPda8tgCv_'
SECRET_KEY = 'TWYbwJ9Y07XNCu0BB7d-6Ek1u5qHEe8D9uWD2DHU'
BUCKET_NAME = 'messstack01'


# Elasticsearch configuration
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200'
    },
}

ELASTICSEARCH_INDEX_NAME = {
    'apis.article.documents': "article"
}