import subprocess
import os 
import argparse

parser = argparse.ArgumentParser(description="Handle to submit retuple an NTuple from a config file that asks what branches to make.")

#modes
parser.add_argument('--flavour'    , dest='flavour'   , default='longlunch'     , help='which condor job flavour to use')
parser.add_argument('--inputFile'  , dest='input_file', default='jobs.sh'       , help='input file (with scripts to run on)')
parser.add_argument('--use-proxy'  , dest='proxy'     , action='store_true'     , help='whether to ship the GRID certificate with the jobs')
parser.add_argument('--ciemat'     , dest='ciemat'    , action='store_true'     , help='whether to run at CIEMAT (grid GRID combined with certificate untested)')
parser.add_argument('--pnfs'       , dest='pnfs'      , action='store_true'     , help='if running at CIEMAT, additional request machines with access to PNFS')
parser.add_argument('--gaefacil'   , dest='gaefacil'  , action='store_true'     , help='whether to include gaefacilXX machines to available machines')

args = parser.parse_args()

