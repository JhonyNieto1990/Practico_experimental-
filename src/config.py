class Config:
    SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^'


class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '2017Ldumb' 
    MYSQL_DB = 'crunch_house_db'
    MYSQL_PORT = 3307


config = {
    'development': DevelopmentConfig
}