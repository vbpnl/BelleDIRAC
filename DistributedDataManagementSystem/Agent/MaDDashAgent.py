""" :mod: Belle2MaDDashAgent

    Uses MaDDash API to retrieve data in each 
    cell of Belle II Mesh and insert data into the MaDDashDB
"""

__RCSID__ = "$Id$"

# # imports
import urllib
import urllib2
import json
from datetime import datetime
from DIRAC import S_OK, S_ERROR
from DIRAC.Core.Base.AgentModule import AgentModule
from BelleDIRAC.DistributedDataManagementSystem.DB import MaDDashDB
from DIRAC.Core.DISET.RPCClient import RPCClient

class MaDDashAgent( AgentModule ):
    """
        .. class:: MaDDashAgent

    """

    def initialize( self ):
        """ 
          agent's initialization
        
        """
        self.am_setOption( "PollingTime", 2400.0 )
        return S_OK()



    def execute( self ):
   """Main Agent code:
      1.- Query MaDDash API for Belle II Mesh.
      Retrieve all cells' perfsonar checks in grid.
      2.- Parse JSON response for check statisitcs (avg,min,max,sd)
      3.- Insert statistics into MaDDashDB
    """
        dashboards = self.getDashboards()
        BelleIIMesh = self.getBelleIIMeshDashboard(dashboards)
        grid = self.getGrids(BelleIIMesh)
        checks = self.getChecks(grid)
        for check in checks:
            check_uri = check['uri']
            check_data = self.getCheck(check_uri)
            check_info = self.getCheckInfo(check_data)
      
            source = check_info[1]
            dest = check_info[2]

            #initialize configuration
            from DIRAC.Core.Base import Script
            Script.parseCommandLine( ignoreErrors = False )

            #initialize db and insert data
            MaDDashService = RPCClient('DistributedDataManagement/MaDDash')
            #db = Belle2MaDDashDB.Belle2MaDDashDB()
            if not MaDDashService.channelExists(source, dest)['Value']:
                MaDDashService.insert('Channel', MaDDashService.getFieldNames('Channel')['Value'], [ source, dest ])
            channelID = MaDDashService.getChannelID(source, dest)['Value']
            timestamp = str(datetime.now())
            #ignore sourceSiteName and destSiteName and insert channelID instead
            toInsert = [timestamp] + [check_info[0]] + [channelID] + check_info[3:]
            result = MaDDashService.insert('Loss', MaDDashService.getFieldNames('Loss')['Value'], toInsert)
        return S_OK()

    def get_data( self, url ):
        '''
        
          Queries REST API given by url and returns text response
          :parm url: url you wish to query
          :returns text data returned by url
        
        '''
        #parse URL on '/'
        lurl = url.split('/') 
        for i in range(len(lurl)):
            #need to properly encode URL if it contains spaces
            if ' ' in lurl[i]:
                #properly encode spaces
                quoted_query = urllib.quote(lurl[i])
                #delete old with spaces and reinsert new without
                lurl.pop(i)
                lurl.insert(i, quoted_query)
                #convert back to string
                url = '/'.join(lurl)
        
        req = urllib2.Request(url)
        handler = urllib2.urlopen(req)
        result = handler.read()
        return result

    def getDashboards( self ):
        '''
        
          :returns all dashboards decoded as JSON
        
        '''
        r = self.get_data('http://maddash.aglt2.org/maddash/dashboards')
        return json.loads(r)

    def getBelleIIMeshDashboard( self, dashboards ):
        '''
          :param dashboards: dashboard JSON
          :returns Belle II Mesh Dashboard encoded as JSON
        
        '''
        for dashboard in dashboards['dashboards']:
            if dashboard['name'] == 'Belle II Mesh':
                return dashboard

    def getGrids( self, BelleIIMeshDashboard ):
        '''
          :param BelleIIMeshDashboard: BelleIIMeshDashboard JSON
          :returns Belle II Mesh grid encoded as JSON
        
        '''
        l = []
        for grid in BelleIIMeshDashboard['grids']:
            r = self.get_data('http://maddash.aglt2.org/maddash/grids/%s' % grid['name'])
            l.append(json.loads(r))
        #Right now we only want the Latency Mesh
        return l[0]
        
    def getCheck( self, check_uri ):
        '''

          :param check_uri: uri of check you want to retrieve
          :returns specified check in decoded JSON
        
        '''
        r = self.get_data('http://maddash.aglt2.org/%s' % (check_uri))
        return json.loads(r)

    def getChecks( self, grid ):
        '''

          Iterates through each cell in grid and retrieves Loss check uri for that cell
          :returns list of check uris
          :param grid: Grid JSON you wish to retrive checks from
        
        '''
        checks = []
        grid = grid['grid']
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                #No check if i == j
                if i != j:
                    #We specifically want the loss check
                    lossCheck = grid[i][j][0]
                    checks.append(lossCheck)
        return checks
    
    def getCheckInfo( self, check ):
        '''
        
          :param check: check JSON you wish to retrive info from
          :returns statistics on most recently performed 
          check (min, max, avg, sd), as well as its timestamp, source site and destination site
        
        '''
        sourceSite = str(check['rowName'])
        destSite = str(check['colName'])
        timestamp = str(datetime.fromtimestamp(check['history'][0]['time']))
    
        # If check timed out and didn't return data, we fill values with -99
        if check['history'][0]['returnCode'] == 3:
            min = -99
            max = -99
            avg = -99
            sd = -99
        else:
            min = float(check['history'][0]['returnParams']['Min'])
            max = float(check['history'][0]['returnParams']['Max'])
            avg = float(check['history'][0]['returnParams']['Average'])
            sd = float(check['history'][0]['returnParams']['Standard_Deviation'])
        return [timestamp, sourceSite, destSite, min, max, avg, sd]
    