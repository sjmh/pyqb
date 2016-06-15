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
  # def Client(username=None, password=None, url="http://www.quickbase.com", database=None):
  qbc = pyqb.Client(username='myusername', password='mypassword')

**DoQuery**

.. code-block:: python

  # doquery(query=None, qid=None, qname=None, database=None, fields=None, fmt=False, rids=False):
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

API Support
+++++++++++++
- DoQuery
- EditRecod
- GetNumRecords
- AddField

Authors
+++++++++++++
Steven Hajducko (steven_hajducko@intuit.com)
