########### Python 3.7 #############
import time
import sys
import json
import http.client, urllib.request, urllib.parse, urllib.error, base64

import argparse

parser = argparse.ArgumentParser( description='Display Train Times')
parser.add_argument('-s', '--station', dest='stationOfInterest', action="store" , required=False, default='College Park-U of Md',
                    help='Station of Interest', type=str)
parser.add_argument('-r', '--run', dest='run', action="store_true" , required=False, default=False, help='Run continuously every 30 sec')

headers = {
    # Request headers
    'api_key': '475a849cbcb44f9f8a5f6e73f8532319',
}

requestString = {
    'station_info' : "/Rail.svc/json/jStations?",
    'arrival_info' : '/StationPrediction.svc/json/GetPrediction/'
}

code_dict = {}
params = urllib.parse.urlencode({
    })

line_dict = { "YL": "Yellow", "GR": "Green", "RD": "RED",
              "SL": "Silver", "BL":"Blue", "OR": "Orange"}

def webConnect( params, params2=""):
    conn = http.client.HTTPSConnection('api.wmata.com')
    conn.request("GET", requestString[ params] + params2, "{body}", headers)
    response = conn.getresponse()
    output = response.read()
    conn.close()
    return output
    
def getStationInfo( printerMode=False):
    json_dict = json.loads( webConnect( 'station_info' ))

    # Crack Open the Dictionary
    stations = json_dict['Stations']
    for ele in stations:
        if printerMode:
            print("%50s: \t%s \t%s" % (ele['Name'], ele['Code'], ele['LineCode1']))
        code_dict[ ele['Name']] = ele['Code']
    
def getArrivalInfo( code="all"):
    json_dict = json.loads( webConnect( 'arrival_info', code))
    trains = json_dict['Trains']
    output = []
    print("%20s \t%s \t%s \t%s" % ('Destination', 'Cars', 'Line', 'Min'))
    for ele in trains:
        print("%20s: \t%s \t%s \t%s" % (ele['Destination'], ele['Car'], ele['Line'], ele['Min']))
        if "BRD" in ele['Min'] or "ARR" in ele['Min']:
            # if "Branch Avenue" in ele['Destination'] or "Greenbelt" in ele['Destination'] or "Huntington" in ele['Destination']:
            output.append( ele)
    return output
        
def main():
    args = parser.parse_args()
    flag = True
    while flag or args.run:
        flag = False
        print( time.asctime( time.localtime()))
        getStationInfo()
        # station = 'College Park-U of Md'
        station = args.stationOfInterest
        output = getArrivalInfo( code_dict[station])
        print('Info for station: %s'%( station))
        if not output:
            print( "No trains arriving or boarding :(")
        else:
            for ele in output:
                if "BRD" in ele['Min']:
                    print( "The %s line train to %s is now boarding..."%( line_dict[ ele['Line']], ele['Destination']))
                elif "ARR" in ele['Min']:
                    print( "The %s line train to %s is now arriving..."%( line_dict[ ele['Line']], ele['Destination']))
                else:
                    print( "Something rotten in the state of Denmark...")
        if args.run:
            time.sleep(30)
    
if __name__ == "__main__":
    try:
        main()
    except OSError as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    except KeyboardInterrupt as e:
        print("You've interrupted me :(")
