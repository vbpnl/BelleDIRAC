from WebAppDIRAC.Lib.WebHandler import WebHandler, WErr, WOK, asyncGen
from DIRAC import gConfig, S_OK, S_ERROR, gLogger
from DIRAC.Core.Utilities import Time
from DIRAC.Core.DISET.RPCClient import RPCClient
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

class MaDDashHandler(WebHandler):

  AUTH_PROPS = "authenticated"
  global MaDDashService
  MaDDashService = RPCClient('DistributedDataManagement/MaDDash')

  @asyncGen
  def web_getChannelData(self):
    #timestamp = Time.dateTime().strftime("%Y-%m-%d %H:%M [UTC]")


    values = json.loads(MaDDashService.getChannelData(None, None, 'MOST_RECENT')['Value'])
    total = len(values)
    callback = {"success":"true", "result":values, "total":total}
    self.finish(callback)

  def web_getGrid(self):
    M, sites = self.createMatrix()
    self.createColoredGrid(M, sites)

    plt.gcf().subplots_adjust(bottom=.15, left=.3)
    plt.grid()
    plt.title('Average Percentage of Dropped Packets\nBetween Sites')
    plt.savefig('/opt/dirac/pro/BelleDIRAC/WebApp/static/BelleDIRAC/MaDDash/images/MaDDashMesh.png')

  def createMap(self):    
    json_data = json.loads(MaDDashService.getChannelData(None, None, 'MOST_RECENT')['Value'])
    siteNames = MaDDashService.getSiteNames()['Value']
    d = {}
    for i in range(len(siteNames)):
      d[siteNames[i]] = {}
      for j in range(len(siteNames)):
        if i == j:
          d[siteNames[i]][siteNames[j]] = np.nan
        else:
          d[siteNames[i]][siteNames[j]] = 0
    for channel in json_data:
      source = channel['Source']
      dest = channel['Dest']
      avg = channel['Average']
      d[source][dest] = avg
    return d


  def createMatrix(self):
    d = self.createMap()
    sites = []
    M = []
    count = 0
    for source in d:
      sites.append(source)
      M.append([])
      for dest in d[source]:
        M[count].append(d[source][dest])
      count = count + 1
    return M, sites

  # def createMatrix(self):
  #   service = RPCClient('DistributedDataManagement/MaDDash')    
  #   json_data = json.loads(service.getChannelData(None, None, 'MOST_RECENT')['Value'])
  #   n = len(service.getSiteNames()['Value'])
  #   print 
  #   siteNames = set()
  #   channelNum = 0
  #   m = []
  #   for i in range(n):
  #     m.append([])
  #     siteNames.add(json_data[channelNum]['Source'])
  #     for j in range(n-1):
  #       channel = json_data[channelNum]
  #       if i == j:
  #         m[i].append(np.nan)
  #       else:
  #         avg = channel['Average']
  #         m[i].append(avg)

  #       channelNum = channelNum + 1
  #   return m, siteNames


  def createColoredGrid(self, M, sites):
    # make a color map of fixed colors
    cmap = colors.ListedColormap(['orange', 'green', 'yellow', 'red'])
    bounds=[-100, 0, .001, .01, 100]
    norm = colors.BoundaryNorm(bounds, cmap.N)


    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    res = ax.imshow(M, interpolation='nearest', cmap=cmap, norm=norm)

    N = len(M)

    for i in range(N):
        for j in range(N):
          val = M[i][j]
          if val is not np.nan and val != -99:
            if val == 0:
              val = '%d' % int(val)
            elif val > 1:
              val = '%d' % int(val)
            else:
              val = '%.3f' % val
            ax.annotate(val, size=10, xy=(j, i), 
                        horizontalalignment='center',
                        verticalalignment='center')

    #cb = fig.colorbar(res, cmap=cmap, ticks=[0, .001, .01, 100], format='%.3f')
    plt.xticks(range(N), sites[:N], ha='right', rotation=45)
    plt.yticks(range(N), sites[:N])


