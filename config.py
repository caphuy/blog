import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1234@localhost/test"
OAUTH_CREDENTIALS = {
    'facebook': {
        'id': '2311401049076307',
        'secret': 'f463899db6d477a7d793f583a34cf1de'
    },
    'google': {
        'id': '892590606738-m79jujo2kos1n1qnbojjf815ah4qadav.apps.googleusercontent.com',
        'secret': 'D-7mvS-hU_91fZC3r5nc_uyT'
    }
}