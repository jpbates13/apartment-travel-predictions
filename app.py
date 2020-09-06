import Stop

from flask import Flask
from flask import render_template, request
app = Flask(__name__)

monatiquotApiCall = "https://api-v3.mbta.com/predictions?filter[stop]=3863&filter[direction_id]=0&include=stop&api_key="
westStreetApiCall = "https://api-v3.mbta.com/predictions?filter[stop]=3935&filter[direction_id]=1&include=stop&api_key="


@app.route("/")
def main():
    monatiquot = Stop.Stop(monatiquotApiCall)
    westStreet = Stop.Stop(westStreetApiCall)
    return render_template('index.html', monatiquotStr=monatiquot.dataString, westStreetStr=westStreet.dataString, monatiquotName=monatiquot.name, westStreetName=westStreet.name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, threaded=True, debug=True)
