#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 23 09:40:49 2022

@author: jstout
"""
import mne
import nibabel as nb
import copy
from mne.transforms import apply_trans
import numpy as np

# from scipy.io import loadmat
# import matlab.engine 
# eng = matlab.engine.start_matlab()

# fname = 'espmeeg_APBWVFAR_airpuff_20200122_05.mat'
# Obj = eng.load(fname, '-mat', 'D')       #['inverse'] #['lib']
# Names = eng.getfield(Obj, 'name')
# Strs = eng.getfield(Obj, 'structures')
# StrLists = eng.getfield(Obj, 'structlist')

# =============================================================================
# >>> Code from https://stackoverflow.com/questions/7008608/scipy-io-loadmat-nested-structures-i-e-dictionaries
# =============================================================================

import scipy.io as spio
def loadmat(filename):
    '''
    this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    '''
    data = spio.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)

def _check_keys(dict):
    '''
    checks if entries in dictionary are mat-objects. If yes
    todict is called to change them to nested dictionaries
    '''
    for key in dict:
        if isinstance(dict[key], spio.matlab.mio5_params.mat_struct):
            dict[key] = _todict(dict[key])
    return dict        

def _todict(matobj):
    '''
    A recursive function which constructs from matobjects nested dictionaries
    '''
    dict = {}
    for strg in matobj._fieldnames:
        elem = matobj.__dict__[strg]
        if isinstance(elem, spio.matlab.mio5_params.mat_struct):
            dict[strg] = _todict(elem)
        else:
            dict[strg] = elem
    return dict

# =============================================================================
# <<<< End of Stackoverflow code
# =============================================================================

def convert2vox(t1_fname, coords_dict):
    t1 = nb.load(t1_fname)
    t1_mgh = nb.MGHImage(t1.dataobj, t1.affine)
    
    vox_coords = copy.deepcopy(coords_dict)
    for fid in vox_coords.keys():
        tmp_ = apply_trans(t1_mgh.header.get_ras2vox(), coords_dict[fid])
        vox_coords[fid] = list(tmp_)
    return vox_coords

spm_meg_fname='espmeeg_APBWVFAR_airpuff_20200122_05.mat'
nii_fname = '/fast/OPEN/APBWVFAR/APBWVFAR.nii'
mr_obj = nb.load(nii_fname)

#Load spm matrix
tmp_ = loadmat(spm_meg_fname)
D = tmp_['D']

#MRI locations
# D.other.inv{1}.datareg.fid_mri.fid.pnt
# mri_fids =  D['other']['inv']['datareg']['fid_mri']['fid']

_label = mri_fids['label'] 
_pnt = mri_fids['pnt'] 
fids = {i:j for i,j in zip(_label, _pnt)}

# =============================================================================
# Get fids from SPM - from SPM listserve
# apply D.inv{val}.mesh.Affine\D.inv{val}.datareg.toMNI
# to D.inv{val}.datareg.fid_mri.fid.fid.pnt
# =============================================================================


inv_mat = np.linalg.inv(D['other']['inv']['mesh']['Affine']) @ \
    D['other']['inv']['datareg']['toMNI']
origMR_pnts = apply_trans(inv_mat, _pnt)

fids_orig = {i:j for i,j in zip(_label, origMR_pnts)}




