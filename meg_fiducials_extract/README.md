
## MEG Research Software
Brainstorm:
- Current brainstorm version provides export of raw meg data into BIDS (experimental feature) - but does not generate the anatomy json
- make_bstorm_json.py adds the fiducials into the anat T1w.json file
```
meg_fiducials_extract/meg_fiducials_extract/make_json_bstorm.py -h 
usage: make_json_bstorm.py [-h] [-bids_root BIDS_ROOT] [-bids_id BIDS_ID]
                           [-bst_id BST_ID] [-bst_datapath BST_DATAPATH]

Use the brainstorm data to generate the NAS,LPA,RPA locations and add them to the
T1w.json file in the bids directory for the subject

optional arguments:
  -h, --help            show this help message and exit
  -bids_root BIDS_ROOT
  -bids_id BIDS_ID      Subject bids_id in the bids_root
  -bst_id BST_ID        Brainstorm subject ID
  -bst_datapath BST_DATAPATH
                        Path to Brainstorm Protocol data folder

```

SPM: 
- Does not currently export to bids
- Commands to extract coregistration from spm .mat file and generate bids
```
meg_fiducials_extract/meg_fiducials_extract/make_spm_bids.py -h 
usage: make_spm_bids.py [-h] -t1w_nii T1W_NII -spm_mat SPM_MAT -orig_meg ORIG_MEG
                        [-line_freq LINE_FREQ]

Extract the positions of the fiducials from the SPM mat file and invert the transform to
get the original locations of the fiducials relative to the input nifti image

optional arguments:
  -h, --help            show this help message and exit
  -t1w_nii T1W_NII      Original T1w nifti image used for coregstration in SPM
  -spm_mat SPM_MAT      The SPM .mat file that was used in the coregistration. This data
                        must have an inverse model performed in order for this script to
                        work.
  -orig_meg ORIG_MEG    The original dataset in: CTF, MEGIN, 4D, or KIT/Ricoh format
  -line_freq LINE_FREQ  Frequency of electrical power 50 or 60Hz

```


Fieldtrip:
- Exports to BIDS:
- data2bids.m -- https://github.com/fieldtrip/fieldtrip/blob/release/data2bids.m
- example: https://www.fieldtriptoolbox.org/example/bids_audio/

MNE: 
- Straightforward export to BIDS

## VENDOR Software:
MEGIN:
- TODO: get coreg and fiducials  in voxel format and nifti.

CTF:
- TODO: get coreg and fiducials  in voxel format and nifti.

RICOH/KIT:
- TODO: get coreg and fiducials  in voxel format and nifti.

4D:
- TODO: get coreg and fiducials  in voxel format and nifti.
