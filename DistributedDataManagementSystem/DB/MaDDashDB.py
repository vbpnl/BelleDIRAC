#! /usr/bin/python

from DIRAC  import gConfig, gLogger, S_OK, S_ERROR
from DIRAC.Core.Base.DB import DB
from DIRAC.Core.Base import Script
import datetime
import json

class MaDDashDB( DB ):

  def __init__( self ):
    

    self.fieldDict = { 'Loss': [ 'Timestamp', 'MaDDashTimestamp', 'ChannelID',
                          'Min', 'Max', 'Avg', 'StandardDeviation' ],
                  'Channel': [ 'SourceSiteName', 'DestSiteName' ] }

    DB.__init__( self, 'MaDDashDB', 'DistributedDataManagement/MaDDashDB', 10 )
    retVal = self.__createTables()
    if not retVal[ 'OK' ]:
        raise Exception( "Can't create tables: %s" % retVal[ 'Message' ] )


  def __createTables( self ):
    """
    Create the tables
    """
    retVal = self._query( "show tables" )
    if not retVal[ 'OK' ]:
      return retVal

    tablesInDB = [ t[0] for t in retVal[ 'Value' ] ]
    tablesD = {}

    if 'Loss' not in tablesInDB:
      tablesD[ 'Loss' ] = { 'Fields' : { 'Timestamp': 'TIMESTAMP NOT NULL', 'MaDDashTimestamp': 'TIMESTAMP NOT NULL', 
                                        'ChannelID' : 'INT NOT NULL', 'Min': 'DOUBLE NOT NULL',
                                        'Max': 'DOUBLE NOT NULL', 'Avg': 'DOUBLE NOT NULL',
                                        'StandardDeviation': 'DOUBLE NOT NULL'},
                                        'ForeignKeys' : { 'ChannelID': 'Channel.id'}, 
                                        'PrimaryKey' : [ 'MaDDashTimestamp', 'ChannelID' ]
                                      }

    if 'Channel' not in tablesInDB:
      tablesD['Channel'] = { 'Fields' : {'SourceSiteName': 'VARCHAR(50) NOT NULL',
                                      'DestSiteName': 'VARCHAR(50) NOT NULL',
                                      'id': 'INT NOT NULL AUTO_INCREMENT'},
                        'PrimaryKey' : [ 'id' ]
                                  }

    return self._createTables( tablesD )


  def insert( self, tableName, columnNames, values ):
    '''
    :param tableName: name of table you wish to insert into
    :type tableName: string
    :param columnNames: list of column names
    :type columnNames: list of strings
    :param values: values you wish to insert into database
    :type values: list
    '''
    
    return self.insertFields( tableName, columnNames, values)

  def channelExists( self, sourceSiteName,  destSiteName ):
    result = self.countEntries('Channel', condDict = {'SourceSiteName': sourceSiteName, 'DestSiteName': destSiteName})['Value']
    return S_OK(bool(result))
  
  def getChannelID( self, sourceSiteName, destSiteName ):
    result = self.getFields('Channel', outFields = [ 'id' ], condDict = {'SourceSiteName': sourceSiteName, 'DestSiteName': destSiteName})['Value'][0][0]
    return S_OK(int(result))

  def getChannelData( self , source=None, dest=None, timeframe='MOST_RECENT' ):
    if timeframe not in ['MOST_RECENT', 'WEEK', 'MONTH']:
      return S_ERROR('Timeframe must be one of MOST_RECENT, WEEK, MONTH')
    if source and not dest:
      return S_ERROR('Forgot to include destination site')
    if dest and not source:
      return S_ERROR('Forgot to include source site')
    numChannels = self.countEntries('Channel', condDict = { })['Value']
    #calculate datetimes for now, one week and one month, if needed
    now = datetime.datetime.now()
    one_week = now - datetime.timedelta(weeks=1)
    one_month = now - datetime.timedelta(days=31)
    channel_where = ''
    if timeframe=='MOST_RECENT':
      #return most recent timestamp,min,max,avg,sd for specific channel
      timeframe_where = ''
      if source and dest:
        limit = 'LIMIT 1'
      else:
        limit = 'LIMIT %s' % numChannels
    elif timeframe=='WEEK':
      #return timestamp,min,max,avg,sd for specific channel 
      timeframe_where = 'AND (Timestamp <= \'%s\' AND Timestamp >= \'%s\')' % (now, one_week)
      limit = ''
    elif timeframe=='MONTH':
      #return timestamp,min,max,avg,sd for specific channel 
      timeframe_where = 'AND (Timestamp <= \'%s\' AND Timestamp >= \'%s\')' % (now, one_month)
      limit = '' 
    if source is not None and dest is not None:
      #return data for specific channel
      channel_where = 'AND Channel.SourceSiteName = \'%s\' AND Channel.DestSiteName = \'%s\'' % (source, dest)
    timestampIndex = 0
    sourceIndex = 1
    destIndex = 2
    avgIndex = 3
    minIndex = 4
    maxIndex = 5
    sdIndex = 6
    cmd = 'SELECT Timestamp, Channel.SourceSiteName as source, Channel.DestSiteName as dest, Avg, Min, Max, StandardDeviation \
           FROM Loss, Channel \
           WHERE Channel.id = Loss.ChannelID %s %s \
           ORDER BY Timestamp DESC \
           %s;' % (channel_where, timeframe_where, limit) 
   
    result = self._query(cmd)['Value']
    if not result:
      return S_ERROR('Source and Dest provided not found in DB')
    if timeframe == 'MOST_RECENT' or (source is not None and dest is not None):
      #Only 1 copy of (source, dest). No need to group (source, dest) together
      l = [{'Timestamp': str(row[timestampIndex]), 'Source': row[sourceIndex],
          'Dest': row[destIndex], 'Average': row[avgIndex], 'Min': row[minIndex],
          'Max': row[maxIndex], 'StandardDeviation': row[sdIndex]} for row in result]
      return S_OK(json.dumps(l))
    else:
      #Need to group (source, dest) together
      d = {}
      for row in result:
        source = row[sourceIndex]
        dest = row[destIndex]
        if (source,dest) not in d:
          d[(source,dest)] = {}
        l = {'Timestamp': str(row[timestampIndex]),'Average': row[avgIndex], 'Min': row[minIndex],
            'Max': row[maxIndex], 'StandardDeviation': row[sdIndex]}
        d[(source,dest)].append(l)
      return S_OK(json.dumps(d))

  def getSiteNames( self ):
    cmd = 'SELECT DISTINCT SourceSiteName from Channel;'
    result = self._query(cmd)['Value']
    #returns a tuple of singleton tuples
    #convert into expected list
    l = []
    for elem in result:
      l.append(elem[0])
    return S_OK(l)

  def getFieldNames(self, tableName):
    return S_OK(self.fieldDict[tableName])
