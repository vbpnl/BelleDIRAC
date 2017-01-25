from WebAppDIRAC.Lib.WebHandler import WebHandler, WErr, WOK, asyncGen
from DIRAC import gConfig, S_OK, S_ERROR, gLogger
from DIRAC.Resources.Storage.StorageElement import StorageElement
from DIRAC.Core.DISET.RPCClient import RPCClient
import matplotlib.pyplot as plt
import matplotlib as mpl

class StorageAccountingHandler(WebHandler):

  AUTH_PROPS = "authenticated"
  global service
  service = RPCClient('DistributedDataManagement/SpaceTokenStorageAccounting')

  def web_getStorage(self):
    availableOrPledged = self.request.arguments["availableOrPledged"][0]
    percentageOfTotalBool = self.request.arguments["percentageOfTotalBool"][0]
    percentageFullBool = self.request.arguments["percentageFullBool"][0]
    if percentageOfTotalBool == 'true':
      percentageOfTotalBool = True
    else:
      percentageOfTotalBool = False
    if percentageFullBool == 'true':
      percentageFullBool = True
    else:
      percentageFullBool = False
    values = []
    hosts = self.getHosts()
    for host in hosts:
      if percentageFullBool:
        title = 'Percentage Storage Site Full'
        fileName = 'percentFullPie.png'
        pledged = service.getPledgedStorage(host)
        available = service.getAvailableStorage(host)
        if pledged['OK'] and available['OK']:
          res = {'OK':True}
        else:
          res = {'OK':False}
      elif availableOrPledged == 'available':
        res = service.getAvailableStorage(host)
        if percentageOfTotalBool:
          title = 'Available Storage Space As Percentage\nof Total'
          fileName = 'availableStoragePercentagePie.png'
        else:
          title = 'Available Storage Space in TB'
          fileName = 'availableStoragePie.png'
      elif availableOrPledged == 'pledged':
        res = service.getPledgedStorage(host)
        if percentageOfTotalBool:
          title = 'Pledged Storage Space As Percentage\nof Total'
          fileName = 'pledgedStoragePercentagePie.png'
        else:
          title = 'Pledged Storage Space in TB'
          fileName = 'pledgedStoragePie.png'
      if res['OK']:
        if percentageFullBool:
          pledgedBytes = pledged['Value'][0][0]
          availableBytes = available['Value'][0][0]
          percentFull = (pledgedBytes - availableBytes) / float(pledgedBytes) * 100
          values.append((percentFull, host, pledgedBytes, availableBytes))
        else:
          storageBytes = res['Value'][0][0]
          storageTeraBytes = storageBytes * 10**-12
          values.append((storageTeraBytes, host))
    sortedValues = sorted(values, reverse=True)
    labels=[sortedValues[i][1] for i in range(len(values))]
    sortedValues = [sortedValues[i][0] for i in range(len(values))]
    if percentageOfTotalBool:
      autopct = '%1.1f%%'
    elif percentageFullBool:
      autopct = self.make_autopct2(values)
    else:
      autopct = self.make_autopct(values)
    self.plotFig(values, labels, title, fileName, autopct)


  def getHosts(self):
    validHosts = set()
    res = gConfig.getSections( '/Resources/StorageElements')
    se_list = res[ 'Value' ]
    for se_name in se_list:
      srm_values = StorageElement( se_name ).getStorageParameters( "SRM2" )
      if srm_values['OK']:
        host = srm_values['Value']['Host']
        validHosts.add(host)
    return validHosts

  def make_autopct(self, values):
    def my_autopct(pct):
        total = sum(values)
        val = float(pct*total/100.0)
        return '%.2f TB' % val
    return my_autopct

  def make_autopct2(self, values):
    def my_autopct2(pct):
        total = sum(values)
        val = float(pct*total/100.0)
        return '%.2f%%' % val
    return my_autopct2

  def plotFig(self, values, labels, title, fileName, autopct):
    largerValues = []
    largerLabels = []
    otherValues = []
    otherLabels = []
    for value,label in zip(values,labels):
      if value < .1*sum(values):
        otherValues.append(value)
        otherLabels.append(label)
      else:
        largerValues.append(value)
        largerLabels.append(label)
    values = [] + largerValues
    labels = [] + largerLabels
    values.append(sum(otherValues))
    labels.append('Other')
    plt.axes(aspect=1)
    patches, text, autotexts = plt.pie(values, labels=labels, autopct=autopct)
    for p, t in zip(patches, autotexts):
      if p.get_fc() == (0.0, 0.0, 0.0, 1.0):
        t.set_color('white')
    for t, at in zip(text, autotexts):
      t.set_size('x-small')
      at.set_size('x-small')
    plt.title(title)
    if 'of Total' in title:
      legendOtherLabels = ['%s: %.2f%%' % (otherLabels[i], otherValues[i] / sum(values) * 100) for i in range(len(otherValues))]
    elif 'Percentage' in title:
      legendOtherLabels = ['%s: %.2f%%' % (otherLabels[i], otherValues[i]) for i in range(len(otherValues))]
    else:
      legendOtherLabels = ['%s: %.2f TB' % (otherLabels[i], otherValues[i]) for i in range(len(otherValues))]
    legendOtherHandles = [mpl.lines.Line2D([0,0], [0,0], color='black') for i in range(len(otherValues))]
    leg = plt.legend(legendOtherHandles, legendOtherLabels, bbox_to_anchor=(1.05, 0.5), loc='center left', title='Other', fontsize='x-small')
    #plt.legend(patches, labels, bbox_to_anchor=(0, .5), fontsize='small')
    plt.savefig('/opt/dirac/pro/BelleDIRAC/WebApp/static/BelleDIRAC/StorageAccounting/images/'+fileName, bbox_inches='tight')
    plt.clf()
    plt.close()
