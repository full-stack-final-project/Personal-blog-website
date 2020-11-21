import os

root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig(object):

    pass

class DevelopmentConfig(BaseConfig):
    pass

class TestConfig(BaseConfig):

    pass

class ProductionConfig(BaseConfig):
    pass




config = {
    'development': DevelopmentConfig
    'test': TestConfig
    'production': ProductionConfig
}