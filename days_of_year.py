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

    if year < 0:
        raise ValueError("Inapproperiate year value.")

    if month not in Month_days.keys():
        raise KeyError("Inapproperiate month value.")

    if day not in range(1, Month_days[month]+1):
        raise ValueError("Inapproperiate day value.")

    #Condition for the years that have a 29th day in February.
    if year % 4 == 0:
        Month_days[2] = 29

    #The code that 
    number_of_days_passed = 0
    for k, v in Month_days.items():
        if k < month:
            number_of_days_passed = number_of_days_passed + v
        elif k == month:
            number_of_days_passed = number_of_days_passed + day
            print(number_of_days_passed)
            return number_of_days_passed
            break


# day_number(-200,3,2)                  # Checking the ValueError being raised as per line 19
# day_number(2024, "jan", 2)            # Checking the KeyError being raised as per line 22
# day_number(2021,80,2)                 # Checking the KeyError being raised as per line 22
# day_number(2021,3,200)                # Checking the ValueError being raised as per line 25
# day_number(2024,3,1)                  # Checking the inclusion of Feb 29
# day_number(2021,3,1)                  # Checking the exclusion of Feb 29




