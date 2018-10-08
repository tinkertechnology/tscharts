'''
unit tests for clinic station application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json

from service.serviceapi import ServiceAPI
from test.tscharts.tscharts import Login, Logout

def setUp():
    login = Login(host, port, username, password)
    ret = login.send(timeout=30)
    if ret[0] == 200:
        global token
        token = ret[1]["token"]

class GetClinicStation(ServiceAPI):
    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/clinicstation/{}/".format(self._id)
        else:
            base = "tscharts/v1/clinicstation/"

        if not self._clinic == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "clinic={}".format(self._clinic)
            hasQArgs = True

        if not self._active == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "active={}".format(self._active)
            hasQArgs = True

        if not self._level == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "level={}".format(self._level)
            hasQArgs = True

        if not self._away == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "away={}".format(self._away)
            hasQArgs = True

        if not self._finished == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "finished={}".format(self._finished)
            hasQArgs = True

        self.setURL(base)

    def __init__(self, host, port, token, id=None):
        super(GetClinicStation, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._id = None
        self._away = None
        self._active = None
        self._finished = None
        self._level = None
        self._clinic = None
        self.makeURL();

    def setId(self, id):
        self._id = id;
        self.makeURL()

    def setAway(self, away):
        self._away = away
        self.makeURL()

    def setFinished(self, finished):
        self._finished = finished
        self.makeURL()

    def setActive(self, active):
        self._active = active
        self.makeURL()

    def setClinic(self, clinic):
        self._clinic = clinic
        self.makeURL()

    def setLevel(self, level):
        self._level = level
        self.makeURL()

def getAllClinicStations(clinicid):
    x = GetClinicStation(host, port, token)
    x.setClinic(clinicid)
    ret = x.send(timeout=30)
    if ret[0] == 200:
        stations = ret[1]       
        for x in stations:
            print("clinic {} station id {} id {} name {}".format(clinicid, x["station"], x["id"], x["name"]))
    else:
        print("Error getting all clinic stations for clinic id {}: {}".format(clinicid, ret[0]))   

def getClinicStation(clinicid, id):
    x = GetClinicStation(host, port, token)
    x.setClinic(clinicid)
    x.setId(id)
    ret = x.send(timeout=30)
    if ret[0] == 200:
        station = ret[1]       
        print("clinic {} station id {} id {} name {}".format(clinicid, station["station"], station["id"], station["name"]))
        print("clinic {} station id {} name {}".format(clinicid, station["id"], station["name"]))
    else:
        print("Error getting clinic station {} for clinic id {}: {}".format(id, clinicid, ret[0]))   

def usage():
    print("clinicstations [-h host] [-p port] [-u username] [-w password] [-c clinic] [-i id]") 

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:u:w:i:c:")
    except getopt.GetoptError as err:
        print str(err) 
        usage()
        sys.exit(2)
    global host
    host = "127.0.0.1"
    global port
    port = 8000
    global username
    username = None
    global password
    password = None
    clinic = None
    id = None
    for o, a in opts:
        if o == "-h":
            host = a
        elif o == "-p":
            port = int(a)
        elif o == "-u":
            username = a
        elif o == "-w":
            password = a
        elif o == "-c":
            clinic = int(a)
        elif o == "-i":
            id = int(a)
        else:   
            assert False, "unhandled option"
    if clinic == None:
        print("clinic required")
        usage();
    setUp()
    if id == None:
        getAllClinicStations(clinic)
    else:
        getClinicStation(clinic, id)
if __name__ == "__main__":
    main()
