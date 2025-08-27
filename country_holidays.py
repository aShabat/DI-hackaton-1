import requests
from my_env import API_KEY


def country_holidays(country_code: str, year: int, month: int, day: int):

    url = f"https://holidays.abstractapi.com/v1/?api_key={API_KEY}&country={country_code}&year={year}&month={month}&day={day}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 5:
        print("Run this module with 4 parameters: counry_code, year, month, day.")
    else:
        print(
            country_holidays(
                sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
            )
        )
