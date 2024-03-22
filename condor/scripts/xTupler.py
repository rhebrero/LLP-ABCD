from llp.pyroot.macros import *
from llp.pyroot import Tree
from llp.utils.parser import str2float
from llp.utils.paths  import is_valid
from collections.abc import Iterable
import ROOT
import argparse


parser = argparse.ArgumentParser(description="Handle to submit retuple an NTuple from a config file that asks what branches to make.")
parser.add_argument('--output',
    dest        = 'output_path',
    required    = True, 
    help        = 'which condor job flavour to use'
)

parser.add_argument('--entries'     , 
    dest        = 'entries'         ,
    action      = 'extend'          ,
    nargs       = '+'               ,
    default     = None              ,
)

parser.add_argument('--verbose'     , 
    dest        = 'verbose'         ,
    action      = 'store_true'      ,
)

parser.add_argument('--input'       , 
    dest        = 'files'           ,
    action      = 'extend'          ,
    nargs       = '+'               ,
    required    = True              ,
)

parser.add_argument('--tree', '-t'  ,
    dest        = 'tree_path'       ,
    required    = True              ,
)

parser.add_argument('--debug-step'  ,
    dest        = 'debug_step'      ,
    nargs       = 1                 ,
    default     = 1e4               ,
)

args = parser.parse_args()



# ==============================================================================
#----------------------------------------------------------
#   ENTRIES
#----------------------------------------------------------
if args.entries is None:
    entries = 0
elif isinstance(args.entries, Iterable):
    if len(args.entries) == 1:
        entries = int(str2float(args.entries[0]))
    elif len(args.entries) == 2:
        entries = [
            int(str2float(ran_i))
            if ran_i != 'None' else None
            for ran_i in args.entries
        ]
    else:
        raise ValueError("Only 1 or 2 can be passed to --entries")
    
#----------------------------------------------------------
#   OUTPUT
#----------------------------------------------------------
if is_valid(args.output_path):
    output_path = args.output_path
else:
    raise ValueError(f"output path {args.output_path} doesn't exist!")

#----------------------------------------------------------
#   VERBOSE
#----------------------------------------------------------
verbose = args.verbose

#----------------------------------------------------------
#   INPUT
#----------------------------------------------------------
files = args.files

#----------------------------------------------------------
#   TREE
#----------------------------------------------------------
tree_path = args.tree_path

#----------------------------------------------------------
#   DEBUG STEP
#----------------------------------------------------------
debug_step = args.debug_step
# ==============================================================================


t1 = Tree(
    tree_path,
    files = files,
    branches = {
            'evt_event'                 : ROOT.std.vector('int')(),
            'patmu_d0_pv'               : ROOT.std.vector('float')(),
            'patmu_idx'                 : ROOT.std.vector('int')(),
            'patmu_px'                  : ROOT.std.vector('double')(),
            'patmu_py'                  : ROOT.std.vector('double')(),
            'patmu_eta'                 : ROOT.std.vector('float')(),
            'patmu_phi'                 : ROOT.std.vector('float')(),
            'trig_hlt_path'             : ROOT.std.vector('string')(),
            'trig_hlt_idx'              : ROOT.std.vector('int')(),
            'patmu_nMatchedStations'    : ROOT.std.vector('int')(),
            'patmu_nTrackerLayers'      : ROOT.std.vector('int')(),
            'patmu_ptError'             : ROOT.std.vector('float')(),
            'patmu_d0sig_pv'            : ROOT.std.vector('float')(),
        },
    debug = True,
    entries = entries,
    debug_step = int(debug_step),
    output_path=output_path,
    overwrite=True
)



# =======================
# PRIORIDAD 4
# =======================

priority = 4
t1.add_branch('patmu_nMuons',
    nMuons,
    branch          = 'patmu',
    default_value   = ROOT.std.vector('int')(),
    priority        = priority
)


# =======================
# PRIORIDAD 3
# =======================

priority = 3
t1.add_branch('patmu_pt',
    pt,
    branch          = 'patmu',
    vector          = True,
    default_value   = ROOT.std.vector('float')(),
    priority        = priority,
)

# =======================
# PRIORIDAD 2
# =======================
priority = 2
t1.add_branch('patmu_isGood',
    isGood,
    branch          = 'patmu',
    vector          = True,
    default_value   = ROOT.std.vector('int')(),
    priority        = priority,
)


