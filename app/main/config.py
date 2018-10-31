class Config:
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass


config_by_name = dict(dev=DevelopmentConfig, prod=ProductionConfig)
