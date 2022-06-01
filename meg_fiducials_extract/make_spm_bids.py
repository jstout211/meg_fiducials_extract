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
from meg_fiducials_extract.spm_fid import main as get_spm_fids
from mne_bids import BIDSPath, write_anat, write_raw_bids

logger = logging.Logger('logger')

def write_mri_spm_bids(sub=None, 
                   ses=None, 
                   t1_fname=None,
                   bids_dir=None):
    if not os.path.exists(bids_dir): os.mkdir(bids_dir)
                   
    # First create the BIDSPath object.
    t1w_bids_path = BIDSPath(subject=sub, session=ses, root=bids_dir,
                             suffix='T1w')
    
    #Extract fiducial information from spm mat file in NII voxels
    spm_fids = get_spm_fids(spm_meg_fname, t1_fname, orig_meg_fname)
    landmarks = mne.channels.make_dig_montage(
            lpa=spm_fids['lpa'],
            nasion=spm_fids['nas'],
            rpa=spm_fids['rpa'],
            coord_frame='mri_voxel')
    
    # << Code snippet from mne_bids >>
    # We use the write_anat function
    t1w_bids_path = write_anat(
        image=t1_fname,  # path to the MRI scan
        bids_path=t1w_bids_path,
        landmarks=landmarks,  # the landmarks in MRI voxel space
        verbose=True  # this will print out the sidecar file
    )

# =============================================================================
# Need to fill in - this is from another script
# =============================================================================
def process_meg_bids(input_path=None, bids_dir=None, session=1):
    '''
    Process the MEG component of the data into bids.
    Calls sessdir2taskrundict to get the task IDs and sort according to run #
    Output is the data in bids format in the assigned bids_dir
    
    !Warning - this does not parse the events from your dataset
    !Use parse marks or other tools -  preferably before doing the bids proc.

    Parameters
    ----------
    input_path : str, optional
        Path to the MEG folder - typically designated by a Date.
    bids_dir : str, optional
        Output path for your bids data.
    session : int
        Session number for data acquisition.  Defaults to 1 if not set

    Returns
    -------
    None.

    '''
    if bids_dir==None:
        raise ValueError('No bids_dir output directory given')
    if not os.path.exists(bids_dir): os.mkdir(bids_dir)
    dset_dict = sessdir2taskrundict(session_dir=input_path)
    
    session = str(session)
    if len(session)==1: session = '0'+session
    
    error_count=0
    for task, task_sublist in dset_dict.items():
        for run, base_meg_fname in enumerate(task_sublist, start=1):
            meg_fname = op.join(input_path, base_meg_fname)
            try:
                subject = op.basename(meg_fname).split('_')[0]
                raw = mne.io.read_raw_ctf(meg_fname, system_clock='ignore')  
                raw.info['line_freq'] = 60 
                
                ses = session
                run = str(run) 
                if len(run)==1: run='0'+run
                bids_path = BIDSPath(subject=subject, session=ses, task=task,
                                      run=run, root=bids_dir, suffix='meg')
                write_raw_bids(raw, bids_path, overwrite=True)
                logger.info(f'Successful MNE BIDS: {meg_fname} to {bids_path}')
            except BaseException as e:
                logger.exception('MEG BIDS PROCESSING:', e)
                error_count+=1
    if error_count > 0:
        logger.info(f'There were {error_count} errors in your processing, \
                    check the error log for more information')  #!!! print the error log location
    else:
        logger.info('SUCCESS: There were no errors!')
    

      
        
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='''Extract the positions of the fiducials from the SPM
        mat file and invert the transform to get the original locations of the
        fiducials relative to the input nifti image''')
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
                        help='''The original dataset in:
                            CTF, MEGIN, 4D, or KIT/Ricoh format
                        ''',
                        required=True)
    parser.add_argument('-line_freq', 
                        help='Frequency of electrical power 50 or 60Hz')
    
    args = parser.parse_args()
    
    fid_dict = get_spm_fids(
        spm_meg_fname=args.spm_mat, 
        nii_fname=args.t1w_nii, 
        orig_meg_fname=args.orig_meg)
    
    print(fid_dict)
    
    
    
    

