from datetime import datetime
'''
Calculates the remaining minutes until the auction ends
'''
def difference_time(time_left):
    time_delta = time_left - datetime.now()
    total_seconds = time_delta.total_seconds()
    minutes = total_seconds/60
    return minutes

'''
Checks that the remaining time of the auction is less than or equal to the time decided by the user (time_max)
'''
def validation_time(time_left, time_max):
    if (time_left - time_max) <= 0:
        return True
    else:
        return False

'''
Check if the price is less than or equal to the maximum price
'''
def validation_price(price_item, max_price):
    if price_item <= max_price:
        return True
    else:
        return False

'''
Check if the auction provides as the only method of payment the bank transfer
'''
def validation_payments(item):
    if item[4] == []:
        return False
    else:
        return True
    

'''
Check if the auction has the right requirements to be subsequently reported to the user
'''
def validation_item(item, tempo_massimo, prezzo_massimo):
    if validation_payments(item):
        tempo_rimasto = difference_time(datetime.strptime(item[1], '%d %b %Y %H:%M:%S'))
        if validation_time(tempo_rimasto, int(tempo_massimo)):
            if validation_price(item[2]+item[3], float(prezzo_massimo)):
                return True
            else:
                False
        else:
            False
    else:
        return False