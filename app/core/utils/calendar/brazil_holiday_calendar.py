from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, nearest_workday
from pandas.tseries.offsets import CustomBusinessDay


class BrazilHolidayCalendar(AbstractHolidayCalendar):
    rules = [
        Holiday('Confraternização Universal', month=1, day=1, observance=nearest_workday),
        Holiday('Tiradentes', month=4, day=21, observance=nearest_workday),
        Holiday('Dia do Trabalho', month=5, day=1, observance=nearest_workday),
        Holiday('Independência do Brasil', month=9, day=7, observance=nearest_workday),
        Holiday('Nossa Senhora Aparecida', month=10, day=12, observance=nearest_workday),
        Holiday('Finados', month=11, day=2, observance=nearest_workday),
        Holiday('Proclamação da República', month=11, day=15, observance=nearest_workday),
        Holiday('Natal', month=12, day=25, observance=nearest_workday),
    ]


def get_brazil_business_day() -> CustomBusinessDay:
    return CustomBusinessDay(calendar=BrazilHolidayCalendar())
