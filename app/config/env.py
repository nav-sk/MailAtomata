import os


class ENV:
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "root"
    MYSQL_DATABASE = "app_db"
    MYSQL_HOST = "localhost"
    RABBITMQ_USER = "guest"
    RABBITMQ_PASSWORD = "guest"
    RABBITMQ_HOST = "localhost"
    USER_SECRET_KEY = "secret"
    EMAIL_HOST_USER = "your_email@example.com"
    EMAIL_HOST_PASSWORD = "your_password"

    @classmethod
    def init_env(cls):
        for en_var in dir(cls):
            if en_var.isupper():
                setattr(cls, en_var, os.getenv(en_var, getattr(cls, en_var)))
