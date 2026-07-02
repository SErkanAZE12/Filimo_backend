from .base import *

DEBUG = True

# برای توسعه، می‌توانید از SQLite استفاده کنید اگر PostgreSQL ندارید
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# تنظیمات ایمیل برای توسعه
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# غیرفعال کردن امنیت در توسعه
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False