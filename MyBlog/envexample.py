# coding: utf-8
# env

FRONT_BASE_URI = 'http://IP:PORT'
ALLOWED_HOSTS = ['ip']  # backend host's ip
CORS_ORIGIN_WHITELIST = (FRONT_BASE_URI,)  # front

# 用于保存上传的文件 图片等
MEDIA_URL = 'http://ip/media/'
MEDIA_ROOT = '/var/www/html/media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dbname',   # change it to real
        'USER': 'USER',  # change it to real
        'PASSWORD': 'password',  # change it to real
        'HOST': '127.0.0.1',
        'PORT': 3306
    },
}

# Social login
# change  client_id and secret to real
SOCIALACCOUNT_PROVIDERS = {'github': {
    'APP': {"client_id": "xxxxxxxxxxxxxx", "secret": "xxxxxxxxxxxxxxxxx", "key": "",
            "certificate_key": ""}}}

# 回调地址，需要和第三方上配置的回调地址一致，这里一般是前端界面的home地址'
CALLBACK_URL = FRONT_BASE_URI
