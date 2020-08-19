"""Python Library for the Quickbase API

For information about the API, please
see http://www.quickbase.com/api-guide/index.html
"""

import requests
import xmltodict
import six
from xml.etree import ElementTree as et
requests.packages.urllib3.disable_warnings()


class AuthenticateError(Exception):
    pass


class ResponseError(Exception):
    pass


class QBRequest():
    def __init__(self, request=None, ticket=None, user_token=None, encoding="UTF-8"):
        self.request = request
        if ticket:
            self.request["ticket"] = ticket
        elif user_token:
            self.request["usertoken"] = user_token
        self.request["encoding"] = encoding
        self.body = ""

    def tostring(self):
        self.body = self.__format_request(self.request)
        return self.body

    def __format_request(self, request=None):
        body = et.Element('qdbapi')
        for f, v in six.iteritems(request):
            self.__add_element(body, f, v)
        return et.tostring(body)

    def __add_element(self, body, f, v):
        # 'fieldname': 'value'
        if isinstance(v, six.string_types):
            e = et.SubElement(body, f)
            e.text = v

        # Change ints to strings
        if isinstance(v, int):
            e = et.SubElement(body, f)
            e.text = str(v)

        # 'fieldname': ['a','b','c']
        # 'fieldname': [('a', {'attr1': 'v1'})]
        if isinstance(v, list):
            for e in v:
                self.__add_element(body, f, e)

        # ('a', {'attr1': 'v1'})
        if isinstance(v, tuple):
            e = et.SubElement(body, f, attrib=v[1])
            e.text = str(v[0])


