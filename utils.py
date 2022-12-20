from datetime import datetime
import calendar
 
def findDay():
    date = datetime.today().strftime('%d %m %Y')
    born = datetime.strptime(date, '%d %m %Y').weekday()
    return (calendar.day_name[born])
