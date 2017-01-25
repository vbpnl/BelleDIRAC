########################################################################
# $HeadURL$
# File: SpaceTokenStorageAccountingHandler.py
# Author: Malachi.Schram@NOSPAMpnnl.gov
########################################################################
""" :mod: SpaceTokenStorageAccountingHandler
    ====================
"""

__RCSID__ = "$Id: $"

from types import StringType, ListType, DictType, IntType, LongType, StringTypes, TupleType
from DIRAC.Core.DISET.RequestHandler import RequestHandler
from DIRAC import gLogger, S_OK, S_ERROR
from DIRAC.Core.Utilities import Time

from BelleDIRAC.DistributedDataManagementSystem.DB.SpaceTokenStorageAccountingDB import SpaceTokenStorageAccountingDB

class SpaceTokenStorageAccountingHandler( RequestHandler ):
  
  @classmethod
  def initializeHandler( cls, serviceInfo ):
    """ Handler initialization
    """
    return S_OK()

  def initialize(self):
    """ Response initialization
    """
    gLogger.info('Initialize db')
    try:
      self.b2stdb = SpaceTokenStorageAccountingDB()
    except Exception:
      return S_ERROR('Problem with SpaceTokenStorageAccountingDB')

  auth_getAvailableStorage = [ 'all' ]
  types_getAvailableStorage = [ StringTypes ]
  def export_getAvailableStorage( self, storage_element ):
    return  self.b2stdb.getAvailableStorage( storage_element )

  auth_getPledgedStorage = [ 'all' ]
  types_getPledgedStorage = [ StringTypes ]
  def export_getPledgedStorage( self, storage_element ):
    return  self.b2stdb.getPledgedStorage( storage_element )
