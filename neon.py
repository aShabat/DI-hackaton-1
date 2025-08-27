import psycopg2
from my_env import NEON_CONNECTION_STRING


class NeonConnection:
    def __init__(self) -> None:
        self.__connection = psycopg2.connect(NEON_CONNECTION_STRING)

    def execute(self, query, vars=None):
        cursor = self.__connection.cursor()
        cursor.execute(query, vars)
        result = cursor.fetchall()
        self.__connection.commit()
        return result


if __name__ == "__main__":
    print(NeonConnection().execute("select * from countries;"))
