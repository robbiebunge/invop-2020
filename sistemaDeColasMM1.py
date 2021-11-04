#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 12 13:34:04 2021

@author: robbiebunge
"""


import numpy as np
import matplotlib.pyplot as plt

# np.random.seed(0)

landa = 20
mu = 10

nSim = 100

nPersonas = np.zeros(nSim)
nPersonasCola = np.zeros(nSim)
tTicks = np.zeros(nSim)
eventos = ['None'] * nSim
serverDisponible = [False] * nSim
eventos[0] = 'arribo'
tProximoServicio = np.Inf
serverDisponible[0] = True

for i in range(nSim-1):
    
    if eventos[i] == 'arribo':
        nPersonas[i+1] = nPersonas[i] + 1
        if serverDisponible[i] == True:
            tProximoServicio = tTicks[i] + np.random.exponential(1/mu)
        else:
            nPersonasCola[i+1] = nPersonasCola[i] + 1
        serverDisponible[i+1] = False
        tProximoArribo = tTicks[i] + np.random.exponential(1/landa)
        
    if eventos[i] == 'servicio':
        serverDisponible[i+1] = True
        nPersonas[i+1] = nPersonas[i] - 1
        tProximoServicio = np.Inf
        if nPersonasCola[i] > 0:
            nPersonasCola[i+1] = nPersonasCola[i] - 1
            serverDisponible[i+1] = False
            tProximoServicio = tTicks[i] + np.random.exponential(1/mu)
    
    if tProximoArribo < tProximoServicio:
        proximoEvento = 'arribo'
        tProximoEvento = tProximoArribo
    else:
        proximoEvento = 'servicio'
        tProximoEvento = tProximoServicio
        
    tTicks[i+1] = tProximoEvento
    eventos[i+1] = proximoEvento
            

plt.figure()
plt.step(tTicks,nPersonas)
plt.xlabel('Tiempo (min)')
plt.ylabel('Numero de personas')
plt.show()

    
    