""" 
"""

__RCSID__ = "$Id: $"

import types
from DIRAC.Core.DISET.RequestHandler import RequestHandler, getServiceOption
from DIRAC import gLogger, S_OK, S_ERROR
from BelleDIRAC.DistributedDataManagementSystem.DB import MaDDashDB

class MaDDashHandler( RequestHandler ):

  @classmethod
  def initializeHandler( cls, serviceInfo ):
    """ Handler initialization
    """
    global MaDDashDB

    MaDDashDB = MaDDashDB.MaDDashDB()

    return S_OK()

  def initialize(self):
    """ Response initialization
    """
    pass
  
  types_getFieldNames = [ types.StringType ]
  def export_getFieldNames( self, tableName ):
    """ Gets a list of all field names for a specified table"""
    return MaDDashDB.getFieldNames( tableName )

  types_insert = [ types.StringType, types.ListType, types.ListType ]
  def export_insert( self, tableName, columnNames, values ):
    """ Inserts row into MaDDashDB """
    return MaDDashDB.insert(tableName, columnNames, values)

  types_channelExists = [ types.StringType, types.StringType ]
  def export_channelExists( self, sourceSiteName, destSiteName ):
    """ Checks whether channel exists in MaDDashDB """
    return MaDDashDB.channelExists(sourceSiteName, destSiteName)

  types_getChannelID = [ types.StringType, types.StringType ]
  def export_getChannelID( self, sourceSiteName, destSiteName ):
    """ Gets ChannelID for a given channel """
    return MaDDashDB.getChannelID(sourceSiteName, destSiteName)

  types_getChannelData = [ (types.NoneType, types.StringType), (types.NoneType, types.StringType), (types.StringType)]
  def export_getChannelData( self , source=None, dest=None, timeframe='MOST_RECENT'):
    """ Gets statistics for channel if provided, or all channels if not provided.
    Can retrieve most recent statistics, 1 week of statistics, or 1 month of statistics.
    Possible values for timeframe are:
    -MOST_RECENT
    -WEEK 
    -MONTH"""
    return MaDDashDB.getChannelData( source=source, dest=dest, timeframe=timeframe )

  types_getSiteNames = [ ]
  def export_getSiteNames( self ):
    """ Gets a list of all site names which are in MaDDashDB"""
    return MaDDashDB.getSiteNames()