class Client():
    def __init__(self, url="http://www.quickbase.com", database=None,
                 proxy=None, user_token=None, session=None):
        """Creates a client and authenticate to the URL/db"""
        self.user_token = user_token
        self.url = url
        self.database = database
        self.ticket = None
        self.session = session or requests.Session()
        if proxy:
            self.proxy = {
                'http': proxy,
                'https': proxy
            }
        else:
            self.proxy = None

    def authenticate(self, username, password):
        req = {"username": username, "password": password}
        res = self.__request("Authenticate", request=req)
        self.ticket = res.find("ticket").text
        if not self.ticket:
            raise AuthenticateError("Failed to authenticate")

    def __request(self, action=None, db="main", request=None):
        headers = {
            "Content-Type": "application/xml",
            "Accept-Charset": "utf-8",
            "QUICKBASE-ACTION": "API_" + action
        }
        url = self.url + "/db/" + db
        if self.ticket:
            request = QBRequest(request, ticket=self.ticket)
        elif self.user_token:
            request = QBRequest(request, user_token=self.user_token)
        else:
            request = QBRequest(request)
        res = self.__make_req(url, headers, request)
        parsed = et.XML(res.text)

        # check errcode
        errcode = parsed.find('errcode')
        if errcode is None:
            raise ResponseError('Could not find errcode')
        errcode = int(errcode.text)
        if errcode != 0:
            errtext = parsed.find('errtext').text
            raise ResponseError('Received err #{0} : {1}'.format(errcode, errtext))
        return parsed

    def __make_req(self, url=None, headers=None, request=None):
        res = self.session.post(url, headers=headers, data=request.tostring(), proxies=self.proxy)
        return res

    def doquery(self, query=None, qid=None, qname=None, database=None,
                fields=None, fmt=False, rids=False, sort_fields=None, options=False, fids=False):
        req = {}
        if query is not None:
            req["query"] = query
        elif qid is not None:
            req["qid"] = str(qid)
        elif qname is not None:
            req["qname"] = qname

        if database is None:
            database = self.database

        if fields is not None:
            fids = [str(x) for x in fields]
            req["clist"] = ".".join(fids)
        else:
            req["clist"] = "a"

        if fmt:
            req["fmt"] = "structured"

        if rids:
            req["includeRids"] = 1

        if sort_fields is not None:
            sids = [str(x) for x in sort_fields]
            req["slist"] = ".".join(sids)

        if options:
            req["options"] = options
            
        if fids:
            req["useFids"] = 1
            
        res = self.__request('DoQuery', database, req)
        return xmltodict.parse(et.tostring(res))['qdbapi']

    def editrecord(self, rid=None, database=None, fields=None, update_id=None, ms_in_utc=False):
        req = {
            "msInUTC": ms_in_utc
        }
        if database is None:
            database = self.database

        if update_id is not None:
            req["update_id"] = update_id

        if rid is None:
            raise ResponseError("You must specify a record id to edit")
        req["rid"] = rid

        f = []
        for k, v in six.iteritems(fields):
            k = str(k)
            try:
                int(k)
                f.append((v, {"fid": k}))
            except ValueError:
                k = k.replace(" ", "_")
                f.append((v, {"name": k}))
        req["field"] = f
        res = self.__request('EditRecord', database, req)
        return xmltodict.parse(et.tostring(res))['qdbapi']

    def addrecord(self, database=None, fields=None, ms_in_utc=False):
        req = {
            "msInUTC": ms_in_utc
        }
        if database is None:
            database = self.database

        f = []
        for k, v in six.iteritems(fields):
            try:
                int(k)
                f.append((v, {"fid": k}))
            except ValueError:
                f.append((v, {"name": k}))
        req["field"] = f
        res = self.__request('AddRecord', database, req)
        return xmltodict.parse(et.tostring(res))['qdbapi']

    def getnumrecords(self, database=None):
        if database is None:
            database = self.database
        res = self.__request('GetNumRecords', database, {})
        return res.find('num_records').text

    def doquerycount(self, query=None, database=None):
        req = {}
        if database is None:
            database = self.database

        if query is not None:
            req["query"] = query

        res = self.__request('DoQueryCount', database, req)
        return res.find('numMatches').text

    def deleterecord(self, rid=None, database=None):
        req = {}
        if database is None:
            database = self.database

        if rid is None:
            raise ResponseError("You must specify a record id to delete")
        req["rid"] = rid

        res = self.__request('DeleteRecord', database, req)
        return xmltodict.parse(et.tostring(res))['qdbapi']

    # Delete multiple records based on a queryid or table
    def purgerecords(self, query=None, qid=None, database=None):
        req = {}
        if database is None:
            database = self.database

        if query is not None:
            req["query"] = query
        elif qid is not None:
            req["qid"] = str(qid)

        if query is None and qid is None:
            raise ResponseError("You must specify a query or qid to delete")

        res = self.__request('PurgeRecords', database, req)
        return xmltodict.parse(et.tostring(res))['qdbapi']

    def importfromcsv(self, recordscsv=None, database=None, clist=None, skipfirst=None, decimalpercent=None, mergeFieldId=None):
        req = {}
        if database is None:
            database = self.database

        if recordscsv is None:
            raise ResponseError("You must specify a records csv to import")
        req["records_csv"] = recordscsv

        if clist is not None:
            req["clist"] = clist

        if skipfirst is True:
            req["skipfirst"] = 1
            
        if mergeFieldId is not None:
            req["mergeFieldId"] = mergeFieldId

        if decimalpercent is True:
            req["decimalPercent"] = 1

        res = self.__request('ImportFromCSV', database, req)
        return xmltodict.parse(et.tostring(res))['qdbapi']

    def purge_records(self, query=None, qid=None, qname=None, database=None):
        req = {}
        if query is not None:
            req["query"] = query
        elif qid is not None:
            req["qid"] = str(qid)
        elif qname is not None:
            req["qname"] = qname

        if database is None:
            database = self.database

        res = self.__request('PurgeRecords', database, req)
        return xmltodict.parse(et.tostring(res))['qdbapi']

    def get_schema(self, database=None):
        req = {}
        if database is None:
            database = self.database

        res = self.__request('GetSchema', database, req)
        return xmltodict.parse(et.tostring(res))['qdbapi']

    def granted_dbs(self):
        req = {}

        res = self.__request('GrantedDBs', 'main', req)
        return xmltodict.parse(et.tostring(res))['qdbapi']
