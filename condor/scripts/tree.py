from llp.pyroot.macros import *
from llp.pyroot import Tree
from llp.utils.parser import str2float
from llp.utils.paths  import is_valid
from collections.abc import Iterable
import ROOT
import argparse


parser = argparse.ArgumentParser(description="Handle to submit retuple an NTuple from a config file that asks what branches to make.")
parser.add_argument('--output',
    dest='output_path',
    required = True, 
    help='which condor job flavour to use'
)

parser.add_argument('--entries', 
    dest    = 'entries' ,
    action  = 'extend'  ,
    nargs   = '+'       ,
    default = None      ,
)

parser.add_argument('--verbose', 
    dest    = 'verbose'   ,
    action  = 'store_true',
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
# ==============================================================================


data_triggers = [
        'HLT_DoubleL2Mu23NoVtx_2Cha_v2',                    # Para Era B
        'HLT_DoubleL2Mu23NoVtx_2Cha_v3',                    # para Era C
        'HLT_DoubleL2Mu10NoVtx_2Cha_VetoL3Mu0DxyMax1cm_v2', # From aescalante@github/work/DDM/SimpleTTree/plots_example.py
        'HLT_DoubleL3Mu16_10NoVtx_DxyMin0p01cm_v2'          # From aescalante@github/work/DDM/SimpleTTree/plots_example.py
    ]

# De las transparencias de Rubén
sim_triggers = [
    'HLT_DoubleL2Mu23NoVtx_2Cha_CosmicSeed_v3' ,
    'HLT_DoubleL2Mu23NoVtx_2Cha_v3' ,
    'HLT_DoubleL2Mu10NoVtx_2Cha_VetoL3Mu0DxyMax1cm_v1' ,
    'HLT_DoubleL3Mu16_10NoVtx_DxyMin0p01cm_v1'
]

triggers = sim_triggers
trigger = '('+'||'.join([f'trig_hlt_path == \"{trigger}\"' for trigger in triggers])+')'

selection_good = [
        # trigger,
        'patmu_nMatchedStations > 1',
        'patmu_nTrackerLayers > 5',
        'patmu_pt > 5',
        '(patmu_ptError/patmu_pt) < 1',
    ]

selection_prompt = [
        # trigger,
        '((patmu_d0_pv    <= 0.1) && (patmu_d0sig_pv > 1.2)) || (patmu_d0sig_pv <= 1.2)'
        # Que esté muy cerca o que no se pueda resolver.
    ]

selection_displaced = [
        # trigger,
        'patmu_d0_pv > 0.1',
        'patmu_d0sig_pv > 6'
    ]

is_good         = '(' + ') && ('.join(  selection_good        ) + ')'
is_prompt       = '(' + ') && ('.join(  selection_prompt      ) + ')'
is_displaced    = '(' + ') && ('.join(  selection_displaced   ) + ')'

# print(my_selection)






files = [
    '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022B-ReReco-v2.root',
    '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022C-ReReco-v2.root'
]

tree_path = 'SimpleNTupler/DDTree'


# files = [
#     '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedLeptons/testProduction_March2024/merged_files/ntuple_2022_SMuon_500_10.root'
# ]
# tree_path = 'SimpleMiniNTupler/DDTree'
# output_path = 'STop_500_10_1PM'

debug_step = 1e4
# ====================================================================================================================
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
t1.add_branch('patmu_d0_pv_idx',
    sortBy,
    branch          = 'patmu_d0_pv',
    selection       = 'patmu_isGood',
    vector          = True,
    default_value   = ROOT.std.vector('int')(),
    priority        = priority,
)


# =======================
# PRIORIDAD -1
# =======================

priority = -1
t1.add_branch('patmu_mu*L_d0_pv_idx',
    getNLowest,
    n               = 1,
    idx             = 'patmu_d0_pv_idx',
    default_value   = ROOT.std.vector('int')(),
    priority        = priority
)
t1.add_branch('patmu_mu*_d0_pv_idx',
    getNHighest,
    n               = 1,
    idx             = 'patmu_d0_pv_idx',
    default_value   = ROOT.std.vector('int')(),
    priority        = priority
)


# =======================
# PRIORIDAD -2
# =======================

priority = -2
t1.add_branch('dimPL_mass',
    invMass_MuMu,
    branch          = 'patmu',
    mu_idx1         = 'patmu_mu1_d0_pv_idx',
    mu_idx2         = 'patmu_mu1L_d0_pv_idx',
    default_value   = ROOT.std.vector('double')(),
    priority        = priority
)



t1.process_branches(verbose=verbose) # Pon esto a True para CADA ITERACIÓN saqque los valores antes y depsués
t1.close()