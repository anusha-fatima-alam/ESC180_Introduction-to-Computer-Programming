"""The Credit Card Simulator starter code
You should complete every incomplete function,
and add more functions and variables as needed.
Ad comments as required.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author: Michael Guerzhoy.  Last modified: Oct. 3, 2022
"""

# You should modify initialize()
def initialize():
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2

    cur_balance_owing_intst = 0
    cur_balance_owing_recent = 0

    last_update_day, last_update_month = -1, -1

    last_country = None
    last_country2 = None

    MONTHLY_INTEREST_RATE = 0.05

def date_same_or_later(day1, month1, day2, month2):
    if month1 == month2 and day1 >= day2:
        return True
    elif month1 >= month2:
        return True
    else:
        return False

def all_three_different(c1, c2, c3):
    if c1 != c3 and c2 != c3 and c1!=c2:
        return True

def purchase(amount, day, month, country):
    global date_same_or_later
    global all_three_different
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2
    global last_purchase

    # Return "error" if a purchase is made on a future date
    if date_same_or_later(day, month, last_update_day, last_update_month) == False:
        return "error"
    # Return "Disabled" if a purchase has been made in three different countries
    elif all_three_different(country, last_country, last_country2) == True:
        last_country2 = last_country
        last_country = country
        return "error"
    # For a valid purchase, update the last month and day and country
    # Return the recent current balance with the new amount purchased
    else:
        cur_balance_owing_recent += amount
        last_update_month = month
        last_update_day = day
        last_country2 = last_country
        last_country = country
        return cur_balance_owing_recent

def amount_owed(day, month):
    global date_same_or_later
    global all_three_different
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2

    #For any amount that is already accruing interest
    cur_balance_owing_intst *= 1.05**(month-last_update_month)

    # Return "error" if the amount owed is dated before the last updated date. This error
    # results from requesting the amount payable before your last updated date.
    if date_same_or_later(day, month, last_update_day, last_update_month) == False:
        return "error"
    # Return the sum of the balance that is acruing interest and that is not acruing
    # interest.
    elif month > (last_update_month+1):
        month_gap = month - last_update_month-1
        cur_balance_owing_recent *=1.05**(month_gap)
        cur_balance_owing_intst += cur_balance_owing_recent
        cur_balance_owing_recent = 0
        return cur_balance_owing_recent + cur_balance_owing_intst
    else:
        return cur_balance_owing_recent + cur_balance_owing_intst

def pay_bill(amount, day, month):
    global date_same_or_later
    global all_three_different
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2

    if date_same_or_later(day, month, last_update_day, last_update_month) == False:
        return "error"
    else:
        if cur_balance_owing_intst > 0:
            # Subtract amount from amount acruing interest first followed by the amount
            # not acruing interest.
            if amount > cur_balance_owing_intst:
                cur_balance_owing_recent = cur_balance_owing_recent + cur_balance_owing_intst - amount
                return cur_balance_owing_recent
            else:
                cur_balance_owing_intst = cur_balance_owing_intst - amount
                return cur_balance_owing_recent + cur_balance_owing_recent
        else:
            cur_balance_owing_recent -= amount
            return cur_balance_owing_recent


# Initialize all global variables outside the main block.
initialize()

if __name__ == '__main__':
    # Describe your testing strategy and implement it below.
    # What you see here is just the simulation from the handout, which
    # doesn't work yet.
    initialize()
    purchase(80, 8, 1, "Canada")
    print("Now owing:", amount_owed(8, 1))      # 80.0                              (Test1)
    pay_bill(50, 2, 2)
    print("Now owing:", amount_owed(2, 2))      # 30.0     (=80-50)                 (Test2)
    print("Now owing:", amount_owed(6, 3))      # 31.5     (=30*1.05)               (Test3)
    purchase(40, 6, 3, "Canada")
    print("Now owing:", amount_owed(6, 3))      # 71.5     (=31.5+40)               (Test4)
    pay_bill(30, 7, 3)
    print("Now owing:", amount_owed(7, 3))      # 41.5     (=71.5-30)               (Test5)
    print("Now owing:", amount_owed(1, 5))      # 43.65375 (=1.5*1.05*1.05+40*1.05) (Test6)
    purchase(40, 2, 5, "France")
    print("Now owing:", amount_owed(2, 5))      # 83.65375                          (Test7)
    print(purchase(50, 3, 5, "United States"))  # error    (3 diff. countries in    (Test8)
                                                #          a row)

    print("Now owing:", amount_owed(3, 5))      # 83.65375 (no change, purchase     (Test9)
                                                #           declined)
    print(purchase(150, 3, 5, "Canada"))        # error    (card disabled)          (Test10)
    print("Now owing:", amount_owed(1, 6))      # 85.8364375                        (Test11)
                                                # (43.65375*1.05+40)


