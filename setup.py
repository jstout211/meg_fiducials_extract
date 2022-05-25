import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="meg_fiducials_extract", 
    version="0.1.0",
    author="Jeff Stout",
    author_email="stoutjd@nih.gov",
    description="Toolbox of scripts to extract coregistration information from external MEG packages to incorporate with mne_bids processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jstout211/meg_fiducials_extract",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Creative Commons Zero v1.0 Universal",
        "Operating System :: Linux/Unix",
    ],
    install_requires=['mne', 'numpy', 'scipy', 'pandas', 'nibabel', 'pytest', 'joblib'],
    scripts=['meg_fiducials_extract/spm_fid.py'] 
             #'enigmeg/process_anatomical.py'],
)