# =======================
# PRIORIDAD 1
# =======================
priority = 1
t1.add_branch('patmu_isPrompt',
    isPrompt,
    branch          = 'patmu',
    vector          = True,
    default_value   = ROOT.std.vector('int')(),
    priority        = priority,
)
t1.add_branch('patmu_isDisplaced',
    isDisplaced,
    branch          = 'patmu',
    vector          = True,
    default_value   = ROOT.std.vector('int')(),
    priority        = priority,
)
t1.add_branch('patmu_nGood',
    nPassing,
    branch          = 'patmu',
    selection       = 'isGood',
    default_value   = ROOT.std.vector('int')(),
    priority        = priority
)
t1.add_branch('patmu_isGood_idx',
    selectionIdx,
    branch          = 'patmu',
    selection       = 'isGood',
    vector          = True,
    default_value   = ROOT.std.vector('int')(),
    priority        = priority
)
t1.add_branch('patmu_isGood_d0_pv_idx',
    sortBy,
    branch          = 'patmu_d0_pv',
    selection       = 'patmu_isGood',
    vector          = True,
    default_value   = ROOT.std.vector('int')(),
    priority        = priority,
)
# =======================
# PRIORIDAD 0 (default)
# =======================
priority = 0
t1.add_branch('patmu_nPrompt',
    nPassing,
    branch          = 'patmu',
    selection       = 'isPrompt',
    default_value   = ROOT.std.vector('int')(),
    priority        = priority
)
t1.add_branch('patmu_isPrompt_idx',
    selectionIdx,
    branch          = 'patmu',
    selection       = 'isPrompt',
    vector          = True,
    default_value   = ROOT.std.vector('int')(),
    priority        = priority,
)
t1.add_branch('patmu_isPrompt_d0_pv_idx',
    sortBy,
    branch          = 'patmu_d0_pv',
    selection       = 'patmu_isPrompt',
    vector          = True,
    default_value   = ROOT.std.vector('int')(),
    priority        = priority,
)
t1.add_branch('patmu_nDisplaced',
    nPassing,
    branch          = 'patmu',
    selection       = 'isDisplaced',
    default_value   = ROOT.std.vector('int')(),
    priority        = priority
)
t1.add_branch('patmu_isDisplaced_idx',
    selectionIdx,
    branch          = 'patmu',
    selection       = 'isDisplaced',
    vector          = True,
    default_value   = ROOT.std.vector('int')(),
    priority        = priority,
)
t1.add_branch('patmu_isDisplaced_d0_pv_idx',
    sortBy,
    branch          = 'patmu_d0_pv',
    selection       = 'patmu_isDisplaced',
    vector          = True,
    default_value   = ROOT.std.vector('int')(),
    priority        = priority,
)
t1.add_branch('patmu_d0_pv_idx',
    sortBy,
    branch          = 'patmu_d0_pv',
    vector          = True,
    default_value   = ROOT.std.vector('int')(),
    priority        = priority,
)


# =======================
# PRIORIDAD -1
# =======================

priority = -1
t1.add_branch('dimDD_mu*_idx',
    getNHighest,
    n               = 2,
    idx             = 'patmu_isDisplaced_d0_pv_idx',
    default_value   = ROOT.std.vector('int')(),
    priority        = priority
)
t1.add_branch('dimPP_mu*_idx',
    getNLowest,
    n               = 2,
    idx             = 'patmu_isPrompt_d0_pv_idx',
    default_value   = ROOT.std.vector('int')(),
    priority        = priority
)


# =======================
# PRIORIDAD -2
# =======================
priority = -2

t1.add_branch('dimPD_muP_idx',
    copyInt,
    branch          = 'dimPP_mu1_idx',
    default_value   = ROOT.std.vector('int')(),
    # vector          = True,
    priority        = priority
)
t1.add_branch('dimPD_muD_idx',
    copyInt,
    branch          = 'dimDD_mu1_idx',
    default_value   = ROOT.std.vector('int')(),
    priority        = priority
)
t1.add_branch('dimPP_mass',
    invMass_MuMu,
    branch          = 'patmu',
    mu_idx1         = 'dimPP_mu1_idx',
    mu_idx2         = 'dimPP_mu2_idx',
    default_value   = ROOT.std.vector('double')(),
    priority        = priority
)
t1.add_branch('dimDD_mass',
    invMass_MuMu,
    branch          = 'patmu',
    mu_idx1         = 'dimDD_mu1_idx',
    mu_idx2         = 'dimDD_mu2_idx',
    default_value   = ROOT.std.vector('double')(),
    priority        = priority
)


# =======================
# PRIORIDAD -3
# =======================
priority = -3

t1.add_branch('dimPD_mass',
    invMass_MuMu,
    branch          = 'patmu',
    mu_idx1         = 'dimPD_muP_idx',
    mu_idx2         = 'dimPD_muD_idx',
    default_value   = ROOT.std.vector('double')(),
    priority        = priority
)


t1.process_branches(verbose=verbose) # Pon esto a True para CADA ITERACIÓN saqque los valores antes y depsués
t1.close()