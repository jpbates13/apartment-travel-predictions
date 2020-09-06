import requests
import json
import datetime
import dateutil.parser
from dateutil.relativedelta import relativedelta
import pytz

from flask import Flask
from flask import render_template, request
app = Flask(__name__)

eastern = pytz.timezone('US/Eastern')
f = open("API_KEY.txt")
API_KEY = f.read()
monatiquotApiCall = "https://api-v3.mbta.com/predictions?filter[stop]=3863&filter[direction_id]=0&include=stop&api_key=" + API_KEY
westStreetApiCall = "https://api-v3.mbta.com/predictions?filter[stop]=3935&filter[direction_id]=1&include=stop&api_key=" + API_KEY


@app.route("/")
def main():
    monatiquotResp = requests.get(monatiquotApiCall)
    westStreetResp = requests.get(westStreetApiCall)
    if('data' in monatiquotResp.json() and 'included' in monatiquotResp.json()):
        monatiquot = monatiquotResp.json()['data']
        monatiquotIncl = monatiquotResp.json()['included']
        monatiquotSuccess = True
    else:
        monatiquotSuccess = False
    if('data' in westStreetResp.json() and 'included' in westStreetResp.json()):
        westStreet = westStreetResp.json()['data']
        westStreetIncl = westStreetResp.json()['included']
        westStreetSuccess = True
    else:
        westStreetSuccess = False
    monatiquotStr = ""
    westStreetStr = ""
    if monatiquotSuccess:
        monatiquotName = monatiquotResp.json(
        )['included'][0]['attributes']['name']
        monatiquotStr = constructString(monatiquot, monatiquotIncl)
    else:
        monatiquotName = "Invalid API Response (Probably no busses coming for a while)"
    if westStreetSuccess:
        westStreetName = westStreetResp.json(
        )['included'][0]['attributes']['name']
        westStreetStr = constructString(westStreet, westStreetIncl)
    else:
        westStreetName = "Invalid API Response (Probably no busses coming for a while)"

    print(monatiquotStr)
    print(westStreetStr)
    return render_template('index.html', monatiquotStr=monatiquotStr, westStreetStr=westStreetStr, monatiquotName=monatiquotName, westStreetName=westStreetName)


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, threaded=True, debug=True)
