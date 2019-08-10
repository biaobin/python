'''
Created on 05.28.2019
@author: Biaobin Li

Usage:
biaobin's python scripts libraries for plotting functions.
'''


#============================================
# plot library
#============================================
import numpy as np
import matplotlib.pyplot as plt

def zdgamplot(z, dgam, filename='energydev.png'):
    """
    2D heat plot for (z,dgam) phase space.
    z,    [m]
    dgam, [1] 
    by default save as energydev.png
    for ImpactZ -2 output, X[:,4] is -z, X[:,5] is -dgam
    """
    z    = z*1e3           #[mm]
    dgam = dgam*0.511001   #[MeV] 
   
    plotsetting()
    plt.hexbin(z, dgam, gridsize=(256,256), mincnt=1, cmap=plt.cm.jet)
    plt.xlabel('z (mm)')
    plt.ylabel('energy deviation (MeV)')
    plt.colorbar()
#     plt.colorbar().ax.tick_params(labelsize=18-2)
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()

def plot2d(x, y, xlabel='x (mm)', ylabel='y (mm)', filename='xy.png'):
    """
    2D heat plot for (x,y) phase space.
    usage:
    blt.plot2d(X[:,4]*1e3, X[:,0]*1e3, xlabel='z (mm)', ylabel='x (mm)', filename='zx.png')
    """
    
    plotsetting()
    plt.hexbin(x, y, gridsize=(256,256), mincnt=1, cmap=plt.cm.jet)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.colorbar()
#     plt.colorbar().ax.tick_params(labelsize=18-2)
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()
    
def plotsetting():
    """
    font settings.
    """ 
    fsz = 18
    plt.style.use('classic')
    plt.rcParams.update({'font.size': fsz})    
#   mpl.rcParams['font.size'] = str(fsz)
#   mpl.rcParams['xtick.direction'] = 'in'
#   mpl.rcParams['ytick.direction'] = 'in'


#============================================
# distribution generation
#============================================
def genHaltonTrans(infile,rb,flag='both'):
    """
    replace the transverse gaussian distribution genrated by elegant
    smoothDis6 with uniform cross circle distribution.
    usage:
    import sys
    sys.path.append("/Users/biaobin/scripts/python")
    
    import bblib as bl
    bl.genHaltonTrans(infile='partcl.data',rb=0.4e-3)
    """
    import ghalton as gt
    import sys
    
    #M = np.loadtxt(infile,skiprows=1)
    # do not skip first line now, as elegant2impactz "Np 0 0" line is commented
    M = np.loadtxt(infile)
    #particle number
    Np = np.shape(M)[0]
    
    #skip the first 1e4 rows, as Kilean said
    startFrom = int(1e4) 
    seq = gt.Halton(4) 
    X0  = np.array(seq.get(Np+startFrom))

    # transform to cross circle distribution
    r = rb*np.sqrt(X0[startFrom:,1])
    theta = 2*np.pi*X0[startFrom:,3]
    
    # replace the x and y with halton uniform distribution
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    M[:,0] = x
    M[:,2] = y
    
    # prepare for writing into new file
    # first line of particle number
    line1 = np.array([Np,0,0])
    
    if flag == 'both':
        # quad on
        # ========
        f = open(infile+'.quadON','w')
        saveformat = '%22.15e %22.15e %22.15e %22.15e \
        %22.15e %22.15e %22.15e %22.15e %d'
        np.savetxt(f,line1.reshape((1,3)),fmt='%d')
        np.savetxt(f,M,fmt=saveformat)
        f.close()

        # quad off
        # ========
        M[:,1] = 0; #set px=py=0
        M[:,3] = 0;
        f = open(infile+".quadOFF",'w')
        np.savetxt(f,line1.reshape((1,3)),fmt='%d')
        np.savetxt(f,M,fmt=saveformat)
        f.close()
    elif flag == 'quadon':       
        # quad on
        # ========
        f = open(infile+'.quadON','w')
        saveformat = '%22.15e %22.15e %22.15e %22.15e \
        %22.15e %22.15e %22.15e %22.15e %d'
        np.savetxt(f,line1.reshape((1,3)),fmt='%d')
        np.savetxt(f,M,fmt=saveformat)
        f.close()
    elif flag == 'quadoff':
        # quad off
        # ========
        M[:,1] = 0; #set px=py=0
        M[:,3] = 0;
        f = open(infile+".quadOFF",'w')
        np.savetxt(f,line1.reshape((1,3)),fmt='%d')
        np.savetxt(f,M,fmt=saveformat)
        f.close()
    else:
        sys.exit("error, flag should be either {both,quadon,quadoff}")
        
            
    
