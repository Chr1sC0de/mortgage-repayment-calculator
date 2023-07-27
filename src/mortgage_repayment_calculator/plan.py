import datetime as dt


class Schedule:
    day_number: int
    days_left: int
    current_date: dt.date

    def __init__(self, start_date: dt.date, plan_years: int):
        self.start_date = start_date
        self.plan_years = plan_years
        self.end_date = dt.date(
            self.start_date.year + plan_years,
            month=self.start_date.month,
            day=self.start_date.day,
        )
        self.total_number_of_days = (self.end_date - self.start_date).days + 1

    def __iter__(self):
        self.day_number = -1
        self.days_left = self.total_number_of_days
        self.current_date = self.start_date - dt.timedelta(days=1)
        return self

    def __next__(self):
        if self.current_date + dt.timedelta(days=1) > self.end_date:
            raise StopIteration
        self.current_date += dt.timedelta(days=1)
        self.day_number += 1
        self.days_left -= 1
        return self.current_date
