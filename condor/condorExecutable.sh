#!/bin/bash

export SCRAM_ARCH=slc7_amd64_gcc10
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /nfs/cms/rhebrero/Displaced2023/CMSSW_12_4_5/src/
eval `scramv1 runtime -sh`
cd /nfs/cms/rhebrero/work/analisis

# Activate venv for cmsstyle
source /nfs/cms/rhebrero/py_environments/cmsstyle//bin/activate

$@
