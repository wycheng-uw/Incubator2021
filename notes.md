# Lightning Incubator

### Instructions for JupyterLab on department server

** This assumes you have an account on [UW Atmospheric Sciences](https://atmos.uw.edu) "Pynchon" server **

1. Set up a SSH RSA key pair to skip typing a password every time
```
# On your laptop
ssh-keygen -t rsa
# use empty passphrase
ssh-copy-id USERNAME@pynchon.atmos.washington.edu
# type your password
# now connect to Pynchon via key rather than password:
ssh -Y USERNAME@pynchon.atmos.washington.edu
```

1. Switch to bash shell from default tcsh
```
# add these two lines to the end of ~/.login
setenv SHELL /bin/bash
exec /bin/bash
```

1. set up a miniconda for managing custom python environments in your home directory
```
# chose your miniconda installer from https://github.com/conda-forge/miniforge/releases
wget https://github.com/conda-forge/miniforge/releases/download/4.9.2-5/Miniforge3-Linux-x86_64.sh
bash Miniforge3-Linux-x86_64.sh
# NOTE: to default to activating a conda environment you might have to run:
#-> eval "$(/home/disk/eos1/scottyh/miniforge3/bin/conda shell.bash hook)"
#-> conda init
## when you login you should see:
## (base) bash-4.1$ which conda
## /home/disk/eos1/USER/miniforge3/bin/conda
```

1. create a conda environment
```
# Note this can take some time for NFS drives
conda create -n jlab python=3 jupyterlab
# or conda env create -f incubator2021.yml
```

1. start jupyterlab on pynchon
```
conda activate jlab
jupyter lab --no-browser --port=9001
#You will see a message like:
# Or copy and paste one of these URLs:
#http://localhost:9001/lab?token=f622febbd9d93afb677ef29b4f67a1f5cf1e9c6b6ecc
```

1. connect to jupyterlab running on Pynchon from your laptop
```
ssh -N -L localhost:9001:localhost:9001 USER@pynchon.atmos.washington.edu
# open a browser with http://localhost:9001/lab for the lab interface
# copy token reported on pynchon to connect to jupyterlab
```

#### Other notes
```
# what is the OS on pynchon?
lsb_release -a
# Description:	CentOS release 6.10 (Final)

# NOTE this is pretty old 2017-08, so some software versions are obsolete, such as git:
# can lead to errors such as "error: The requested URL returned error: 403 Forbidden while accessing"
git --version
# 1.7.1
# can create a new conda environment with the latest git version:
conda create -n git git

# default shell?
echo $SHELL
#/bin/tcsh

# configure git to access private repositories
# https://docs.github.com/en/github/using-git/setting-your-username-in-git
# https://docs.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
# https://docs.github.com/en/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account
```
