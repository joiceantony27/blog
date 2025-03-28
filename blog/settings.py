# CSRF Settings
CSRF_TRUSTED_ORIGINS = [
    'https://djangoblog-cwhbcca7czghbcgg.canadacentral-01.azurewebsites.net',
    'http://djangoblog-cwhbcca7czghbcgg.canadacentral-01.azurewebsites.net',
    'https://www.djangoblog-cwhbcca7czghbcgg.canadacentral-01.azurewebsites.net',
    'http://www.djangoblog-cwhbcca7czghbcgg.canadacentral-01.azurewebsites.net',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
]

# Security Settings
SECURE_SSL_REDIRECT = False  # Set to False temporarily for testing
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# CSRF Additional Settings
CSRF_USE_SESSIONS = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

ALLOWED_HOSTS = [
    'djangoblog-cwhbcca7czghbcgg.canadacentral-01.azurewebsites.net',
    'www.djangoblog-cwhbcca7czghbcgg.canadacentral-01.azurewebsites.net',
    '127.0.0.1',
    'localhost',
]

# Debug settings (for troubleshooting)
DEBUG = True  # Remember to set this to False in production
CSRF_COOKIE_DOMAIN = None  # Allow all subdomains

# If you're using whitenoise for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Static files settings
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
] 