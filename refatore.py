import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def create_map(model, lat1, lat2, lon1, lon2, res):
    if model == 'wrf':
        m = Basemap(llcrnrlon=lon1-0.05, llcrnrlat=lat1-0.05, urcrnrlon=lon2+0.05, urcrnrlat=lat2+0.05,
               resolution='i', projection='tmerc', lat_0=np.mean(lats), lon_0=np.mean(lons))

        latitudes = wrf_lats[(wrf_lats > lats[0]) & (wrf_lats < lats[1])]
        longitudes = wrf_lons[(wrf_lons > lons[0]) & (wrf_lons < lons[1])]

    else:
        m = Basemap(llcrnrlon=lon1-0.1, llcrnrlat=lat1-0.1, urcrnrlon=lon2+0.1, urcrnrlat=lat2+0.1,
               resolution='i', projection='tmerc', lat_0=np.mean(lats), lon_0=np.mean(lons))

        latitudes = np.arange(lat1, lat2+res, res)
        longitudes = np.arange(lon1, lon2+res, res)

    return m, latitudes, longitudes

def plot_points(m, latitudes, longitudes):
    for y in latitudes:
        for x in longitudes:
            xpt, ypt = m(x, y)
            m.plot([xpt], [ypt], 'ro', markersize=.5)
            plt.text(xpt, ypt, f'{x:0.02f}, {y:0.02f}', fontsize=2, weight='bold', color='magenta', va='bottom', ha='center')

def plot_map(model, lats, lons):
    ress = {
       'wrf': 0.07,
       'gfs': 0.25,
    }

    wrf_lats = np.arange(-57.9, 17.69, 0.07)
    wrf_lons = np.arange(269.32-360, 340.58-360, 0.07)

    lat1, lat2 = round(lats[0], 2), round(lats[1], 2)
    lon1, lon2 = round(lons[0], 2), round(lons[1], 2)

    m, latitudes, longitudes = create_map(model, lat1, lat2, lon1, lon2, ress[model])

    plot_points(m, latitudes, longitudes)

    plt.title(model)
    m.readshapefile('Brasil_estados', 'Brasil_estados', linewidth=0.25, color='blue')
    plt.savefig(model+ '.png', dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()

lats = sorted([-25.561503547985822, -23.507873138354064])
lons = sorted([-49.51023615949202, -46.5811047502339])

plot_map('wrf', lats, lons)
plot_map('gfs', lats, lons)