def day_number(year: int, month: int, day: int) -> int:

    Month_days = {
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
    }

    assert 0 < day <= Month_days[month] and year > 0, 'invalid day, month, or year input.'

    number_of_days_passed = 0
    if year % 4 == 0:
        Month_days[2] = 29

    for k, v in Month_days.items():
        if k < month:
            number_of_days_passed = number_of_days_passed + v
        elif k == month:
            number_of_days_passed = number_of_days_passed + day
            print(number_of_days_passed)
            break


# day_number(2024, "jan", 2)
# day_number(2024,3,1)
# day_number(2021,3,1)
# day_number(2021,80,2)
# day_number(2021,3,200)
# day_number(-200,3,2)


