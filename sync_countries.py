from neon import NeonConnection
from os import path

conn = NeonConnection()
for line in open(path.join(path.dirname(__file__), "extra", "countries.txt"), "r"):
    country, country_code = line.strip().split("\t")
    print(
        conn.execute(
            "insert into countries (name, code) values (%s, %s) returning *;",
            (country, country_code),
        )
    )
    print("-----------------------")
