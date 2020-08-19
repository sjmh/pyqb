pyqb
+++++++++++++

A python library for the Quickbase API.  For more information about the Quickbase API, please see http://www.quickbase.com/api-guide/index.html

Requirements
+++++++++++++
  - python 2.6+
  - xmltodict
  - requests

Installation
+++++++++++++

.. code-block:: sh

  $ pip install pyqb

Usage
+++++++++++++

**Create the client**

.. code-block:: python

  import pyqb
  # def Client(url="http://www.quickbase.com", database=None, proxy=None, user_token=None):
  qbc = pyqb.Client(url='http://my_domain.quickbase.com')
  # Below authenticate is not required if `user_token` argument is passed to pyqb.Client() above
  qbc.authenticate(username='myusername', password='mypassword')

**DoQuery**

.. code-block:: python

  # doquery(query=None, qid=None, qname=None, database=None, fields=None, fmt=False, rids=False, sort_fields=None, options=False):
  qbc.doquery(qid=64)
  qbc.doquery(query='{"6".EX."myval"}', database='asdfasdf')
  qbc.doquery(qid=64, fields=["3", "4"], fmt=True, rids=False)

**EditRecord**

.. code-block:: python

  # editrecord(rid=None, database=None, fields=None, update_id=None)
  f = { "6": "newvalue" }
  res = qbc.editrecord(rid='18081', database='asdfasdf', fields=f)

**AddRecord**

.. code-block:: python

  # def addrecord(database=None, fields=None)
  f = { "hostname": "myhost", "7": "1.2.3.4" }
  res = qbc.addrecord(database='asdfasdf', fields=f)

**DeleteRecord**

.. code-block:: python

  # deleterecord(rid=None, database=None)
  res = qbc.deleterecord(rid='18081', database='asdfasdf')

API Support
+++++++++++++
- DoQuery
- EditRecord
- GetNumRecords
- AddField
- DeleteRecord

Authors
+++++++++++++
- Steven Hajducko (steven_hajducko@intuit.com)
- George Matthew (George.Matthew@umassmed.edu)
