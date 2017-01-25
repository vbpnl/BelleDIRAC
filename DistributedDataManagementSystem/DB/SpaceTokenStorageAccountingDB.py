#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import time
import threading
import copy
from DIRAC import gConfig, gLogger, S_OK, S_ERROR
from DIRAC.Core.Base.DB import DB
from types import IntType, LongType, StringTypes, StringType, ListType, \
    TupleType, DictType


class SpaceTokenStorageAccountingDB(DB):

    def __init__(self):
        DB.__init__(self, 'SpaceTokenStorageAccountingDB', 'DistributedDataManagement/SpaceTokenStorageAccountingDB', 10)
        retVal = self.__initializeDB()
        if not retVal['OK']:
            raise Exception("Can't create tables: %s" % retVal['Message'])
        #self.lock = threading.Lock()

    def __initializeDB(self):
        """
    Create the tables
    """

        retVal = self._query('show tables')
        if not retVal['OK']:
            return retVal

        tablesInDB = [t[0] for t in retVal['Value']]
        tablesD = {}

        if 'StorageElementSpaceToken' not in tablesInDB:
            tablesD['StorageElementSpaceToken'] = {'Fields': {
                'Id': 'INTEGER NOT NULL AUTO_INCREMENT',
                'StorageElement': 'VARCHAR(128) NOT NULL',
                'SpaceToken': 'VARCHAR(128) NOT NULL',
                #'TotalSize': 'INTEGER NOT NULL',
                'GuaranteedSizeBYTE': 'BIGINT UNSIGNED NOT NULL',
                'UnusedSizeBYTE': 'BIGINT UNSIGNED NOT NULL',
                #'AssignedLifetime': 'INTEGER NOT NULL',
                #'LeftLifetime': 'INTEGER NOT NULL',
                #'RetentionPolicy': 'VARCHAR(64) NOT NULL',
                #'AccessLatency': 'VARCHAR(64) NOT NULL',
                'UpdateTime': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
                }, 'PrimaryKey': ['Id']}

        return self._createTables(tablesD)

    def addStorageElementSpaceTokenInfo(
        self,
        se,
        space_token,
        #total_size,
        guaranteed_size,
        unused_size,
        #assigned_lifetime,
        #left_lifetime,
        #retention_policy,
        #access_latency,
        connection=False,
        ):
        print 'Adding storage accounting space token information...'
        result = self.insertFields( 'StorageElementSpaceToken', [ 'StorageElement', 'SpaceToken', 'GuaranteedSizeBYTE', 'UnusedSizeBYTE' ], [ se, space_token, guaranteed_size, unused_size ], connection )

        return result

    def getAvailableStorage(self, storage_element, connection=False ):
      query = "SELECT UnusedSizeBYTE FROM StorageElementSpaceToken WHERE StorageElement='%s' ORDER BY id DESC LIMIT 1" %  storage_element
      result = self._query(query, connection) 
      values = result['Value']
      if not values:
      	return S_ERROR('No values returned.')
      return S_OK( values )

    def getPledgedStorage(self, storage_element, connection=False ):
      query = "SELECT GuaranteedSizeBYTE FROM StorageElementSpaceToken WHERE StorageElement='%s' ORDER BY id DESC LIMIT 1" %  storage_element
      result = self._query(query, connection) 
      values = result['Value']
      if not values:
        return S_ERROR('No values returned.')
      return S_OK( values )
