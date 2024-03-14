#!/bin/bash
export SCRAM_ARCH=slc7_amd64_gcc11
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /nfs/cms/martialc/Displaced2024/CMSSW_13_0_14/src/
eval `scramv1 runtime -sh`
cd /nfs/cms/martialc/Displaced2024/llp/condor
export PYTHONPATH=$PYTHONPATH:/nfs/cms/martialc/Displaced2024/llp/src
$@
