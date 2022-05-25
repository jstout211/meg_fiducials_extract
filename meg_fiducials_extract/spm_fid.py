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
import os.path as op
import os
import logging

logger = logging.Logger('logger')

# from scipy.io import loadmat
# import matlab.engine 
# eng = matlab.engine.start_matlab()

# fname = 'espmeeg_APBWVFAR_airpuff_20200122_05.mat'
# Obj = eng.load(fname, '-mat', 'D')       #['inverse'] #['lib']
# Names = eng.getfield(Obj, 'name')
# Strs = eng.getfield(Obj, 'structures')
# StrLists = eng.getfield(Obj, 'structlist')

# =============================================================================
# SPM does not work with the typical scipy loadmat or matlab python engine
#
# To extract matlab structure
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

def _confirm_inputs(spm_meg_fname=None, 
                    nii_fname=None, 
                    orig_meg_fname=None):
    '''
    Verify that everything is in order for processing

    Parameters
    ----------
    spm_meg_fname : TYPE, optional
        DESCRIPTION. The default is None.
    nii_fname : TYPE, optional
        DESCRIPTION. The default is None.
    orig_meg_fname : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    None.

    '''
    if not op.exists(spm_meg_fname):
        logger.exception(f'No file found: {spm_meg_fname}')
    if not op.exists(orig_meg_fname):
        logger.exception(f'No file found: {orig_meg_fname}')

    # NEED to put in data reader section for MNE
    #<<<>>>
    
    #Load SPM meg matrix
    try:
        tmp_ = loadmat(spm_meg_fname)
        D = tmp_['D']
    except BaseException() as e:
        logger.exception(f'Could not properly load: {spm_meg_fname} \n {e}')
        
    #Does the dataset have an inverse solution
    try:
        _inv_struct = D['other']['inv']
    except:
        try:
            _inv_struct = D['inv']
        except BaseException() as e:
            logger.exception(f'''Could not load the inv data structure - 
                             Does your data have an inverse solution?
                             \n\n {e}''')
    
    #Try to access the necessary variables
    try:
        _aff = _inv_struct['mesh']['Affine']
    except BaseException() as e:
        logger.exception(f'''Could not load the affine matrix''')

    try:
        _datareg = _inv_struct['datareg']['toMNI']
    except BaseException() as e:
        logger.exception(f'''Could not load the coregistration''')
    
    try:
        _mri_fids = _inv_struct['datareg']['fid_mri']['fid']
        _label = _mri_fids['label'] 
        _pnt = _mri_fids['pnt'] 
        # spm_fids = {i:j for i,j in zip(_label, _pnt)}
    except BaseException() as e:
        logger.exception(f'''Could not load the fiducials''')
        
    return _aff, _datareg, _label, _pnt


def main(affine=None,
         coreg=None, 
         spm_fid_label=None, 
         spm_fid_pnt=None, 
         nii_fname=None):
    
    inv_mat = np.linalg.inv(affine) @ coreg
    origMR_pnts = apply_trans(inv_mat, spm_fid_pnt)
    
    fids_orig_mm = {i:j for i,j in zip(spm_fid_label, origMR_pnts)}
    fids_orig_vox = convert2vox(nii_fname, fids_orig_mm)
    return fids_orig_vox
    
        


                             
        
        
    
    
    




# spm_meg_fname='espmeeg_APBWVFAR_airpuff_20200122_05.mat'
# nii_fname = '/fast/OPEN/APBWVFAR/APBWVFAR.nii'
# mr_obj = nb.load(nii_fname)



# #MRI locations
# # D.other.inv{1}.datareg.fid_mri.fid.pnt
# # mri_fids =  D['other']['inv']['datareg']['fid_mri']['fid']

# _label = mri_fids['label'] 
# _pnt = mri_fids['pnt'] 
# fids = {i:j for i,j in zip(_label, _pnt)}

# =============================================================================
# Get fids from SPM - from SPM listserve
# apply D.inv{val}.mesh.Affine\D.inv{val}.datareg.toMNI
# to D.inv{val}.datareg.fid_mri.fid.fid.pnt
# =============================================================================


# inv_mat = np.linalg.inv(D['other']['inv']['mesh']['Affine']) @ \
#     D['other']['inv']['datareg']['toMNI']
# origMR_pnts = apply_trans(inv_mat, _pnt)

# fids_orig_mm = {i:j for i,j in zip(_label, origMR_pnts)}
# fids_orig_vox = convert2vox(nii_fname, fids_orig_mm)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-t1w_nii',
                        help='''Original T1w nifti image used for coregstration
                        in SPM''',
                        required=True)
    parser.add_argument('-spm_mat',
                        help='''The SPM .mat file that was used in the 
                        coregistration.  This data must have an inverse model
                        performed in order for this script to work.''',
                        required=True)
    parser.add_argument('-orig_meg', 
                        help='''The original dataset (CTF, MEGIN, 4D, KIT/Ricoh
                        ''',
                        required=True)
    parser.add_argument('-line_freq', 
                        help='Frequency of electrical power 50 or 60Hz')
    
    args = parser.parse_args()
    
    affine, coreg, fid_label, fid_pnt = _confirm_inputs(
        spm_meg_fname=args.spm_mat, 
        nii_fname=args.t1w_nii, 
        orig_meg_fname=args.orig_meg)
    
    fid_dict = main(affine=affine,
                     coreg=coreg, 
                     spm_fid_label=fid_label, 
                     spm_fid_pnt=fid_pnt, 
                     nii_fname=args.t1w_nii)
    print(fid_dict)
    
    
    
    

