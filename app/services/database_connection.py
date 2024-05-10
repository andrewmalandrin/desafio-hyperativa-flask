from sqlalchemy import create_engine, URL
from app.services.config import CONFIG


class DBConnection:
    def __init__(self) -> None:
        self.__db_name = CONFIG['database']['name']
        self.__db_host = CONFIG['database']['host']
        self.__sgbd = CONFIG['database']['sgbd']
        self.__db_driver = CONFIG['database']['driver']
        self.__sa_user = CONFIG['database']['sa_user']
        self.__sa_pwd = CONFIG['database']['sa_pwd']
        self.__db_port = CONFIG['database']['db_port']
        self.__url = URL.create(
            f"{self.__sgbd}+{self.__db_driver}",
            username=self.__sa_user,
            password=self.__sa_pwd,
            host=self.__db_host,
            port=self.__db_port,
            database=self.__db_name
        )
        self.engine = create_engine(self.__url)
