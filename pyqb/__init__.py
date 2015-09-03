"""Python Library for the Quickbase API

For information about the API, please
see http://www.quickbase.com/api-guide/index.html
"""

import requests
import xmltodict
from xml.etree import ElementTree as et

class ResponseError(Exception):
    pass

class Client():

    def __init__(self, username=None, password=None, url="http://www.quickbase.com", database=None):
        """Creates a client and authenticate to the URL/db"""
        self.username = username
        self.password = password
        self.url = url
        self.database = database
        self.ticket = None
        self.__authenticate()

        if self.ticket is None:
            raise AuthenticateError("Failed to authenticate")

    def __authenticate(self):
        req = {"username": self.username, "password": self.password}
        res = self.__request("Authenticate", "main", req)
        self.ticket = res.find("ticket").text

    def __request(self, action=None, db="main", req=None):
        if self.ticket:
            req["ticket"] = self.ticket
        else:
            if action != "Authenticate":
                raise AuthenticateError("You must authenticate first")
        headers = {
                "Content-Type": "application/xml",
                "Accept-Charset": "utf-8",
                "QUICKBASE-ACTION": "API_" + action
        }

        url = self.url + "/db/" + db
        req["encoding"] = "UTF-8"
        res = self.__make_req(url, headers, req)
        parsed = et.XML(res.text)

        # check errcode
        errcode = parsed.find('errcode')
        if errcode is None:
            raise RequestError('Could not find errcode')
        errcode = int(errcode.text)
        if errcode != 0:
            errtext = parsed.find('errtext').text
            raise ResponseError('Received err #{0} : {1}'.format(errcode, errtext))
        return parsed

    def __format_req(self, req=None):
        body = et.Element('qdbapi')
        for f, v in req.iteritems():
            self.__add_element(body, f, v)
        return et.tostring(body)

    def __add_element(self, body, fname, val):
        #print "field: {0}, val: {1}, type: {2}".format(fname, val, type(val))
        if isinstance(val, basestring):
            e = et.SubElement(body, fname)
            e.text = val
        elif isinstance(val, list):
            for i in val:
               __add_element(body, fname, i)
        elif isinstance(val, dict):
            if val.has_key('attrib'):
                attrib = val['attrib']

            if isinstance(val['value'], list):
                for f in val['value']:
                   __add_element(body, fname, {'attrib': attrib, 'value': f})
            else:
                e = et.SubElement(body, fname, attrib=attrib)
                if isinstance(val['value'], basestring):
                    e.text = val['value']
                elif isinstance(val['value'], dict):
                    for f, v in val['value'].iteritems():
                       __add_element(e, f, v)

    def __make_req(self, url=None, headers=None, req=None):
        body = self.__format_req(req)
        res = requests.post(url, headers=headers, data=body)
        return res

    def doquery(self, query=None, qid=None, qname=None, database=None, fields=None, fmt=False, rids=False):
        request = {}
        if query is not None:
            request["query"] = query
        elif qid is not None:
            request["qid"] = str(qid)
        elif qname is not None:
            request["qname"] = qname

        if database is None:
            database = self.database

        if fields is not None:
            request["clist"] = fields.join(".")
        else:
            request["clist"] = "a"

        if fmt:
            request["fmt"] = "structured"

        if rids:
            request["includeRids"] = 1
        res = self.__request('DoQuery', database, request)
        return xmltodict.parse(et.tostring(res))

    def getnumrecords(self, database=None):
        if database is None:
            database = self.database
        res = self.__request('GetNumRecords', database, {})
        return res.find('num_records').text
