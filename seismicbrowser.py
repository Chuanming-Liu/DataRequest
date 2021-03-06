
import pyasdf
from obspy.clients.fdsn.client import Client
import obspy.clients.iris
from mpl_toolkits.basemap import Basemap, shiftgrid, cm
import matplotlib.pyplot as plt
import obspy
import numpy as np


mondict = {1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR', 5: 'MAY', 6: 'JUN', 7: 'JUL', 8: 'AUG', 9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DEC'}

def plot_fault_lines(mapobj, infname, lw=2, color='red'):
    with open(infname, 'rb') as fio:
        is_new  = False
        lonlst  = []
        latlst  = []
        for line in fio.readlines():
            if line.split()[0] == '>':
                x, y  = mapobj(lonlst, latlst)
                mapobj.plot(x, y,  lw = lw, color=color)
                # # # m.plot(xslb, yslb,  lw = 3, color='white')
                lonlst  = []
                latlst  = []
                continue
            lonlst.append(float(line.split()[0]))
            latlst.append(float(line.split()[1]))
        x, y  = mapobj(lonlst, latlst)
        mapobj.plot(x, y,  lw = lw, color=color)
            
    

class browseASDF(pyasdf.ASDFDataSet):
    
    def get_limits_lonlat(self):
        """Get the geographical limits of the stations
        """
        staLst  = self.waveforms.list()
        minlat  = 90.
        maxlat  = -90.
        minlon  = 360.
        maxlon  = 0.
        for staid in staLst:
            lat, elv, lon   = self.waveforms[staid].coordinates.values()
            if lon<0:
                lon += 360.
            minlat  = min(lat, minlat)
            maxlat  = max(lat, maxlat)
            minlon  = min(lon, minlon)
            maxlon  = max(lon, maxlon)
        print 'latitude range: ', minlat, '-', maxlat, 'longitude range:', minlon, '-', maxlon
        self.minlat=minlat; self.maxlat=maxlat; self.minlon=minlon; self.maxlon=maxlon
        return
    
    def get_stations(self, startdate=None, enddate=None,  startbefore=None, startafter=None, endbefore=None, endafter=None,\
            network=None, station=None, location=None, channel=None, includerestricted=False,\
            minlatitude=None, maxlatitude=None, minlongitude=None, maxlongitude=None, latitude=None, longitude=None, minradius=None, maxradius=None):
        """Get station inventory from IRIS server
        =======================================================================================================
        Input Parameters:
        startdate, enddata  - start/end date for searching
        network             - Select one or more network codes.
                                Can be SEED network codes or data center defined codes.
                                    Multiple codes are comma-separated (e.g. "IU,TA").
        station             - Select one or more SEED station codes.
                                Multiple codes are comma-separated (e.g. "ANMO,PFO").
        location            - Select one or more SEED location identifiers.
                                Multiple identifiers are comma-separated (e.g. "00,01").
                                As a special case ?--? (two dashes) will be translated to a string of two space
                                characters to match blank location IDs.
        channel             - Select one or more SEED channel codes.
                                Multiple codes are comma-separated (e.g. "BHZ,HHZ").
        includerestricted   - default is False
        minlatitude         - Limit to events with a latitude larger than the specified minimum.
        maxlatitude         - Limit to events with a latitude smaller than the specified maximum.
        minlongitude        - Limit to events with a longitude larger than the specified minimum.
        maxlongitude        - Limit to events with a longitude smaller than the specified maximum.
        latitude            - Specify the latitude to be used for a radius search.
        longitude           - Specify the longitude to the used for a radius search.
        minradius           - Limit to events within the specified minimum number of degrees from the
                                geographic point defined by the latitude and longitude parameters.
        maxradius           - Limit to events within the specified maximum number of degrees from the
                                geographic point defined by the latitude and longitude parameters.
        =======================================================================================================
        """
        try:
            starttime   = obspy.core.utcdatetime.UTCDateTime(startdate)
        except:
            starttime   = None
        try:
            endtime     = obspy.core.utcdatetime.UTCDateTime(enddate)
        except:
            endtime     = None
        try:
            startbefore = obspy.core.utcdatetime.UTCDateTime(startbefore)
        except:
            startbefore = None
        try:
            startafter  = obspy.core.utcdatetime.UTCDateTime(startafter)
        except:
            startafter  = None
        try:
            endbefore   = obspy.core.utcdatetime.UTCDateTime(endbefore)
        except:
            endbefore   = None
        try:
            endafter    = obspy.core.utcdatetime.UTCDateTime(endafter)
        except:
            endafter    = None
        client          = Client('IRIS')
        inv             = client.get_stations(network=network, station=station, starttime=starttime, endtime=endtime, startbefore=startbefore, startafter=startafter,\
                                endbefore=endbefore, endafter=endafter, channel=channel, minlatitude=minlatitude, maxlatitude=maxlatitude, \
                                minlongitude=minlongitude, maxlongitude=maxlongitude, latitude=latitude, longitude=longitude, minradius=minradius, \
                                    maxradius=maxradius, level='channel', includerestricted=includerestricted)
        self.add_stationxml(inv)
        try:
            self.inv    += inv
        except:
            self.inv    = inv
        return
    
    def read_TA_lst(self, infname, startdate=None, enddate=None,  startbefore=None, startafter=None, endbefore=None, endafter=None, location=None, channel=None,\
            includerestricted=False, minlatitude=None, maxlatitude=None, minlongitude=None, maxlongitude=None, \
            latitude=None, longitude=None, minradius=None, maxradius=None):
        """Get station inventory from IRIS server
        =======================================================================================================
        Input Parameters:
        startdate, enddata  - start/end date for searching
        network             - Select one or more network codes.
                                Can be SEED network codes or data center defined codes.
                                    Multiple codes are comma-separated (e.g. "IU,TA").
        station             - Select one or more SEED station codes.
                                Multiple codes are comma-separated (e.g. "ANMO,PFO").
        location            - Select one or more SEED location identifiers.
                                Multiple identifiers are comma-separated (e.g. "00,01").
                                As a special case ?--? (two dashes) will be translated to a string of two space
                                characters to match blank location IDs.
        channel             - Select one or more SEED channel codes.
                                Multiple codes are comma-separated (e.g. "BHZ,HHZ").
        includerestricted   - default is False
        minlatitude         - Limit to events with a latitude larger than the specified minimum.
        maxlatitude         - Limit to events with a latitude smaller than the specified maximum.
        minlongitude        - Limit to events with a longitude larger than the specified minimum.
        maxlongitude        - Limit to events with a longitude smaller than the specified maximum.
        latitude            - Specify the latitude to be used for a radius search.
        longitude           - Specify the longitude to the used for a radius search.
        minradius           - Limit to events within the specified minimum number of degrees from the
                                geographic point defined by the latitude and longitude parameters.
        maxradius           - Limit to events within the specified maximum number of degrees from the
                                geographic point defined by the latitude and longitude parameters.
        =======================================================================================================
        """
        try:
            starttime   = obspy.core.utcdatetime.UTCDateTime(startdate)
        except:
            starttime   = None
        try:
            endtime     = obspy.core.utcdatetime.UTCDateTime(enddate)
        except:
            endtime     = None
        try:
            startbefore = obspy.core.utcdatetime.UTCDateTime(startbefore)
        except:
            startbefore = None
        try:
            startafter  = obspy.core.utcdatetime.UTCDateTime(startafter)
        except:
            startafter  = None
        try:
            endbefore   = obspy.core.utcdatetime.UTCDateTime(endbefore)
        except:
            endbefore   = None
        try:
            endafter    = obspy.core.utcdatetime.UTCDateTime(endafter)
        except:
            endafter    = None
        client          = Client('IRIS')
        init_flag       = True
        with open(infname, 'rb') as fio:
            for line in fio.readlines():
                network = line.split()[1]
                station = line.split()[2]
                if network == 'NET':
                    continue
                # print network, station
                if init_flag:
                    try:
                        inv     = client.get_stations(network=network, station=station, starttime=starttime, endtime=endtime, startbefore=startbefore, startafter=startafter,\
                                    endbefore=endbefore, endafter=endafter, channel=channel, minlatitude=minlatitude, maxlatitude=maxlatitude, \
                                        minlongitude=minlongitude, maxlongitude=maxlongitude, latitude=latitude, longitude=longitude, minradius=minradius, \
                                            maxradius=maxradius, level='channel', includerestricted=includerestricted)
                    except:
                        print 'No station inv: ', line
                        continue
                    init_flag   = False
                    continue
                try:
                    inv     += client.get_stations(network=network, station=station, starttime=starttime, endtime=endtime, startbefore=startbefore, startafter=startafter,\
                                endbefore=endbefore, endafter=endafter, channel=channel, minlatitude=minlatitude, maxlatitude=maxlatitude, \
                                    minlongitude=minlongitude, maxlongitude=maxlongitude, latitude=latitude, longitude=longitude, minradius=minradius, \
                                        maxradius=maxradius, level='channel', includerestricted=includerestricted)
                except:
                    # for i in xrange(10):
                    #     try:
                    #         inv += client.get_stations(network=network, station=station, starttime=starttime, endtime=endtime, startbefore=startbefore, startafter=startafter,\
                    #             endbefore=endbefore, endafter=endafter, channel=channel, minlatitude=minlatitude, maxlatitude=maxlatitude, \
                    #                 minlongitude=minlongitude, maxlongitude=maxlongitude, latitude=latitude, longitude=longitude, minradius=minradius, \
                    #                     maxradius=maxradius, level='channel', includerestricted=includerestricted)
                    #     except:
                    print 'No station inv: ', line
                    continue
                    # if i >= 9:
                        # print 'No station inv: ', line
        self.add_stationxml(inv)
        try:
            self.inv    += inv
        except:
            self.inv    = inv
        return
    
    def _get_basemap(self, projection='lambert', geopolygons=None, resolution='i', blon=0., blat=0.):
        """Get basemap for plotting results
        """
        # fig=plt.figure(num=None, figsize=(12, 12), dpi=80, facecolor='w', edgecolor='k')
        try:
            minlon  = self.minlon-blon
            maxlon  = self.maxlon+blon
            minlat  = self.minlat-blat
            maxlat  = self.maxlat+blat
        except AttributeError:
            self.get_limits_lonlat()
            minlon  = self.minlon-blon; maxlon=self.maxlon+blon; minlat=self.minlat-blat; maxlat=self.maxlat+blat
        lat_centre  = (maxlat+minlat)/2.0
        lon_centre  = (maxlon+minlon)/2.0
        if projection == 'merc':
            m       = Basemap(projection='merc', llcrnrlat=minlat-5., urcrnrlat=maxlat+5., llcrnrlon=minlon-5.,
                        urcrnrlon=maxlon+5., lat_ts=20, resolution=resolution)
            m.drawparallels(np.arange(-80.0,80.0,5.0), labels=[1,0,0,1])
            m.drawmeridians(np.arange(-170.0,170.0,5.0), labels=[1,0,0,1])
            m.drawstates(color='g', linewidth=2.)
        elif projection == 'global':
            m       = Basemap(projection='ortho',lon_0=lon_centre, lat_0=lat_centre, resolution=resolution)
        elif projection == 'regional_ortho':
            m1      = Basemap(projection='ortho', lon_0=minlon, lat_0=minlat, resolution='l')
            m       = Basemap(projection='ortho', lon_0=minlon, lat_0=minlat, resolution=resolution,\
                        llcrnrx=0., llcrnry=0., urcrnrx=m1.urcrnrx/mapfactor, urcrnry=m1.urcrnry/3.5)
            m.drawparallels(np.arange(-80.0,80.0,10.0), labels=[1,0,0,0],  linewidth=2,  fontsize=20)
            m.drawmeridians(np.arange(-170.0,170.0,10.0),  linewidth=2)
        elif projection=='lambert':
            distEW, az, baz = obspy.geodetics.gps2dist_azimuth((lat_centre+minlat)/2., minlon, (lat_centre+minlat)/2., maxlon) # distance is in m
            distNS, az, baz = obspy.geodetics.gps2dist_azimuth(minlat, minlon, maxlat-2, minlon) # distance is in m
            m       = Basemap(width=distEW, height=distNS, rsphere=(6378137.00,6356752.3142), resolution='h', projection='lcc',\
                        lat_1=minlat, lat_2=maxlat, lon_0=lon_centre, lat_0=lat_centre+1.5)
            # distEW, az, baz = obspy.geodetics.gps2dist_azimuth(minlat, minlon, minlat, maxlon) # distance is in m
            # distNS, az, baz = obspy.geodetics.gps2dist_azimuth(minlat, minlon, maxlat+2., minlon) # distance is in m
            # m               = Basemap(width = distEW, height=distNS, rsphere=(6378137.00,6356752.3142), resolution='l', projection='lcc',\
            #                     lat_1=minlat, lat_2=maxlat, lon_0=lon_centre, lat_0=lat_centre+1)
            m.drawparallels(np.arange(-80.0,80.0,10.0), linewidth=1, dashes=[2,2], labels=[1,1,0,0], fontsize=15)
            m.drawmeridians(np.arange(-170.0,170.0,10.0), linewidth=1, dashes=[2,2], labels=[0,0,1,1], fontsize=15)
        m.drawcoastlines(linewidth=1.0)
        m.drawcountries(linewidth=1.)
        # m.fillcontinents(lake_color='#99ffff',zorder=0.2)
        # m.drawmapboundary(fill_color="white")
        try:
            geopolygons.PlotPolygon(inbasemap=m)
        except:
            pass
        return m
    
    def plot_stations(self, projection='lambert', geopolygons=None, showfig=True, blon=.5, blat=0.5):
        """Plot station map
        ==============================================================================
        Input Parameters:
        projection      - type of geographical projection
        geopolygons     - geological polygons for plotting
        blon, blat      - extending boundaries in longitude/latitude
        showfig         - show figure or not
        ==============================================================================
        """
        staLst  = self.waveforms.list()
        stalons = np.array([])
        stalats = np.array([])
        for staid in staLst:
            stla, evz, stlo = self.waveforms[staid].coordinates.values()
            stalons         = np.append(stalons, stlo)
            stalats         = np.append(stalats, stla)
        m                   = self._get_basemap(projection=projection, geopolygons=geopolygons, blon=blon, blat=blat)
        # m.warpimage(image='etopo1')
        # m.warpimage(image='https://www.ngdc.noaa.gov/mgg/image/color_etopo1_ice_low.jpg')
        # m.shadedrelief()
        # m.etopo()
        stax, stay          = m(stalons, stalats)
        m.plot(stax, stay, 'r^', markersize=10)
        # plt.title(str(self.period)+' sec', fontsize=20)
        if showfig:
            plt.show()
        return
    
    def plot_inv(self, projection='lambert', geopolygons=None, showfig=True, blon=1, blat=1, \
                 netcodelist=[], plotetopo=True, stacode=None):
        """Plot station map
        ==============================================================================
        Input Parameters:
        projection      - type of geographical projection
        geopolygons     - geological polygons for plotting
        blon, blat      - extending boundaries in longitude/latitude
        showfig         - show figure or not
        ==============================================================================
        """
        # inv     = self.inv
        m       = self._get_basemap(projection=projection, geopolygons=geopolygons, blon=blon, blat=blat)
        if plotetopo:
            from netCDF4 import Dataset
            from matplotlib.colors import LightSource
            import pycpt
            etopodata   = Dataset('/home/leon/station_map/grd_dir/ETOPO2v2g_f4.nc')
            etopo       = etopodata.variables['z'][:]
            lons        = etopodata.variables['x'][:]
            lats        = etopodata.variables['y'][:]
            ls          = LightSource(azdeg=315, altdeg=45)
            # nx          = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1
            etopo,lons  = shiftgrid(180.,etopo,lons,start=False)
            # topodat,x,y = m.transform_scalar(etopo,lons,lats,nx,ny,returnxy=True)
            ny, nx      = etopo.shape
            topodat,xtopo,ytopo = m.transform_scalar(etopo,lons,lats,nx, ny, returnxy=True)
            m.imshow(ls.hillshade(topodat, vert_exag=1., dx=1., dy=1.), cmap='gray')
            mycm1       = pycpt.load.gmtColormap('/home/leon/station_map/etopo1.cpt')
            mycm2       = pycpt.load.gmtColormap('/home/leon/station_map/bathy1.cpt')
            mycm2.set_over('w',0)
            m.imshow(ls.shade(topodat, cmap=mycm1, vert_exag=1., dx=1., dy=1., vmin=0, vmax=8000))
            m.imshow(ls.shade(topodat, cmap=mycm2, vert_exag=1., dx=1., dy=1., vmin=-11000, vmax=-0.5))
        
        # shapefname  = '/home/leon/geological_maps/qfaults'
        # m.readshapefile(shapefname, 'faultline', linewidth=2, color='red')
        # shapefname  = '/home/leon/AKgeol_web_shp/AKStategeolarc_generalized_WGS84'
        # m.readshapefile(shapefname, 'geolarc', linewidth=1, color='red')
        # inet        = 0
        # for network in inv:
        #     stalons     = np.array([])
        #     stalats     = np.array([])
        #     if len(netcodelist) != 0:
        #         if network.code not in netcodelist:
        #             continue
        #     inet        += 1
        #     for station in network:
        #         # if stacode != None:
        #         #     if station.code != stacode:
        #         #         continue
        #         # if station.code == 'DHY':
        #         # time            = obspy.UTCDateTime('20150101')
        #         # if station.end_date < time:
        #         #     continue
        #         # time            = obspy.UTCDateTime('20141231')
        #         # if station.start_date > time:
        #         #     continue
        #         stalons         = np.append(stalons, station.longitude)
        #         stalats         = np.append(stalats, station.latitude)
        #     stax, stay      = m(stalons, stalats)
        #     # if inet==1:
        #     #     m.plot(stax, stay, 'r^', mec='k', markersize=8, label = network.code)
        #     # if inet == 2:
        #     #     m.plot(stax, stay, 'b^', mec='k', markersize=8, label = network.code)
        #     # m.plot(stax, stay, 'r^', mec='k', markersize=20, label = network.code+'.'+stacode)
        #     
        #     # m.plot(stax, stay, 'r^', markersize=15)
        #     labellst    = ['r^', 'b^', 'm^', 'c^', 'w^', \
        #                    'ro', 'bo', 'mo', 'co',  'wo', \
        #                       'rv', 'bv', 'mv', 'cv',  'wv', \
        #                       'rs', 'bs', 'ms', 'cs',  'ws', \
        #                       'rp', 'bp', 'mp', 'cp',  'wp']
        #     m.plot(stax, stay, labellst[inet-1], mec='k', markersize=8, label = network.code)
            # if inet<=10:
            #     m.plot(stax, stay, '^', mec='k', markersize=8, label = network.code)
            # elif inet > 10 and inet <=20:
            #     m.plot(stax, stay, 's', mec='k', markersize=8, label = network.code)
            # elif inet > 20:
            #     m.plot(stax, stay, 'v', mec='k', markersize=8, label = network.code)
            
            # xc, yc      = m(np.array([-153]), np.array([67.5]))
            # m.plot(xc, yc,'*', ms = 15, markeredgecolor='black', markerfacecolor='yellow')
            # xc, yc      = m(np.array([-150]), np.array([65]))
            # m.plot(xc, yc,'*', ms = 15, markeredgecolor='black', markerfacecolor='yellow')
            # xc, yc      = m(np.array([-149]), np.array([62]))
            # m.plot(xc, yc,'*', ms = 15, markeredgecolor='black', markerfacecolor='yellow')
            
        # plt.legend(numpoints=1, loc=2, fontsize=13)
        
        plot_fault_lines(m, 'AK_Faults.txt')
        if showfig:
            plt.show()
        return
    
    def write_inv(self, outfname, format='stationxml'):
        self.inv.write(outfname, format=format)
        return
    
    def read_inv(self, infname):
        self.inv    = obspy.core.inventory.inventory.read_inventory(infname)
        return
    
    def check_access(self):
        for net in self.inv:
            for sta in net:
                if sta.restricted_status != 'open':
                    print sta
        return
    
    def get_date(self):
        start_date  =  obspy.UTCDateTime('2599-12-31T23:59:59.000000Z')
        end_date    =  obspy.UTCDateTime(0)
        for net in self.inv:
            for sta in net:
                if sta.start_date < start_date:
                    start_date      = sta.start_date
                    self.sta_start  = sta
                    
                if sta.end_date > end_date:
                    end_date    = sta.end_date
                    self.sta_end= sta
        self.start_date = start_date
        self.end_date   = end_date
        
    def write_txt(self, outfname):
        with open(outfname, 'w') as fid:
            for staid in self.waveforms.list():
                temp    = staid.split('.')
                network = temp[0]
                stacode = temp[1]
                fid.writelines(stacode+' '+network+'\n')
        return
            
        
        
        
    
    