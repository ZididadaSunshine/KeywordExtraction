class Config:
    ENV = 'production'
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True


class TestConfig(Config):
    ENV = 'test'
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    pass


config_by_name = dict(dev=DevelopmentConfig, test=TestConfig, prod=ProductionConfig)
