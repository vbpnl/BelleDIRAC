import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from DIRAC.Core.Base import Script
from DIRAC.DataManagementSystem.DB import Belle2MaDDashDB
import json

def createMap():
	Script.parseCommandLine( ignoreErrors = False )
	
	db = Belle2MaDDashDB.Belle2MaDDashDB()
	json_data = json.loads(db.getChannelData())
	siteNames = db.getSiteNames()
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




def createMatrix():
	d = createMap()
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


def createColoredGrid(M, sites):
	# make a color map of fixed colors
	cmap = colors.ListedColormap(['orange', 'green', 'yellow', 'red'])
	bounds=[-100, 0, .001, .01, 100]
	norm = colors.BoundaryNorm(bounds, cmap.N)


	fig = plt.figure(figsize=(10,10), dpi=1)
	ax = fig.add_subplot(111)
	res = ax.imshow(M, interpolation='nearest', cmap=cmap, norm=norm)

	N = len(M)

	for i in range(N):
	    for j in range(N):
	    	val = M[i][j]
	    	if val is not np.nan and val != -99:
	    		if val > 1:
	    			val = '%d' % int(val)
	    		else:
	    			val = '%.2f' % val
		        ax.annotate(val, xy=(j, i), 
		                    horizontalalignment='center',
		                    verticalalignment='center')

	cb = fig.colorbar(res, cmap=cmap, ticks=[0, .001, .01, 100], format='%.3f')
	plt.xticks(range(N), sites[:N], ha='right', rotation=45)
	plt.yticks(range(N), sites[:N])

if __name__ == '__main__':
	M, sites = createMatrix()
	createColoredGrid(M, sites)

	plt.gcf().subplots_adjust(bottom=.15, left=.3)
	plt.grid()
	#plt.title('Average Percentage of Dropped Packets Between Sites')
	plt.savefig('images/test_mesh.png')
