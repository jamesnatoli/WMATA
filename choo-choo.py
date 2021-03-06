########### Python 2.7 #############
import sys
import json
import httplib, urllib, base64

headers = {
    # Request headers
    'api_key': '475a849cbcb44f9f8a5f6e73f8532319',
}

requestString = {
    'station_info' : "/Rail.svc/json/jStations?",
    'arrival_info' : '/StationPrediction.svc/json/GetPrediction/'
}

code_dict = {}
params = urllib.urlencode({
})

def webConnect( params, params2=""):
    conn = httplib.HTTPSConnection('api.wmata.com')
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
            output.append( ele)
    return output
        
def main():
    getStationInfo()
    output = getArrivalInfo( code_dict['College Park-U of Md'])
    if not output:
        print( "No trains arriving or boarding :(")
    else:
        print( output)
    
if __name__ == "__main__":
    try:
        main()
    except OSError as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    # except Exception as e:
    #     print "Error: Info below..."
    #     print e
