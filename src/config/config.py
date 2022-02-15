class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SECRET_KEY = 'wxyy'
    username = 'root'
    password = '75ZuW#mY'
    database = 'yanyan-pro'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@sh-cynosdbmysql-grp-l6mgd8ra.sql.tencentcdb.com:27501/%s?charset=utf8mb4' % (username, password, database)
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WTF_CSRF_ENABLED = False
    UPLOAD_PATH = 'D:\\software\\website\\static\\moment-mobile\\'  # pro 根
    UPLOAD_MOMENT_MOBILE_PATH = 'D:\\software\\program\\BaiduNetdiskWorkspace\\static-pro\\moment' # moment-mobile pro
    UPLOAD_ARTICLE_PATH = 'D:\\software\\program\\BaiduNetdiskWorkspace\\static-pro\\article' # article pro
    STATIC_PATH = 'D:\\software\\program\\BaiduNetdiskWorkspace\\static-pro'


class DevelopmentConfig(Config):
    SECRET_KEY = 'wxyy'
    username = 'root'
    password = 123456
    database = 'common_api' # test
    # database = 'common_pro'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@127.0.0.1:3306/%s?charset=utf8mb4' % (username, password, database)
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WTF_CSRF_ENABLED = False
    # UPLOAD_PATH = 'D:\\website\\commonStatic\\upload\\'  # test
    UPLOAD_PATH = 'D:\\software\\website\\static\\moment-mobile\\'  # pro 根
    UPLOAD_MOMENT_MOBILE_PATH = 'D:\\software\\program\\BaiduNetdiskWorkspace\\static-dev\\moment' # dev
    UPLOAD_ARTICLE_PATH = 'D:\\software\\program\\BaiduNetdiskWorkspace\\static-dev\\article' # article dev
    STATIC_PATH = 'D:\\software\\program\\BaiduNetdiskWorkspace\\static-dev'


# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['WTF_CSRF_ENABLED'] = False


class TestingConfig(Config):
    TESTING = True
    #    SQLALCHEMY_DATABASE_URI = <Testing DB URL>
    SQLALCHEMY_ECHO = False
