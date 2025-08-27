from ftplib import parse227
from getpass import getpass
from uuid import UUID
from neon import NeonConnection
from password_util import check_password, hash_password
from user_session import UserSession


class App:
    def __init__(self) -> None:
        self.__conn = NeonConnection()
        self.__user: None | UserSession = None

    def auth(self):
        name = input("Write user name: ")
        password = getpass("Write password: ")
        user_data = self.__conn.execute(
            """
            select user_password_hash, user_password_salt, country_id, user_id
            from users
            where user_name = %s
            """,
            (name),
        )
        if len(user_data) == 0:
            print(f"No user with a name '{name}'.")
            return
        else:
            pwd_hash, pwd_salt, country_id, user_id = user_data[0]
            if check_password(password, pwd_salt, pwd_hash):
                country_code = None
                if country_id is not None:
                    country_code = self.__conn.execute(
                        """
                            select code from countries
                            where country_id = %s
                            """,
                        (country_id),
                    )[0][0]
                self.__user = UserSession(
                    user_id, country_code=country_code, connection=self.__conn
                )
            else:
                print("Wrong password!")

    def add_user(self):
        while True:
            name = input("Write user name: ")
            name_query = self.__conn.execute(
                """
                select user_id from users
                where name = %s
                """,
                (name),
            )
            if len(name_query) == 0:
                break
            print("There already is a user with a name '{name}'")
        while True:
            password = getpass("Write your password: ")
            password2 = getpass("Write your password again: ")
            if password == password2:
                break
            print("You wrote different passwords! Try again.\n")

        pwd_hash, pwd_salt = hash_password(password)

        result = self.__conn.execute(
            """
            insert into users (user_name, user_password_hash, user_password_salt)
            values (%s, %s, %s)
            returning user_id
            """,
            (name, pwd_hash, pwd_salt),
        )
        self.__user = UserSession(result[0][0], connection=self.__conn)
