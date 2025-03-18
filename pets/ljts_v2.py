# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

#%% Convert Gibbs free energy from PeTS to ms2 value
def g_PeTS2ms2(g_pets, T, rho):
    '''
    Convert Gibbs free energy from PeTS to ms2 value
    
    :param float g_pets: Gibbs free energy from PeTS
    :param float T: Temperature
    :param float rho: Density
    :return: float g_ms2: Gibbs free energy from ms2
    '''
    
    rhocrit = 0.319
    Tcrit   = 1.086
    delta0 = (0.001/0.8)/rhocrit
    tau0   = Tcrit/0.8
    ig1 = -2.5/tau0  # Originally in PeTS: -2.5/tau0
    ig2 = 1.5 - np.log(delta0) - 1.5*np.log(tau0)
    tau   = Tcrit/T
    delta = rho/rhocrit
    alphaId = np.log(delta) + 1.5*np.log(tau) + ig1*tau + ig2
    g_res = g_pets/T - 1.0 - alphaId
    g_ms2 = g_res + np.log(rho)
    return g_ms2


#%% Convert Gibbs free energy from ms2 to PeTS value
def g_ms22PeTS(g_ms2, T, rho):
    '''
    Convert Gibbs free energy from ms2 to PeTS value
    
    :param float g_ms2: Gibbs free energy from ms2
    :param float T: Temperature
    :param float rho: Density
    :return: float g_pets: Gibbs free energy from PeTS
    '''
    
    rhocrit = 0.319
    Tcrit   = 1.086
    delta0 = (0.001/0.8)/rhocrit
    tau0   = Tcrit/0.8
    ig1 = -2.5/tau0  # Originally in PeTS: -2.5/tau0
    ig2 = 1.5 - np.log(delta0) - 1.5*np.log(tau0)
    tau   = Tcrit/T
    delta = rho/rhocrit
    alphaId = np.log(delta) + 1.5*np.log(tau) + ig1*tau + ig2
    g_res = g_ms2 - np.log(rho)
    g_pets = T*(1.0 + alphaId + g_res)
    return g_pets


if __name__ == "__main__":
    
    value = -3.28166
    rho = 0.72
    T = 0.88
    pets2ms2 = False
    if pets2ms2 == True:
        print(g_PeTS2ms2(value,T,rho))
    else:
        print(g_ms22PeTS(value,T,rho))
    