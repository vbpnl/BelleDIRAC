
from DIRAC import gConfig, S_OK, S_ERROR, gLogger
from DIRAC.Core.DISET.RPCClient import RPCClient
import json
import numpy as np

def createMatrix():
  import DIRAC.Core.Base.Script as Script
  Script.parseCommandLine()
  service = RPCClient('DistributedDataManagement/MaDDash')    
  json_data = json.loads(service.getChannelData(None, None, 'MOST_RECENT')['Value'])
  for channel in json_data:
    print '%s->%s' % (channel['Source'], channel['Dest'])
  return
  return json_data
  print json_data
  n = len(service.getSiteNames()['Value'])
  print 
  siteNames = set()
  channelNum = 0
  m = []
  for i in range(n):
    m.append([])
    siteNames.add(json_data[channelNum]['Source'])
    for j in range(n-1):
      channel = json_data[channelNum]
      if i == j:
        m[i].append(np.nan)
      else:
        avg = channel['Average']
        m[i].append(avg)

      channelNum = channelNum + 1
  return m, siteNames

def test():
  createMatrix()
  #print m
  #print siteNames

if __name__ == '__main__':
  test()


#   print json_data
#   siteNames = service.getSiteNames()['Value']
#   d = {}
#   for i in range(len(siteNames)):
#     d[siteNames[i]] = {}
#     for j in range(len(siteNames)):
#       if i == j:
#         d[siteNames[i]][siteNames[j]] = np.nan
#       else:
#         d[siteNames[i]][siteNames[j]] = 0
#   for channel in json_data:
#     source = channel['Source']
#     dest = channel['Dest']
#     avg = channel['Average']
#     d[source][dest] = avg
#   return d

# def createMatrix():
#   d = createMap()
#   sites = []
#   M = []
#   count = 0
#   for source in d:
#     sites.append(source)
#     M.append([])
#     for dest in d[source]:
#       M[count].append(d[source][dest])
#     count = count + 1
#   return M, sites

	
