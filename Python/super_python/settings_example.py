'''
FilePath: settings_example.py
Author: yun.huang <1594909346@qq.com>
Date: 2023-08-23 18:09:17
LastEditors: yun.huang <1594909346@qq.com>
LastEditTime: 2023-08-30 15:05:06
Version: 1.0.1
Copyright: 2023 YunYou Innovation Technology Co., Ltd. All Rights Reserved.
Descripttion: 愿你开心每一天~
'''
"""
Django settings for super_python project.

Generated by 'django-admin startproject' using Django 4.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
import sys

from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(1, os.path.join(BASE_DIR, 'extra_apps'))

# ================================================= #
# ******************** 动态配置 ******************** #
# ================================================= #

from config import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_caw@g5(6y1ud63&@nx5n$4*7y2gv123m&5z&p*07x^zv#wait'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = locals().get("DEBUG", True)

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # api规范
    'rest_framework',
    # 允许跨域
    'corsheaders',
    # 核心组件
    'system'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 跨域中间件
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 自定义日志中间件
    'utils.middleware.ApiLoggingMiddleware',
]

ROOT_URLCONF = 'super_python.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 放置前端页面的地方
        'DIRS': [os.path.join(BASE_DIR, 'frontend')]
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

ASGI_APPLICATION = 'super_python.asgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': DATABASE_ENGINE,
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT,
        'CONN_MAX_AGE':DATABASE_CONN_MAX_AGE,
        'OPTIONS': {
                    'charset':DATABASE_CHARSET,
                    # innodb才支持事务
                    'init_command': 'SET default_storage_engine=INNODB',
                }
    }
}

AUTH_USER_MODEL = 'system.Users'
USERNAME_FIELD = 'username'
# 所有app models 对象
ALL_MODELS_OBJECTS = []

# 配置redis缓存
CACHES = {
    'default': {
        # 缓存后端 Redis
        'BACKEND': 'django_redis.cache.RedisCache',
        # 连接Redis数据库(服务器地址)
        # 一主带多从(可以配置多个Redis，写走第一台，读走其他的机器)
        'LOCATION': [
            f'{REDIS_URL}/0',
        ],
        # 项目名当做文件前缀
        'KEY_PREFIX': 'yyclb',
        'OPTIONS': {
            # 连接选项(默认，不改)
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                # 连接池的连接(最大连接)
                'max_connections': 512,
            },
        }
    },
    # 缓存session
    'session': {
        # 缓存后端 Redis
        'BACKEND': 'django_redis.cache.RedisCache',
        # 连接Redis数据库(服务器地址)
        # 一主带多从(可以配置多个Redis，写走第一台，读走其他的机器)
        'LOCATION': [
            f'{REDIS_URL}/1',
        ],
        'OPTIONS': {
            # 连接选项(默认，不改)
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
    # 缓存短信验证码
    'verify_codes': {
        # 缓存后端 Redis
        'BACKEND': 'django_redis.cache.RedisCache',
        # 连接Redis数据库(服务器地址)
        # 一主带多从(可以配置多个Redis，写走第一台，读走其他的机器)
        'LOCATION': [
            f'{REDIS_URL}/2',
        ],
        'OPTIONS': {
            # 连接选项(默认，不改)
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
    # 接口安全校验（验证接口重复第二次访问会拒绝）
    "authapi": {
        # 缓存后端 Redis
        'BACKEND': 'django_redis.cache.RedisCache',
        # 连接Redis数据库(服务器地址)
        # 一主带多从(可以配置多个Redis，写走第一台，读走其他的机器)
        'LOCATION': [
            f'{REDIS_URL}/3',
        ],
        'OPTIONS': {
            # 连接选项(默认，不改)
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
    # jwt单用户登录（确保一个账户只有一个地点登录，后一个会顶掉前一个）
    "singletoken": {
        # 缓存后端 Redis
        'BACKEND': 'django_redis.cache.RedisCache',
        # 连接Redis数据库(服务器地址)
        # 一主带多从(可以配置多个Redis，写走第一台，读走其他的机器)
        'LOCATION': [
            f'{REDIS_URL}/4',
        ],
        'OPTIONS': {
            # 连接选项(默认，不改)
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            # 添加这一行,防止取出的值带有b'' bytes
            'CONNECTION_POOL_KWARGS': {'decode_responses': True},
        }
    },
    # 缓存图片验证码
    'image_codes': {
        # 缓存后端 Redis
        'BACKEND': 'django_redis.cache.RedisCache',
        # 连接Redis数据库(服务器地址)
        # 一主带多从(可以配置多个Redis，写走第一台，读走其他的机器)
        'LOCATION': [
            f'{REDIS_URL}/5',
        ],
        'OPTIONS': {
            # 连接选项(默认，不改)
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
}

REDIS_TIMEOUT = 7 * 24 * 60 * 60
CUBES_REDIS_TIMEOUT = 60 * 60
NEVER_REDIS_TIMEOUT = 365 * 24 * 60 * 60

CHANNEL_LAYERS = {
    'default': {
        # 默认用内存
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    },
}

# session使用的存储方式
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# 指明使用哪一个库保存session数据
SESSION_CACHE_ALIAS = "session"

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# 设置为中国时间
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
# 设置django的静态文件目录
FRONTEND_ROOT = os.path.join(BASE_DIR, "frontend")
STATICFILES_DIRS = [
    os.path.join(FRONTEND_ROOT,"static"),
    os.path.join(FRONTEND_ROOT,"download-app","static"),
]
# 收集静态文件，必须将 MEDIA_ROOT,STATICFILES_DIRS先注释
# python manage.py collectstatic
STATIC_ROOT=os.path.join(BASE_DIR,'static')

# 访问上传文件的url地址前缀
if not os.path.exists(os.path.join(BASE_DIR, 'media')):
    os.makedirs(os.path.join(BASE_DIR, 'media'))

MEDIA_URL = "/media/"
# 项目中存储上传文件的根目录
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ================================================= #
# ******************* 跨域的配置 ******************* #
# ================================================= #
# 如果为True，则将不使用白名单，并且将接受所有来源。默认为False
# 允许跨域
CORS_ORIGIN_ALLOW_ALL = True
# 新版 ACCESS_CONTROL_ALLOW_ORIGIN = '*' ,不能与CORS_ALLOW_CREDENTIALS一起使用
CORS_ALLOW_ALL_ORIGINS = True
# 允许cookie
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'None'
# ================================================= #
# ********************* 日志配置 ******************* #
# ================================================= #
# log 配置部分BEGIN
SERVER_LOGS_FILE = os.path.join(BASE_DIR, 'logs', 'server.log')
ERROR_LOGS_FILE = os.path.join(BASE_DIR, 'logs', 'error.log')
if not os.path.exists(os.path.join(BASE_DIR, 'logs')):
    os.makedirs(os.path.join(BASE_DIR, 'logs'))
# 格式:[2020-04-22 23:33:01][micoservice.apps.ready():16] [INFO] 这是一条日志:
# 格式:[日期][模块.函数名称():行号] [级别] 信息
STANDARD_LOG_FORMAT = '[%(asctime)s][%(name)s.%(funcName)s():%(lineno)d] [%(levelname)s] %(message)s'
CONSOLE_LOG_FORMAT = '[%(asctime)s][%(name)s.%(funcName)s():%(lineno)d] [%(levelname)s] %(message)s'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': STANDARD_LOG_FORMAT
        },
        'console': {
            'format': CONSOLE_LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'file': {
            'format': CONSOLE_LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': SERVER_LOGS_FILE,
            # 10 MB
            'maxBytes': 1024 * 1024 * 10,
            # 最多备份10个
            'backupCount': 10,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': ERROR_LOGS_FILE,
            # 10 MB
            'maxBytes': 1024 * 1024 * 10,
            # 最多备份10个
            'backupCount': 10,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        }
    },
    'loggers': {
        # default日志
        '': {
            'handlers': ['console', 'error', 'file'],
            'level': 'INFO',
        },
        'django': {
            'handlers': ['console', 'error', 'file'],
            'level': 'INFO',
        },
        'scripts': {
            'handlers': ['console', 'error', 'file'],
            'level': 'INFO',
        },
        # 数据库相关日志
        'django.db.backends': {
            'handlers': [],
            'propagate': True,
            'level': 'INFO',
        },
    }
}

# ================================================= #
# *************** REST_FRAMEWORK配置 *************** #
# ================================================= #
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES':
        ( 'rest_framework.renderers.JSONRenderer', ),
}

# ====================================#
# ****************swagger************#
#====================================#
SWAGGER_SETTINGS = {
    # 基础样式
    'SECURITY_DEFINITIONS': {
        # 用户名密码cookie验证
        "basic":{
            'type': 'basic'
        },
        # 通过jwt验证
        'JWT': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        },
    },
    # 如果需要登录才能够查看接口文档, 登录的链接使用restframework自带的.
    'LOGIN_URL': 'rest_framework:login',
    'LOGOUT_URL': 'rest_framework:logout',
    'APIS_SORTER': 'alpha',
    # 如果支持json提交, 则接口文档中包含json输入框
    'JSON_EDITOR': True,
    # 方法列表字母排序
    'OPERATIONS_SORTER': 'alpha',
    'VALIDATOR_URL': None,
    # 分组根据url层级分，0、1 或 2 层
    'AUTO_SCHEMA_TYPE': 1,
    'DEFAULT_AUTO_SCHEMA_CLASS': 'utils.swagger.CustomSwaggerAutoSchema',
}

# ================================================= #
# ******************** 其他配置 ******************** #
# ================================================= #
# 全局控制日志记录
API_LOG_ENABLE = True
API_LOG_METHODS = ['POST', 'UPDATE', 'DELETE', 'PUT']
# 日志记录显示的请求模块中文名映射
API_MODEL_MAP = {
    "/api/token/": "登录模块",
}
# 设置异步SSH任务的线程池大小
ASYNCSSH_THREAD_POOL_SIZE = 10
# 结果分块的大小
CHUNK_SIZE = 20
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
