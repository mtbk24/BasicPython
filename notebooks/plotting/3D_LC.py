# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 16:06:07 2017

@author: KimiZ
"""
from __future__ import division
from astropy.io import fits as pyfits
import os, glob, numpy
import pandas as pd
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
import matplotlib.pyplot as plt
import Zoldak
from Zoldak.General.assortedfunctions import nearest

def get_channels(File, emin, emax):
    '''
    get_channels(File, emin, emax)
    File:   Fits file already opened with pyfits. 
            Make sure it has an EBOUNDS table containing 
            CHANNEL, E_MIN, and E_MAX.
    emin:  minimum energy, such as 30. keV
    emax:  maximum energy, such as 500 keV.
    
    *** Uses nearest function from from  
    Zoldak.General.assortedfunctions import nearest
    import call is within this function.
    
    '''
    # BECAUSE THE CHANNEL NUMBERS START AT 0, LIKE PYTHON DOES, 
    # WHEN NEAREST FUNCTION RETURNS THE ARRAY INDEX, THIS WILL ALSO
    # BE THE CHANNEL NUMBER
    from Zoldak.General.assortedfunctions import nearest
    EBOUNDS     = numpy.array(list(File['EBOUNDS'].data))
    locEmin     = nearest(EBOUNDS[:,1], float(emin))
    locEmax     = nearest(EBOUNDS[:,2], float(emax))
    print("Lower Channel and Energy:   %i,  %f"%locEmin)
    print("Upper Channel and Energy:   %i,  %f"%locEmax)
    return locEmin[0], locEmax[0]
    


def get_data(en_low, en_up, detector):
    filename    = glob.glob('glg_tte_%s_*.fit'%detector)[0]
    f           = pyfits.open(filename)
    trig        = f[0].header['TRIGTIME']
    PHA         = list(f['EVENTS'].data['PHA'])
    TIME        = list(f['EVENTS'].data['TIME'])
    ch_cuts     = get_channels(f, en_low, en_up)
    # STORE DATA IN A PANDAS DATAFRAME.
    PHAdata     = pd.DataFrame(zip(TIME,PHA), 
                               columns = ['TIME','PHA'])
    # CHANNEL CUTS 
    if ch_cuts is not None: 
        #       CHANNEL CUTS TO 50-300 keV
        PHAdata     = PHAdata[PHAdata.PHA.between(ch_cuts[0],
                                                  ch_cuts[1])]
    
    ttarray        = numpy.asarray(PHAdata.TIME)
    ttarray        = numpy.unique(ttarray) # REMOVE IDENTICAL COPIES.
    ttarray.sort()
    return ttarray, trig
    


def get_bkg_rates(time_array, binwidth, polyorder, bkgIntervals): 
    '''
    get_bkg_rates(time_array, binwidth, polyorder, bkgIntervals): 
    
    time_array:     array of times from raw TTE data.
    binwidth:       exposure, typically 0.064 seconds.
    polyorder:      order of polynomial, 0 is typically fine.
    bkgIntervals:   list or array of background intervals, not in MET times.
                    will be turned into MET times within function.
    
    Returns:  array of background rates from the polyfit
    
    '''
    print(binwidth, polyorder)
    from scipy import polyfit, polyval
    BI          = numpy.asarray(bkgIntervals)
    print(BI)
    
    # BIN DATA FIRST
    time_array  = numpy.asarray( time_array )
    start       = time_array[0]
    stop        = time_array[-1]
    Times       = numpy.arange(start, 
                               stop + binwidth,
                               binwidth)
                               
    Rates, nPha = [0],[]
    for i,j in enumerate(Times[:-1]):
        nPha = len( time_array[(time_array < Times[i+1]) & (time_array > Times[i])])
        Rates.append( nPha / binwidth )

    data0       = pd.DataFrame(zip(Times[1:], Rates[1:]), 
                                columns = ['Times','Rates'])
    before      = data0[data0.Times.between(BI[0], BI[1])] # BEFORE BURST
    after       = data0[data0.Times.between(BI[2], BI[3])] # AFTER BURST
    bkgData     = before.merge(after, how='outer') # BACKGROUND DATA
    
    # Fit bkg with Polynomial
    polyresults    = polyfit(bkgData.Times, bkgData.Rates, polyorder)
    bkgRates       = polyval(polyresults, Times)
    bkgSubRates    = Rates - bkgRates
    #plt.figure(figsize=(11,7))
    #plt.step(Times[1:], Rates[1:], color='blue', alpha=0.4)
    #plt.plot(Times[1:], bkgRates[1:], color='black', linestyle='--', lw=2)
    #plt.xlim(Times.min(), Times.max())
    #plt.ylim(min(Rates[1:]), max(Rates[1:]))
    #plt.show()
    plt.figure(figsize=(11,7))
    plt.step(Times[1:], bkgSubRates[1:], color='blue', alpha=0.4)
    plt.hlines(0, Times.min(),  Times.max(), color='black', linestyle='-', lw=2)
    plt.xlim(Times.min(), Times.max())
    plt.ylim(min(bkgSubRates[1:]), max(bkgSubRates[1:]))
    plt.ylabel('cts/s')
    plt.xlabel('Time (s)')
    plt.title('%r'%(energies[n] ))
    plt.show()
    return Times[1:], numpy.array(Rates[1:]), numpy.array(bkgRates[1:]), numpy.array(bkgSubRates[1:]), polyresults
    






#%%


  
#               BEGIN MAIN PROGRAM

burst           = 'bn130518580' #'bn080916009'
det             = ['n3', 'n7']
basedir         = '/Users/KimiZ/GRBs2/python_modeling/'
direc           = '/Users/KimiZ/GRBs/analysis/%s/integrated/'%burst
outdir          = '/Users/KimiZ/GRBs2/analysis/LAT/%s/integrated/'%burst
os.chdir(direc)

savefig         = True

exposure        =  0.1        # 0.064
t_cuts          =  [5, 50]    #[-5, 60]

#energies        = [[8., 50.], [50., 300.], [300., 900.], [8.,900.]]
energies        = [[8., 900.], [50., 300.], [300., 900.], [8.,900.]]
background      = [-200, -25, 100, 200]

#energies      = [[8., 50.], [50., 100.], [100.,300.], [300., 900.], [8.,900.]]
#energies      = [[150., 900.], [100.,150.], [50., 100.],[8., 50.]]
#energies      = [[300., 900.], [250.,300.], [200.,250.], [150.,200.], [100.,150.], [50., 100.], [8., 50.]]
#energies      = [[8.,25.], [25.,50.], [50.,75.], [75.,100.], [100.,300.], [300.,900.]]
#background    = [-20, -5, 100, 200]





srt,stp = [],[]
lc  = [0]*len(energies)
n   = 0

for energy in energies:
    d,trigtime      = get_data(energy[0], energy[1], det)
    lc[n]           = d
    srt.append(d[0])
    stp.append(d[-1])
    n               = n+1
    
bkgStrt     = max(srt)
bkgStop     = min(stp) 

if len(background) < 4:
    bkgInt      = numpy.array([bkgStrt, background[0]+trigtime, background[1]+trigtime, bkgStop])
else:
    bkgInt      = numpy.array([background[0]+trigtime, background[1]+trigtime, 
                               background[2]+trigtime, background[3]+trigtime])






minR, maxR  = [],[]
times       = [0]*len(lc)
rates       = [0]*len(lc)
verts       = [0]*len(lc)
zs          = range(1, len(lc)+1)

n = 0
for l in lc:
    T, R, bR, bsR, polyRes = get_bkg_rates(time_array=l, binwidth=exposure, polyorder=1, bkgIntervals=bkgInt)
    T = T - trigtime # GET TIME RELATIVE TO TRIGGER
    k = list(zip(T, bsR)) 
    data        = []
    data        = pd.DataFrame(k, columns=['Times', 'Rates'])
    data        = data[data.Times.between(t_cuts[0], t_cuts[1])] # CUT DOWN LC IN TIME
    minR.append(min( list(data.Rates)) )
    maxR.append(max( list(data.Rates)) )
    verts[n]    = list(zip(data.Times, data.Rates))
    n = n+1

maxRate     = max(maxR)
minRate     = min(minR)




#if len(verts) <= 5:
#    colors =  'purple,blue,green,yellow,orange,red'.split(',')[0:len(verts)]
#else:    
#    colors =  'plum,purple,blue,green,yellow,orange,red'.split(',')[0:len(verts)]
#    
#n = 0
#for en in energies:
#    print('%s:  %i - %i'%(colors[n],  int(en[0]), int(en[1])  ))
#    n=n+1   


   
#%%


colors = ['orange', 'red', 'green', 'blue']
    
fig     = plt.figure(figsize=(12,6))
ax      = fig.gca(projection='3d')
poly    = PolyCollection(verts, facecolors=colors)
poly.set_alpha(0.3)
ax.add_collection3d(poly, zs=zs, zdir='y')

ax.set_xlim3d(t_cuts[0], t_cuts[1])
ax.set_ylim3d(0, len(verts)+1)      #(1, len(verts))
ax.set_zlim3d(minRate, maxRate)

ax.set_xlabel('Time Since Trigger (s)', fontsize=14)
ax.set_ylabel('NaI Energy Bandpass', fontsize=14)
ax.set_zlabel('cts/s', fontsize=14)
ax.set_title('%s'%(burst), fontsize=18)

plt.yticks(range(1, len(verts)+1), ['']*len(verts))
plt.tick_params(axis=u'x', pad=0.5)
#plt.yticks([1,2,3,4], ['8-50 keV','50-300 keV','300-900 keV','8-900 keV'])
#ax2.set_yticks([1,2,3,4], ['8-50','50-300','300-900','8-900'])

n=0
for en in energies:
    ax.text(t_cuts[1]-5, n+1, maxRate-500,
        "%i-%i keV"%(int(en[0]), int(en[1])),
        color=colors[n], fontsize=14)
    n=n+1

ax.view_init(elev=30., azim=-135) # ANGLE OF PLOT

if savefig == True:
    import pickle
    pickle.dump(fig, open( os.path.join(outdir,'%s_3dNaIlightcurve.fig.pickle'%burst), 'wb'))
else:
plt.show()


#output = open('interactive_figure.pickle', 'wb')
#pickle.dump(fig.gca(), output)
#output.close()
#
#
#input = open('interactive_figure.pickle', 'r')
#kz = pickle.load(input)





