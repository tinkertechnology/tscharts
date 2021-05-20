#(C) Copyright Syd Logan 2021
#(C) Copyright Thousand Smiles Foundation 2021
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#
#You may obtain a copy of the License at
#http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

from rest_framework.views import APIView
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from vaccine.models import *
from clinic.models import *
from patient.models import *
from datetime import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound

from common.decorators import *

import sys
import numbers
import json

import logging
LOG = logging.getLogger("tscharts")

class VaccineView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def __init__(self):
        super(VaccineView, self).__init__()

        self._vaccNames = ["covid19", "covid19_booster", "dtap", "dt", "hib", 
                  "hepa", "hepb", "hpv", "iiv", "laiv4", "mmr", 
                  "menacwy", "menb", "pcv13", "ppsv23", "ipv", "rv", 
                  "tap", "td", "var", "dtap_hepb_ipv", "dtap_ipv_hib", 
                  "dtap_ipv", "dtap_ipv_hib_hepb", "mmvr"]

        self._vaccDates = ["covid19_date", "covid19_booster_date", "dtap_date", "dt_date", "hib_date", 
                  "hepa_date", "hepb_date", "hpv_date", "iiv_date", "laiv4_date", "mmr_date", 
                  "menacwy_date", "menb_date", "pcv13_date", "ppsv23_date", "ipv_date", "rv_date", 
                  "tap_date", "td_date", "var_date", "dtap_hepb_ipv_date", "dtap_ipv_hib_date", 
                  "dtap_ipv_date", "dtap_ipv_hib_hepb_date", "mmvr_date"]

        self._integerNames = ["covid19_doses"]

        self._integerFields = [("covid19_doses", [0, 1, 2])]

        self._otherFields = ["clinic", "patient"]

    def booleanToText(self, val):
        ret = "false"

        if val == True:
            ret = "true"

        return ret

    def textToBoolean(self, val):
        ret = False

        if val == "true":
            ret = True

        return ret

    def serialize(self, entry):
        m = {}
        m["id"] = entry.id  
        m["clinic"] = entry.clinic_id
        m["patient"] = entry.patient_id
        m["time"] = entry.time

        m["covid19"] = self.booleanToText(entry.covid19)
        m["covid19_doses"] = entry.covid19_doses 
        m["covid19_date"] = entry.covid19_date.strftime("%m/%d/%Y") 
        m["covid19_booster"] = self.booleanToText(entry.covid19_booster)
        m["covid19_booster_date"] = entry.covid19_booster_date.strftime("%m/%d/%Y") 
        m["dtap"] = self.booleanToText(entry.dtap)
        m["dtap_date"] = entry.dtap_date.strftime("%m/%d/%Y") 
        m["dt"] = self.booleanToText(entry.dt)
        m["dt_date"] = entry.dt_date.strftime("%m/%d/%Y") 
        m["hib"] = self.booleanToText(entry.hib)
        m["hib_date"] = entry.hib_date.strftime("%m/%d/%Y") 
        m["hepa"] = self.booleanToText(entry.hepa)
        m["hepa_date"] = entry.hepa_date.strftime("%m/%d/%Y") 
        m["hepb"] = self.booleanToText(entry.hepb)
        m["hepb_date"] = entry.hepb_date.strftime("%m/%d/%Y") 
        m["hpv"] = self.booleanToText(entry.hpv)
        m["hpv_date"] = entry.hpv_date.strftime("%m/%d/%Y") 
        m["iiv"] = self.booleanToText(entry.iiv)
        m["iiv_date"] = entry.iiv_date.strftime("%m/%d/%Y") 
        m["laiv4"] = self.booleanToText(entry.laiv4)
        m["laiv4_date"] = entry.laiv4_date.strftime("%m/%d/%Y") 
        m["mmr"] = self.booleanToText(entry.mmr)
        m["mmr_date"] = entry.mmr_date.strftime("%m/%d/%Y") 
        m["menacwy"] = self.booleanToText(entry.menacwy)
        m["menacwy_date"] = entry.menacwy_date.strftime("%m/%d/%Y") 
        m["menb"] = self.booleanToText(entry.menb)
        m["menb_date"] = entry.menb_date.strftime("%m/%d/%Y") 
        m["pcv13"] = self.booleanToText(entry.pcv13)
        m["pcv13_date"] = entry.pcv13_date.strftime("%m/%d/%Y") 
        m["ppsv23"] = self.booleanToText(entry.ppsv23)
        m["ppsv23_date"] = entry.ppsv23_date.strftime("%m/%d/%Y") 
        m["ipv"] = self.booleanToText(entry.ipv)
        m["ipv_date"] = entry.ipv_date.strftime("%m/%d/%Y") 
        m["rv"] = self.booleanToText(entry.rv)
        m["rv_date"] = entry.rv_date.strftime("%m/%d/%Y") 
        m["tap"] = self.booleanToText(entry.tap)
        m["tap_date"] = entry.tap_date.strftime("%m/%d/%Y") 
        m["td"] = self.booleanToText(entry.td)
        m["td_date"] = entry.td_date.strftime("%m/%d/%Y") 
        m["var"] = self.booleanToText(entry.var)
        m["var_date"] = entry.var_date.strftime("%m/%d/%Y") 
        m["dtap_hepb_ipv"] = self.booleanToText(entry.dtap_hepb_ipv)
        m["dtap_hepb_ipv_date"] = entry.dtap_hepb_ipv_date.strftime("%m/%d/%Y") 
        m["dtap_ipv_hib"] = self.booleanToText(entry.dtap_ipv_hib)
        m["dtap_ipv_hib_date"] = entry.dtap_ipv_hib_date.strftime("%m/%d/%Y") 
        m["dtap_ipv"] = self.booleanToText(entry.dtap_ipv)
        m["dtap_ipv_date"] = entry.dtap_ipv_date.strftime("%m/%d/%Y") 
        m["dtap_ipv_hib_hepb"] = self.booleanToText(entry.dtap_ipv_hib_hepb)
        m["dtap_ipv_hib_hepb_date"] = entry.dtap_ipv_hib_hepb_date.strftime("%m/%d/%Y") 
        m["mmvr"] = self.booleanToText(entry.mmvr)
        m["mmvr_date"] = entry.mmvr_date.strftime("%m/%d/%Y") 

        return m

    @log_request
    def get(self, request, vaccine_id=None, format=None):
        vaccine = None
        badRequest = False
        aPatient = None
        aClinic = None
        aStation = None
        kwargs = {}

        if vaccine_id:
            try:
                vaccine = Vaccine.objects.get(id = vaccine_id)
            except:
                vaccine = None
        else:
            # look for optional arguments
            try:
                patientid = request.GET.get('patient', '')
                if patientid != '':
                    try:
                        aPatient = Patient.objects.get(id=patientid)
                        if not aPatient:
                            badRequest = True
                        else:
                            kwargs["patient"] = aPatient
                    except:
                        badRequest = True
            except:
                pass # no patient ID

            try:
                clinicid = request.GET.get('clinic', '')
                if clinicid != '':
                    try:
                        aClinic = Clinic.objects.get(id=clinicid)
                        if not aClinic:
                            badRequest = True
                        else:
                            kwargs["clinic"] = aClinic
                    except:
                        badRequest = True
            except:
                pass # no clinic ID

            if not badRequest and len(kwargs):
                # look for invalid arg combinations

                # there are 2 legal combinations of args

                case1 = False
                case2 = False
                case3 = False

                if aPatient and aClinic:
                    case1 = True
                elif aPatient and not aClinic:
                    case2 = True
                elif aClinic and not aPatient:
                    case3 = True
                else:
                    badRequest = True

            if not badRequest:
                kwargs = {}
                if case1:
                    kwargs["patient"] = aPatient
                    kwargs["clinic"] = aClinic
                elif case2:
                    kwargs["patient"] = aPatient
                elif case3:
                    kwargs["clinic"] = aClinic
                try:
                    vaccine = Vaccine.objects.filter(**kwargs)
                except:
                    vaccine = None

        if not vaccine and not badRequest:
            raise NotFound
        elif not badRequest:
            if vaccine_id:
                ret = self.serialize(vaccine)
            elif case1 and len(vaccine) == 1:
                ret = self.serialize(vaccine[0])
            else:
                ret = []
                for x in vaccine:
                    m = self.serialize(x)
                    ret.append(m)
        if badRequest:
            return HttpResponseBadRequest()
        else:
            return Response(ret)

    def validatePostArgs(self, data):
        valid = True
        kwargs = data

        try:
            for key, val in data.iteritems():
                if not (key in self._vaccNames or key in self._vaccDates or key in self._integerNames or key in self._otherFields):
                    LOG.error("validatePostArgs invalid key {}".format(key))
                    return False, kwargs
 
            for x in self._vaccNames:
                LOG.error("validatePostArgs processing name {}".format(x))
                if not x in data:
                    LOG.error("validatePostArgs name failed on {}".format(x))
                    valid = False
                else:
                    val = data[x] 
                    if not (val == "true" or val == "false"):
                        LOG.error("validatePostArgs val failed on {}".format(val))
                        valid = False
                    else:
                        kwargs[x] = self.textToBoolean(data[x])
                dateField = "{}_date".format(x)
                if not dateField in data:
                    LOG.error("validatePostArgs datefield failed on {}".format(dateField))
                    valid = False
                else:
                    try:
                        kwargs[dateField] = datetime.strptime(data[dateField], '%m/%d/%Y')
                    except ValueError:
                        try:
                            kwargs[dateField] = datetime.strptime(data[dateField], '%m-%d-%Y')
                        except ValueError:
                            valid = False

            for x in self._integerFields:
                LOG.error("validatePostArgs processing integer {}".format(x))
                name = x[0]
                if not name in data:
                    LOG.error("validatePostArgs integer failed on name {}".format(name))
                    valid = False
                allowedValues = x[1]
                if not int(data[name]) in allowedValues:
                    LOG.error("validatePostArgs integer failed on val {}".format(int(data[name])))
                    valid = False
        except:
            LOG.error("validatePostArgs name exception")
            valid = False

        if not "patient" in data:
            LOG.error("validatePostArgs no patient")
            valid = False

        if not "clinic" in data:
            LOG.error("validatePostArgs no clinic")
            valid = False

        LOG.error("validatePostArgs return {}".format(valid))
        return valid, kwargs

    def validatePutArgs(self, data, vaccine):
        valid = True

        try:
            for key, val in data.iteritems():
                if not (key in self._vaccNames or key in self._vaccDates or key in self._integerNames or key in self._otherFields):
                    LOG.error("validatePutArgs invalid key {}".format(key))
                    return False, vaccine
 
            for x in self._vaccNames:
                if x in data:
                    val = data[x]
                    if not (val == "true" or val == "false"):
                        LOG.error("validatePutArgs {} failed {}".format(x, val))
                        valid = False
                    else:
                        setattr(vaccine, x, self.textToBoolean(val))
                dateField = "{}_date".format(x)
                if dateField in data:
                    try:
                        setattr(vaccine, dateField, datetime.strptime(data[dateField], '%m/%d/%Y'))
                    except ValueError:
                        LOG.error("validatePutArgs {} failed {}".format(dateField, data[dateField]))
                        try:
                            setattr(vaccine, dateField, datetime.strptime(data[dateField], '%m-%d-%Y'))
                        except ValueError:
                            LOG.error("validatePutArgs {} failed {}".format(dateField, data[dateField]))
                            valid = False

            for x in self._integerFields:
                name = x[0]
                allowedValues = x[1]
                if name in data:
                    val = data[name]
                    if not val in allowedValues:
                        LOG.error("validatePutArgs {} failed {}".format(name, val))
                        valid = False
                    else:
                        setattr(vaccine, name, val)
        except:
            LOG.error("validatePutArgs exception")
            valid = False

        return valid, vaccine

    @log_request
    def post(self, request, format=None):
        badRequest = False
        implError = False

        data = json.loads(request.body)
        try:
            patientid = int(data["patient"])
        except:
            badRequest = True

        try:
            clinicid = int(data["clinic"])
        except:
            badRequest = True

        # validate the post data, and get a kwargs dict for
        # creating the object 

        valid, kwargs = self.validatePostArgs(data)

        if not valid:
            badRequest = True

        if not badRequest:

            # get the instances

            try:
                aPatient = Patient.objects.get(id=patientid)
            except:
                aPatient = None
 
            try:
                aClinic = Clinic.objects.get(id=clinicid)
            except:
                aClinic = None

            if not aPatient or not aClinic:
                raise NotFound

        if not badRequest:
                
            try:
                kwargs["patient"] = aPatient
                kwargs["clinic"] = aClinic
                LOG.error("POST before create kwargs {}".format(kwargs))
                vaccine = Vaccine(**kwargs)
                LOG.error("POST after create kwargs {}".format(kwargs))
                if vaccine:
                    LOG.error("POST before save")
                    vaccine.save()
                    LOG.error("POST after save")
                else:
                    implError = True
            except Exception as e:
                implError = True
                implMsg = sys.exc_info()[0] 
                LOG.error("POST exception {}".format(implMsg))

        if badRequest:
            return HttpResponseBadRequest()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({'id': vaccine.id})

    @log_request
    def put(self, request, vaccine_id=None, format=None):
        badRequest = False
        implError = False
        notFound = False

        if not vaccine_id:
            badRequest = True

        if not badRequest:
            vaccine = None

            try:
                vaccine = Vaccine.objects.get(id=vaccine_id)
            except:
                pass

            if not vaccine:
                notFound = True 
            else:
                try:
                    data = json.loads(request.body)
                    valid, vaccine = self.validatePutArgs(data, vaccine)
                    if valid: 
                        vaccine.save()
                    else:
                        badRequest = True
                except:
                    implError = True
                    implMsg = sys.exc_info()[0] 
        if badRequest:
            return HttpResponseBadRequest()
        if notFound:
            return HttpResponseNotFound()
        if implError:
            return HttpResponseServerError(implMsg) 
        else:
            return Response({})
       
    @log_request 
    def delete(self, request, vaccine_id=None, format=None):
        vaccine = None

        # see if the state change object exists

        if not vaccine_id:
            return HttpResponseBadRequest()
        try:
            vaccine = Vaccine.objects.get(id=vaccine_id)
        except:
            vaccine = None

        if not vaccine:
            raise NotFound
        else:
            vaccine.delete()

        return Response({})