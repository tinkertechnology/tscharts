'''
unit tests for clinic station application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json

from service.serviceapi import ServiceAPI
from test.tscharts.tscharts import Login, Logout
from test.clinic.clinic import CreateClinic, DeleteClinic
from test.station.station import CreateStation, DeleteStation

class CreateClinicStation(ServiceAPI):
    def __init__(self, host, port, token, clinic, station, active=False, away=True, name=""):
        super(CreateClinicStation, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        payload = {"clinic": clinic, "away": away, "station": station, "active": active, "name": name}
        self.setPayload(payload)
        self.setURL("tscharts/v1/clinicstation/")
    
class GetClinicStation(ServiceAPI):
    def __init__(self, host, port, token, id=None):
        super(GetClinicStation, self).__init__()
        
        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
       
        if id:
            self.setURL("tscharts/v1/clinicstation/{}".format(id))
        else:
            self.setURL("tscharts/v1/clinicstation/")

    def setAway(self, away):
        self._payload["away"] = away
        self.setPayload(self._payload)

    def setActive(self, active):
        self._payload["active"] = active
        self.setPayload(self._payload)

    def setClinic(self, clinic):
        self._payload["clinic"] = clinic
        self.setPayload(self._payload)

    def setLevel(self, level):
        self._payload["level"] = level
        self.setPayload(self._payload)

class UpdateClinicStation(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(UpdateClinicStation, self).__init__()
        
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload)
        self.setURL("tscharts/v1/clinicstation/{}/".format(id))

    def setAway(self, away):
        self._payload["away"] = away
        self.setPayload(self._payload)

    def setActive(self, active):
        self._payload["active"] = active
        self.setPayload(self._payload)

    def setName(self, name):
        self._payload["name"] = name
        self.setPayload(self._payload)

    def setLevel(self, level):
        self._payload["level"] = level
        self.setPayload(self._payload)

    def setAwayTime(self, minutes):
        self._payload["awaytime"] = minutes
        self.setPayload(self._payload)

class DeleteClinicStation(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteClinicStation, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/clinicstation/{}/".format(id))

class TestTSClinicStation(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateClinicStation(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid = int(ret[1]["id"])

        # default active and away state 

        x = CreateClinicStation(host, port, token, clinicid, stationid, name="test1")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)  
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("station" in ret[1])
        stationId = int(ret[1]["station"])
        self.assertTrue(stationId == stationid)
        self.assertTrue("active" in ret[1])
        self.assertTrue(ret[1]["active"] == False)
        self.assertTrue("away" in ret[1])
        self.assertTrue(ret[1]["away"] == True)
        self.assertTrue("name" in ret[1])
        self.assertTrue(ret[1]["name"] == "test1")

        x = DeleteClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # explicit active state

        x = CreateClinicStation(host, port, token, clinicid, stationid, active=False, name="test2")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("station" in ret[1])
        stationId = int(ret[1]["station"])
        self.assertTrue(stationId == stationid)
        self.assertTrue("active" in ret[1])
        self.assertTrue(ret[1]["active"] == False)
        self.assertTrue("name" in ret[1])
        self.assertTrue(ret[1]["name"] == "test2")

        x = DeleteClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = CreateClinicStation(host, port, token, clinicid, stationid, active=True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("station" in ret[1])
        stationId = int(ret[1]["station"])
        self.assertTrue(stationId == stationid)
        self.assertTrue("active" in ret[1])
        self.assertTrue(ret[1]["active"] == True)
        self.assertTrue("name" in ret[1])
        self.assertTrue(ret[1]["name"] == "")

        x = DeleteClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # explicit away state

        x = CreateClinicStation(host, port, token, clinicid, stationid, away=False)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("station" in ret[1])
        stationId = int(ret[1]["station"])
        self.assertTrue(stationId == stationid)
        self.assertTrue("away" in ret[1])
        self.assertTrue(ret[1]["away"] == False)

        x = DeleteClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = CreateClinicStation(host, port, token, clinicid, stationid, away=True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        x = GetClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("clinic" in ret[1])
        clinicId = int(ret[1]["clinic"])
        self.assertTrue(clinicId == clinicid)
        self.assertTrue("station" in ret[1])
        stationId = int(ret[1]["station"])
        self.assertTrue(stationId == stationid)
        self.assertTrue("away" in ret[1])
        self.assertTrue(ret[1]["away"] == True)
        x = DeleteClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetClinicStation(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        # non-existent clinic param

        x = CreateClinicStation(host, port, token, 9999, stationid, active=True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # non-existent station param

        x = CreateClinicStation(host, port, token, clinicid, 9999, active=True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        # bogus active param

        x = CreateClinicStation(host, port, token, clinicid, stationid, active="Hello")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        # bogus away param

        x = CreateClinicStation(host, port, token, clinicid, stationid, away="Hello")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteStation(host, port, token, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testDeleteClinicStation(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid = int(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, stationid, True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        clinicstationid = int(ret[1]["id"])

        x = DeleteClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        x = GetClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = DeleteClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteStation(host, port, token, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testUpdateClinicStation(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stationid = int(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, stationid, active=True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        clinicstationid = int(ret[1]["id"])

        x = GetClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("active" in ret[1])
        self.assertTrue(ret[1]["active"] == True) 
        self.assertTrue("name" in ret[1])
        self.assertTrue(ret[1]["name"] == "") 

        x = UpdateClinicStation(host, port, token, clinicstationid)
        x.setActive(False)
        x.setAway(True)
        x.setAwayTime(15)
        x.setName("Dental 1")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("away" in ret[1])
        self.assertTrue(ret[1]["away"] == True)
        self.assertTrue("active" in ret[1])
        self.assertTrue(ret[1]["active"] == False)
        self.assertTrue("awaytime" in ret[1])
        self.assertTrue(ret[1]["awaytime"] == 15)
        self.assertTrue("name" in ret[1])
        self.assertTrue(ret[1]["name"] == "Dental 1")
        self.assertTrue("willreturn" in ret[1])

        x = UpdateClinicStation(host, port, token, clinicstationid)
        x.setActive(True)
        x.setAway(False)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("active" in ret[1])
        self.assertTrue(ret[1]["active"] == True)
        self.assertTrue(ret[1]["away"] == False)

        x = UpdateClinicStation(host, port, token, clinicstationid)
        x.setLevel(15)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("level" in ret[1])
        self.assertTrue(int(ret[1]["level"]) == 15)
        self.assertTrue(ret[1]["active"] == True)
        self.assertTrue(ret[1]["away"] == False)

        x = UpdateClinicStation(host, port, token, clinicstationid)
        x.setLevel(0)
        x.setAwayTime(23)
        x.setActive(False)
        x.setAway(True)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("level" in ret[1])
        self.assertTrue(int(ret[1]["level"]) == 0)
        self.assertTrue(ret[1]["active"] == False)
        self.assertTrue("awaytime" in ret[1])
        self.assertTrue(ret[1]["awaytime"] == 23)
        self.assertTrue("willreturn" in ret[1])
        self.assertTrue("away" in ret[1])
        self.assertTrue(ret[1]["away"] == True)

        x = DeleteClinicStation(host, port, token, clinicstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteStation(host, port, token, stationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteClinic(host, port, token, clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testGetAllClinicStations(self):
        x = CreateClinic(host, port, token, "Ensenada", "02/05/2016", "02/06/2016")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("id" in ret[1])
        clinicid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "ENT")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        entstationid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "Dental")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        dentalstationid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "Ortho")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        orthostationid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "Screening")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        screeningstationid = int(ret[1]["id"])

        x = CreateStation(host, port, token, "Speech")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        speechstationid = int(ret[1]["id"])

        ids = []
        delids = []
        x = CreateClinicStation(host, port, token, clinicid, entstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(ret[1]["id"])
        delids.append(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, dentalstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(ret[1]["id"])
        delids.append(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, orthostationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(ret[1]["id"])
        delids.append(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, screeningstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(ret[1]["id"])
        delids.append(ret[1]["id"])

        x = CreateClinicStation(host, port, token, clinicid, speechstationid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        ids.append(ret[1]["id"])
        delids.append(ret[1]["id"])

        x = GetClinicStation(host, port, token)
        x.setClinic(clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        stations = ret[1]
        self.assertTrue(len(stations) == 5)
        for x in stations:
            if x["id"] in ids:
                ids.remove(x["id"])

        if len(ids):
            self.assertTrue("failed to find all created clinicstation items {}".format(ids) == None)

        for x in delids:
            y = DeleteClinicStation(host, port, token, x)
            ret = y.send(timeout=30)
            self.assertEqual(ret[0], 200)

        x = GetClinicStation(host, port, token)
        x.setClinic(clinicid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)
        stations = ret[1]
        self.assertTrue(len(stations) == 0)

def usage():
    print("clinicstations [-h host] [-p port] [-u username] [-w password]") 

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:u:w:")
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
    for o, a in opts:
        if o == "-h":
            host = a
        elif o == "-p":
            port = int(a)
        elif o == "-u":
            username = a
        elif o == "-w":
            password = a
        else:   
            assert False, "unhandled option"
    unittest.main(argv=[sys.argv[0]])

if __name__ == "__main__":
    main()
