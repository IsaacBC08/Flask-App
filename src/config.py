class config:
    SECRET_KEY = 'chamba'

class DevelopmentConfig(config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'usuarios'

config = {
    'deve' : DevelopmentConfig
}