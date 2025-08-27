from datetime import date, datetime, time
from uuid import UUID
from neon import NeonConnection


class UserSession:
    def __init__(self, user_id: UUID) -> None:
        self.__conn = NeonConnection()
        self.__id = user_id

    def check_datetime(self, time_to_check: datetime):
        day = time_to_check.date()
        time_of_day = time_to_check.time()
        events = self.__conn.execute(
            """
            select title, description, priority, event_start, event_end
            from events
            where user_id = %s
            and event_date = %s
            and (event_end >= % or event_start <= %)
            order by priority desc;
            """,
            (self.__id, day, time_of_day, time_of_day),
        )
        return events

    def check_date(self, day: date):
        events = self.__conn.execute(
            """
            select title, description, priority, event_start, event_end
            from events
            where user_id = %s
            and event_date = %s
            order by priority desc;
            """,
            (self.__id, day),
        )
        return events

    def add_event(
        self,
        day: date,
        start: time,
        end: time,
        title: str,
        description: str = "",
        priority: int = 0,
    ):
        result = self.__conn.execute(
            """
            insert into events
            (user_id, event_date, event_start, event_end, title, description, priority)
            values
            (%s, %s, %s, %s, %s, %s, %s)
            returning event_id;
            """,
            (self.__id, day, start, end, title, description, priority),
        )
        return len(result) > 0

    def remove_event(self, day: date, title: str):
        result = self.__conn.execute(
            """
            delete from events
            where user_id = %s
            and title = %s
            returning event_id;
            """,
            (day, title),
        )
        return len(result) > 0
