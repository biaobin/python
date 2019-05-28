'''
Created on 05.28.2019
@author: Biaobin Li

Usage:
biaobin's python scripts libraries for plotting functions.
'''

import numpy as np
import matplotlib.pyplot as plt

def zdgamplot(z, dgam, filename='energydev.png'):
    """
    2D heat plot for (z,dgam) phase space.
    z,    [m]
    dgam, [1] 
    by default save as energydev.png
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

    
	


