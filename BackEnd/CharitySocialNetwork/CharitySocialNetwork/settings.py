"""
Django settings for CharitySocialNetwork project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from . import configLocal

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-oh!&a-p-$tqc&l=mmb6gh8tf8h2ue%p4f&o2cjgkpj9bfqjh2-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'AppCharitySocialNetwork.apps.AppcharitysocialnetworkConfig',
    'rest_framework',
    'drf_yasg',
    'rest_framework.authtoken',
    'oauth2_provider',
    'corsheaders',
    'django_filters',
    'cloudinary',
    'ckeditor',
    'ckeditor_uploader',
    'graphene_django',
    # 'debug_toolbar'
]

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',,
    'AppCharitySocialNetwork.middlewares.LoginByClientIdMiddleware',
    'AppCharitySocialNetwork.middlewares.AuthorizationMiddleware',

]

ROOT_URLCONF = 'CharitySocialNetwork.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'CharitySocialNetwork.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

AUTH_USER_MODEL = "AppCharitySocialNetwork.User"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': configLocal.db,
        'USER': configLocal.userDB,
        'PASSWORD': configLocal.passwordDB,
        'HOST': configLocal.hostDB
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = '%s/AppCharitySocialNetwork/static/' % BASE_DIR
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication'
    ]
}

# OAUTH2_PROVIDER = {
#     # parses OAuth2 data from application/json requests
#     'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore',
#     # this is the list of available scopes
#     'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
# }

CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOWED_ORIGINS = ['http://dkmh.ou.edu.vn',]

# Page number
PAGE_SIZE_QUERY_PARAM = "page_size"

POST_PAGE_SIZE = 30
MAX_POST_PAGE_SIZE = 50

COMMENT_PAGE_SIZE = 30
MAX_COMMENT_PAGE_SIZE = 50

NOTIFICATION_PAGE_SIZE = 30
MAX_NOTIFICATION_PAGE_SIZE = 50

IMAGE_PAGE_SIZE = 30
MAX_IMAGE_PAGE_SIZE = 50

# Notification
TYPE_NOTIFICATION = [
    (0, "Thông báo hệ thông"),
    (1, "Thông báo người dùng"),
    (2, "Thông báo bài viết mới"),
    (3, "Thông báo có bài viết đấu giá"),
    (4, "Report"),
]

NOTIFICATION_MESSAGE = {
    "add_post": {
        "title": "Tạo bài viết thành công",
        "message": "Bài sẽ được đội admin duyệt sớm bạn hãy chờ nhé"
    },
    'update_post': {
        'title': "Update",
        'message': "bạn vừa thay đổi nội dung bài viết chờ đội admin duyệt bài lại nhé"
    },
    'delete_post': {
        "title": "Xóa bài viết",
        "message": "Xóa bài viết thành công"
    },
    'comment_child_new': {
        "title": "Bạn có bình luận mới",
        "message": "abc"
    },
    'comment_post': {
        "title": "Có bình luận mới",
        "message": "abc"
    },

}

# DROPBOX_SETTING = {
#     "app_key": configLocal.dropbox.get("app_key"),
#     "app_secret": configLocal.dropbox.get("app_secret"),
#     "access_token": configLocal.dropbox.get("access_token")
# }

CLOUDINARY = {
    'cloud_name': 'charitycdn',
    'api_key': '717287562921176',
    'api_secret': configLocal.cloudinary.get('api_secret'),
    'secure': True
}

CLOUDINARY_URL = 'cloudinary://717287562921176:CPNboHJ8GqH0uT5f_uLNgHpuMIk@charitycdn'

FACEBOOK = {
    'id_app': '502879657806363',
    'secret_key': 'a8e308eff516df7638fd7444862d479b',
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'charitysocialnetwork@gmail.com'
EMAIL_HOST_PASSWORD = 'Tinice@123'
EMAIL_PORT = 587

CKEDITOR_UPLOAD_PATH = 'images/newspost/'

# DROPBOX_OAUTH2_TOKEN = configLocal.dropbox.get("access_token")
# DROPBOX_ROOT_PATH = '/images/'
# DROPBOX_TIMEOUT = 100
# DROPBOX_WRITE_MODE = 'add'
# CKEDITOR_ALLOW_NONIMAGE_FILES = True

CATEGORY_POST_AUCTION = 1

# phần thêm của đồ án

GRAPHENE = {
    "SCHEMA": "AppCharitySocialNetwork.schema.schema",
    'MIDDLEWARE': [
        'graphene_django.debug.DjangoDebugMiddleware',
        # 'AppCharitySocialNetwork.middlewares.AuthorizationMiddleware',
        # 'oauth2_provider.contrib.rest_framework.OAuth2Authentication'
    ],
    'RELAY_CONNECTION_MAX_LIMIT': 100,  # chỉ định số đối tượng lấy được trong một lần request,
    'CAMELCASE_ERRORS': False,  # tên field bị lỗi sẽ được chuyển thành chuẩn đặt tên CAMELCASE nếu được bặt lên True
}


