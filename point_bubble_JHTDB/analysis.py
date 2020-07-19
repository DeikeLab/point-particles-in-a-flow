# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 11:55:39 2020

@author: ldeike
"""

import numpy as np
import pickle
from point_bubble_JHTDB import model

def get_hist(y,bins=1001):
    '''return a normalized pdf and x locs of bin centers'''
    hist,edges = np.histogram(y[~np.isnan(y)],bins=bins,density=True)
    return edges[:-1]+np.diff(edges)/2, hist

def get_rot_dirs(g_dir):
    '''get vectors denoting the new x,y,z directions wrt the DNS coordinate system'''
    
    # z is in the direction of gravity
    z_dir = g_dir.copy()
    
    # x direction has to be normal to z, and we arbitrarily choose it's also normal to the DNS x
    x_dir_unscaled = np.cross(z_dir,[1,0,0])
    x_dir = x_dir_unscaled / np.linalg.norm(x_dir_unscaled)
    
    # get the y direction
    y_dir = np.cross(z_dir,x_dir)
    

def rot_coord_system(arr,g_dir):
    '''
    coordinate system rotation to align z with gravity, just for a single bubble.
    '''

    # z is in the direction of gravity
    z_dir = g_dir.copy()
    
    # x direction has to be normal to z, and we arbitrarily choose it's also normal to the DNS x
    x_dir_unscaled = np.cross(z_dir,[1,0,0])
    x_dir = x_dir_unscaled / np.linalg.norm(x_dir_unscaled)
    
    # get the y direction
    y_dir = np.cross(z_dir,x_dir)
    
    arr_rot = np.array([np.dot(arr,x_dir),np.dot(arr,y_dir),np.dot(arr,z_dir)]).T

    return arr_rot

def rot_all(arrs,g_dirs):    
    '''
    rotate the coordinate systems for all n_b bubbles (along axis 1). 
    
    arrs has shape (n_t,n_b,3); g_dirs has shape (n_b,3)
    '''

    arrs_new = []
    for i in np.arange(len(g_dirs)):
        arrs_new.append(rot_coord_system(arrs[:,i,:],g_dirs[i,:]))        
    arrs_new = np.moveaxis(np.array(arrs_new),0,1)
    return arrs_new

def load_case(d,calc_forces=False):
    
    if isinstance(d,str):
        with open(d, 'rb') as handle:
            res = pickle.load(handle)
    else:
        res = d
        
    # rotate the velocities and position
    res['v'] = rot_all(res['v'],res['g_dir'])
    res['u'] = rot_all(res['u'],res['g_dir'])
    res['x'] = rot_all(res['x'],res['g_dir'])
    
    # get vorticity in DNS coords then rotate
    vort_DNS_coords = get_vorticity(res['velgrad'])
    res['vort'] = rot_all(vort_DNS_coords,res['g_dir'])
    
    # calculate the slip velocity
    res['slip'] = res['v']-res['u']
    
    # see which points to consider (after initial transient)
    res['cond'] = res['t']>model.T_int*2
    
    return res
    
    #if calc_forces:
        
# '''
# Functions like those in model.py
# '''
    
def get_vorticity(velgrad):
    vort = np.zeros((len(velgrad),3)) # 
    velgrad_shape = np.shape(velgrad)
    vort_shape = velgrad_shape[:-1]
    vort = np.zeros(vort_shape)
    vort[...,0] = velgrad[...,2,1] - velgrad[...,1,2]
    vort[...,1] = velgrad[...,0,2] - velgrad[...,2,0]
    vort[...,2] = velgrad[...,1,0] - velgrad[...,0,1]
    return vort