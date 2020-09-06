import requests
import json
import datetime
import dateutil.parser
from dateutil.relativedelta import relativedelta
import pytz

eastern = pytz.timezone('US/Eastern')


class Stop:
    def __init__(self, apiCall):
        f = open("API_KEY.txt")
        f = open("API_KEY.txt")
        API_KEY = f.read()
        self.apiCall = apiCall + API_KEY

        response = requests.get(self.apiCall)
        if('data' in response.json() and 'included' in response.json()):
            data = response.json()['data']
            incl = response.json()['included']
            success = True
        else:
            success = False
        self.dataString = ""
        if success:
            self.name = response.json()['included'][0]['attributes']['name']
            self.dataString = constructString(data, incl)
        else:
            self.name = "No Response from API (Probably no busses coming for a bit)"


def constructString(stop, stopDetails):
    returnStr = ""
    name = stopDetails[0]['attributes']['name']
    if not stop:
        returnStr = "No busses arriving at the moment"
        return returnStr
    returnStr = "Bus arriving at "
    index = 0
    for arrivals in stop:
        if (arrivals['attributes']['arrival_time']) == None:
            continue
        if(index == 0):
            returnStr += dateCleanup(arrivals['attributes']
                                     ['arrival_time']) + " "
            index += 1
            continue
        returnStr += "and " + \
            dateCleanup(arrivals['attributes']['arrival_time']) + " "
        index += 1
    return returnStr


def dateCleanup(date):
    cleanDate = dateutil.parser.parse(date)
    today = datetime.datetime.today()
    today = eastern.localize(today)
    rd = relativedelta(cleanDate, today)
    timeUntilMinutes = rd.days * 24 * 60 + rd.hours * 60 + rd.minutes
    timeUntilSeconds = rd.seconds
    cleanMinute = str(cleanDate.minute)
    if(cleanDate.minute < 10):
        cleanMinute = "0" + str(cleanDate.minute)
    if(cleanDate.hour < 12 and cleanDate.hour != 0):
        cleanDateStr = str(cleanDate.hour) + ":" + cleanMinute + \
            "am (in " + str(timeUntilMinutes) + " minutes and " + \
            str(timeUntilSeconds) + " seconds)"
    elif cleanDate.hour == 12:
        cleanDateStr = str(cleanDate.hour) + ":" + cleanMinute + \
            "pm (in " + str(timeUntilMinutes) + " minutes and " + \
            str(timeUntilSeconds) + " seconds)"
    elif cleanDate.hour == 0:
        cleanDateStr = "12" + ":" + cleanMinute + \
            "am (in " + str(timeUntilMinutes) + " minutes and " + \
            str(timeUntilSeconds) + " seconds)"
    else:
        cleanDateStr = str(cleanDate.hour - 12) + ":" + cleanMinute + \
            "pm (in " + str(timeUntilMinutes) + " minutes and " + \
            str(timeUntilSeconds) + " seconds)"
    return cleanDateStr
