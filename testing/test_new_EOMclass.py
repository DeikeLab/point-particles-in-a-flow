# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 16:55:07 2021

@author: druth
"""



import point_bubble_JHTDB as pb
from point_bubble_JHTDB import analysis, equations
from point_bubble_JHTDB.velocity_fields import gaussian, two_dimensional
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import toolkit.parallel
import time

#vf = gaussian.RandomGaussianVelocityField(n_modes=64,u_rms=1,L_int=1)
vf = two_dimensional.SteadyPlanarPoiseuilleFlow()
vf.init_field()

d,g = analysis.dg_given_nondim(4, 0.1, vf.u_char, vf.L_char)

phys_params = {'d':d,
                'g':g,
                'Cm':0.5,
                'Cd':1,
                'Cl':0.5}

sim_params = {'n_bubs':1,
              'dt':1e-3,
              't_min':0,
              't_max':4,
              'fname':'inertial'}

eom = equations.MaxeyRileyPointBubbleConstantCoefs()
sim = pb.Simulation(vf,phys_params,sim_params,eom)
sim.init_sim(g_dir='-y')
sim.x[0,0,:] = np.array([0,0.5,0])
sim.v[0,0,:] = np.array([0,-sim.v_q,0])*10
t1 = time.time()
sim.run()
print(time.time()-t1)
a = analysis.CompleteSim(sim,rotated=False)
plt.figure();plt.plot(a['t'],a['x'][:,0,:])
stophere

phys_params = {'d':d,
                'g':g,
                'Cm':0.5,
                'Cd':1.,
                'Cl':0.0}
sim_params = {'n_bubs':1000,
              'dt':1e-3,
              't_min':0,
              't_max':8,
              'fname':'inertial'}
vf = gaussian.RandomGaussianVelocityField(n_modes=64,u_rms=1,L_int=1)
vf.init_field()
eom = equations.MaxeyRileyPointBubbleConstantCoefs()
sim2 = pb.Simulation(vf,phys_params,sim_params,eom)
sim2.init_sim(g_dir='random')
t1 = time.time()
sim2.run()
print(time.time()-t1)
a = analysis.CompleteSim(sim2)
a['v'].mean(axis=(0,1))

phys_params = {}
eom = equations.LagrangianEOM()
sim3 = pb.Simulation(vf,phys_params,sim_params,eom)
sim3.init_sim(g_dir='random')
sim3.x[0,...] = sim.x[0,...].copy()
sim3.g_dir = sim.g_dir.copy()
t1 = time.time()
sim3.run()
print(time.time()-t1)


fig,ax = plt.subplots()
ax.plot(sim.t,sim.x[:,0,:],ls='-')
ax.plot(sim2.t,sim2.x[:,0,:],ls='--')
ax.plot(sim3.t,sim3.x[:,0,:],ls=':')