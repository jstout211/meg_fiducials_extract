
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
