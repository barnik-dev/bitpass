import datetime

def greet():
    current_date = datetime.datetime.now()
    time = int(current_date.strftime("%H"))

    if time >= 0 and time < 12:
        return "Good Morning"
    elif time >= 12 and time < 18:
        return "Good Afternoon"
    else:
        return "Good Evening"