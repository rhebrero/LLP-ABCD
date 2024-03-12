import subprocess
import os 
import argparse
from utils import confirmation

parser = argparse.ArgumentParser(description="Handle to submit lxplus condor jobs, it request a plain file with all the scripts to run.")

#modes
parser.add_argument('--flavour'    , dest='flavour'   , default='longlunch'     , help='which condor job flavour to use')
parser.add_argument('--inputFile'  , dest='input_file', default='jobs.sh'       , help='input file (with scripts to run on)')
parser.add_argument('--use-proxy'  , dest='proxy'     , action='store_true'     , help='whether to ship the GRID certificate with the jobs')
parser.add_argument('--ciemat'     , dest='ciemat'    , action='store_true'     , help='whether to run at CIEMAT (grid GRID combined with certificate untested)')
parser.add_argument('--pnfs'       , dest='pnfs'      , action='store_true'     , help='if running at CIEMAT, additional request machines with access to PNFS')
parser.add_argument('--gaefacil'   , dest='gaefacil'  , action='store_true'     , help='whether to include gaefacilXX machines to available machines')

args = parser.parse_args()

# Check if pnfs is True while ciemat is not
if args.pnfs and (not args.ciemat):
    parser.error("--pnfs requires --ciemat to be set to True")

if args.gaefacil and (not args.ciemat):
    parser.error("--gaefacil requires --ciemat to be set to True")


# Check if pnfs is False while ciemat is True
if (not args.pnfs) and args.ciemat:
    print("WARNING: This submission will only work if you are not reading fron PNFS")
    if not confirmation('is this what you want?'):
        print('Exiting...')
        exit()

if (not args.gaefacil) and args.ciemat:
    print("WARNING: This submission will not run in CIEMAT's Analysis Facility (gaefacil)")
    if not confirmation('is this what you want?'):
        print('Exiting...')
        exit()
  
print (f"running on jobs in {args.input_file}")

# set some global variables needed for submission scripts
CMSSW_BASE   = os.environ['CMSSW_BASE']
SCRAM_ARCH   = os.environ['SCRAM_ARCH']
USER         = os.environ['USER']
HOME         = os.environ['HOME']
PWD          = os.environ['PWD']

# Various literal submission scripts with formatting placeholders for use in submission loops below
# Some format specifiers are global; otherwise ARGS will be set during the loop + format
condorExecutable = "".join([
                        f"#!/bin/bash\n",
                        f"export SCRAM_ARCH={SCRAM_ARCH}\n",
                        f"source /cvmfs/cms.cern.ch/cmsset_default.sh\n",
                        f"cd {CMSSW_BASE}/src/\n",
                        f"eval `scramv1 runtime -sh`\n",
                        f"cd {PWD}\n",
                        f"$@\n"
                    ])

# default script for condor submission in lxplus
condorSubmit = "".join([
                    "universe               = vanilla\n",
                    "executable             = condorExecutable.sh\n",
                    "getenv                 = True\n"
                ])

condorSubmitAdd = "".join([
                        'output                 = logs/run{runNum}/{logname}_{index}.out\n',
                        'log                    = logs/run{runNum}/{logname}_{index}.log\n',
                        'error                  = logs/run{runNum}/{logname}_{index}.err\n',
                        'arguments              = {ARGS}\n',
                        '{proxy_literal}\n',
                        'should_transfer_files  = NO\n',
                        '+JobFlavour            = "{flavour}"\n',
                        'queue 1\n'
                    ])

# modifications needed for CIEMAT submission
if args.ciemat:
    condorSubmit = "executable             = condorExecutable.sh\n"

    if args.pnfs:
       condorSubmit += "".join([
                        'requirements = stringListIMember("DCACHE_NFS", TARGET.WN_property, ",")\n',
                        'request_cpus=4\n'
                        ])
    if args.gaefacil:
        condorSubmit += "".join([
                        '+CieIncludeAF           = True\n',         # Includes Ciemat's Analysis Facility's machines
                        '+CieSingularityImage    = cc7\n'           # CentOS 7
                        ])
    
    condorSubmitAdd = "".join([
                        'output                 = logs/run{runNum}/{logname}_{index}.out\n',
                        'log                    = logs/run{runNum}/{logname}_{index}.log\n',
                        'error                  = logs/run{runNum}/{logname}_{index}.err\n',
                        'arguments              = {ARGS}\n',
                        '{proxy_literal}\n',
                        'queue 1\n'
                    ])

# get rid of empty lines in the condor scripts
# if condorExecutable starts with a blank line, it won't run at all!!
# the other blank lines are just for sanity, at this point
# def stripEmptyLines(string):
#     if string[0] == '\n':
#         string = string[1:]
#     return string

# condorExecutable = stripEmptyLines(condorExecutable)
# condorSubmit     = stripEmptyLines(condorSubmit    )
# condorSubmitAdd  = stripEmptyLines(condorSubmitAdd )
# clipSubmit  = stripEmptyLines(clipSubmit)
# clipSubmitAdd = stripEmptyLines(clipSubmitAdd)

if args.proxy == True:
    # prepare the grid certificate
    proxy = '{HOME}/private/.proxy'.format(**locals())
    if not os.path.isfile(proxy) or int(subprocess.check_output('echo $(expr $(date +%s) - $(date +%s -r {}))'.format(
           proxy), shell=True)) > 6*3600:
        print('GRID certificate not found or older than 6 hours. You will need a new one.')
        subprocess.call('voms-proxy-init --voms cms --valid 168:00 -out {}'.format(proxy), shell=True)
        
    # export the environment variable related to the certificate
    os.environ['X509_USER_PROXY'] = proxy
    
    PROXY_LITERAL = 'x509userproxy = $ENV(X509_USER_PROXY)\\nuse_x509userproxy = true'
else: 
     PROXY_LITERAL = '#'

# make the logs directory if it doesn't exist
subprocess.call('mkdir -p logs', shell=True)

# make executable
executableName = 'condorExecutable.sh'
with open(executableName, 'w') as f:
    f.write(condorExecutable.format(**locals()))

# get the number of run* directories, and make the next one
try:
    numberOfExistingRuns = int(subprocess.check_output('ls -d logs/run* 2>/dev/null | wc -l', shell=True))
except subprocess.CalledProcessError:
    numberOfExistingRuns = 0
runNum = numberOfExistingRuns+1
subprocess.call(f'mkdir logs/run{runNum}', shell=True)


# make the submit file
#work is needed
condorSubmit += '#\n'
    
# get jobs
with open(args.input_file, 'r') as f:
    lines = f.readlines()
for index, line in enumerate(lines):
    line = line.strip()
    
    if (len(line) == 0) or (line[0] == "#"): continue
    condorSubmit += condorSubmitAdd.format(
        runNum        = runNum,
        #logname       = line.split(".")[-1] if line != '' else 'dummy',
        logname       = "job",
        index         = index,
        ARGS          = line,
        flavour       = args.flavour,
        proxy_literal = PROXY_LITERAL
    )
    print (line)
print (f"logs in logs/run{runNum}")

# write file and submit.
submitName = 'condorSubmit'
with open(submitName, 'w') as f:
    f.write(condorSubmit)

subprocess.call(f'chmod +x {executableName}'                               , shell=True)
subprocess.call(f'cp {executableName} {submitName} logs/run{runNum}'       , shell=True)

# direct submission from CIEMAT does not work... to be debugged.
print('\n ')
print(f'to submit the jobs execute: condor_submit {submitName}\n ')
print('to check the status of the jobs execute: condor_q \n ')        
print('to kill the jobs execute: condor_rm \n ')
