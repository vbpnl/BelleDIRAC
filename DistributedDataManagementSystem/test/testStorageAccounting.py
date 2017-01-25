from DIRAC import gConfig, S_OK, S_ERROR, gLogger
from DIRAC.Resources.Storage.StorageElement import StorageElement
from DIRAC.Core.DISET.RPCClient import RPCClient
from DIRAC.Core.Base import Script
import matplotlib.pyplot as plt
import matplotlib as mpl

def testStorageAccounting():
	Script.parseCommandLine()
	service = RPCClient('DistributedDataManagement/SpaceTokenStorageAccounting')
	hosts = getHosts()
	values = []
	siteNames = []
	for host in hosts:
		res = service.getPledgedStorage(host)
		if res['OK']:
			storageBytes = res['Value'][0][0]
			storageTeraBytes = storageBytes * 10**-12
			values.append((storageTeraBytes, host))
			#values.append(storageTeraBytes)
			#siteNames.append(se_name)
	# d = {}
	# for i in range(len(values)):
		#d[values[i]] = siteNames[i]
	values = sorted(values, reverse=True)
	labels=[values[i][1] for i in range(len(values))]
	values = [values[i][0] for i in range(len(values))]
	autopct = make_autopct(values)
	plotFig(values, labels, autopct)

def getHosts():
	validHosts = set()
	res = gConfig.getSections( '/Resources/StorageElements')
	se_list = res[ 'Value' ]
	for se_name in se_list:
		srm_values = StorageElement( se_name ).getStorageParameters( "SRM2" )
		if srm_values['OK']:
			host = srm_values['Value']['Host']
			validHosts.add(host)
	return validHosts

def make_autopct(values):
	def my_autopct(pct):
	    total = sum(values)
	    val = float(pct*total/100.0)
	    return '%.2f TB' % val
	return my_autopct

def plotFig(values, labels, autopct):
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
	#print zip(values, labels)
	#print zip(otherValues, otherLabels)
	legendOtherLabels = ['%s: %.2f TB' % (otherLabels[i], otherValues[i]) for i in range(len(otherValues))]
	plt.axes(aspect=1)
	#fig = plt.figure()
	#ax = fig.add_axes([0.1, 0.1, 0.5, 0.5])
	#ax = plt.subplot(121)
	patches, text, autotexts = plt.pie(values, labels=labels, autopct=autopct)
	#plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
	legendColor = ''
	for patch in patches:
		if patch.get_label() == 'Other':
			legendColor = patch.get_facecolor()
	for p, t in zip(patches, autotexts):
		if p.get_fc() == (0.0, 0.0, 0.0, 1.0):
			t.set_color('white')
	for t, at in zip(text, autotexts):
		t.set_size('x-small')
		at.set_size('x-small')
	#leg = plt.legend(otherValues, legendOtherLabels, title='Other', loc='center left', bbox_to_anchor=(.75, 0.6), fontsize='x-small')
	#fig = plt.gcf()
	#fig.subplots_adjust(left=.2)
	legendOtherHandles = [mpl.lines.Line2D([0,0], [0,0], color='black') for i in range(len(otherValues))]
	leg = plt.legend(legendOtherHandles, legendOtherLabels, bbox_to_anchor=(1.05, 0.5), loc='center left', title='Other', fontsize='x-small')
	# for l in leg.legendHandles:
	# 	l.set_color(legendColor)
	#print legendOtherLabel
	plt.title('Available Storage Space in TB')
	plt.savefig('test.png', bbox_inches='tight')
	plt.clf()
	plt.close()

if __name__ == '__main__':
	testStorageAccounting()