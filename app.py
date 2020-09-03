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

monatiquotApiCall = "https://api-v3.mbta.com/predictions?filter[stop]=3863&filter[direction_id]=0&include=stop"
westStreetApiCall = "https://api-v3.mbta.com/predictions?filter[stop]=3935&filter[direction_id]=1&include=stop"
monatiquotResp = requests.get(monatiquotApiCall)
westStreetResp = requests.get(westStreetApiCall)
monatiquot = monatiquotResp.json()['data']
westStreet = westStreetResp.json()['data']
monatiquotIncl = monatiquotResp.json()['included']
westStreetIncl = westStreetResp.json()['included']
monatiquotStr = ""
westStreetStr = ""


@app.route("/")
def main():
    print(monatiquotResp.status_code)
    print(westStreetResp.status_code)

    monatiquotStr = constructString(monatiquot, monatiquotIncl)
    westStreetStr = constructString(westStreet, westStreetIncl)

    print(monatiquotStr)
    print(westStreetStr)
    return render_template('index.html', monatiquotStr=monatiquotStr, westStreetStr=westStreetStr, monatiquotName=monatiquotResp.json()['included'][0]['attributes']['name'], westStreetName=westStreetResp.json()['included'][0]['attributes']['name'])


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
    cleanDateStr = str(cleanDate.hour) + ":" + str(cleanDate.minute) + \
        " (in " + str(timeUntilMinutes) + " minutes and " + \
        str(timeUntilSeconds) + " seconds)"
    return cleanDateStr


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True, debug=True)
