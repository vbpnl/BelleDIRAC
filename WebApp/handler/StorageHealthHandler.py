from WebAppDIRAC.Lib.WebHandler import WebHandler, WErr, WOK, asyncGen
from DIRAC import gConfig, S_OK, S_ERROR, gLogger
from DIRAC.Core.DISET.RPCClient import RPCClient

class StorageHealthHandler(WebHandler):

  AUTH_PROPS = "authenticated"
  global service
  service = RPCClient('DistributedDataManagement/StorageHealth')

  @asyncGen
  def web_getStorageHealth(self):
    values = []
    res = gConfig.getSections( '/Resources/StorageElements' )
    se_list = res[ 'Value' ]
    for se_name in se_list:
      isLS = service.getStorageisLS(se_name)
      isUP = service.getStorageisUP(se_name)
      isDN = service.getStorageisDN(se_name)
      isRMDIR = service.getStorageisRMDIR(se_name)
      isRM = service.getStorageisRM(se_name)
      if isLS['OK'] and isUP['OK'] and isDN['OK'] and isRMDIR['OK'] and isRM['OK']:
        isLS = isLS['Value'][0][0]
        isUP = isUP['Value'][0][0]
        isDN = isDN['Value'][0][0]
        isRMDIR = isRMDIR['Value'][0][0]
        isRM = isRM['Value'][0][0]
        isHealthy = 1 if (isLS and isUP and isDN and isRMDIR and isRM) else 0
        values.append({'StorageElement': se_name, 'isLS': isLS, 'isUP': isUP, 
          'isDN': isDN, 'isRMDIR': isRMDIR, 'isRM': isRM, 'isHealthy': isHealthy})
    callback = {"success":"true", "result":values }
    self.finish(callback)
