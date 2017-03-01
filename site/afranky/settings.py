DEBUG = True
TESTING = False
SECRET_KEY = 'Will_Be_replaced_With_random'
PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 30

# flask wtf settings
WTF_CSRF_ENABLED = True

# flask mongoengine settings
#     'MONGO_URI': 'mongodb://localhost:27017/afranky'
MONGODB_SETTINGS = {
    'DB': 'afranky',
    #'HOST': '127.0.0.1',
    'HOST': 'dckmongodb',
    'PORT': 27017
}

# flask mail settings
MAIL_DEFAULT_SENDER = 'noreply@yourmail.com'
MAIL_FAKE_LINK = 'True'

# project settings
PROJECT_PASSWORD_HASH_METHOD = 'pbkdf2:sha1'
PROJECT_SITE_NAME = 'Flask Example'
PROJECT_SITE_URL = 'http://127.0.0.1:18080'
PROJECT_SIGNUP_TOKEN_MAX_AGE = 60 * 60 * 24 * 7  # in seconds
PROJECT_RECOVER_PASSWORD_TOKEN_MAX_AGE = 60 * 60 * 24 * 7  # in seconds
