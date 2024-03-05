from llp.pyroot.macros import *
from llp.pyroot import Tree
import ROOT
from array import array

prompt_cut   = 'abs(patmu_d0_pv) < 0.1'



data_triggers = [
        'trig_hlt_path=="HLT_DoubleL2Mu23NoVtx_2Cha_v2"', # Para Era B
        'trig_hlt_path=="HLT_DoubleL2Mu23NoVtx_2Cha_v3"'  # para Era C
    ]
triggers = '('+'||'.join(data_triggers)+')'
data_filters = [
        triggers,
    ]

my_selection = '(' + ') && ('.join(data_filters) + ')'







files = [
    '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022B-ReReco-v2.root',
    '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022C-ReReco-v2.root'
]

t1 = Tree(
    'SimpleNTupler/DDTree',
    files = files,
    branches = {
            'patmu_d0_pv'   : ROOT.VecOps.RVec('float')(),
            'patmu_idx'     : ROOT.VecOps.RVec('int')(),
            'patmu_px'      : ROOT.VecOps.RVec('float')(),
            'patmu_py'      : ROOT.VecOps.RVec('float')(),
            'trig_hlt_path' : ROOT.std.vector('string')(),
        },
    debug = True,
    # nentries = int(10),
    debug_step = int(1e4),
    output_path='test',
    overwrite=True
)

# =======================
# PRIORIDAD 3
# =======================

priority = 3
t1.add_branch(
    'patmu_nMuons',
    nMuons,
    mu_type         = 'pat',
    default_value   = ROOT.VecOps.RVec('int')(),
    priority        = priority
)

t1.add_branch(
    'patmu_pt',
    pt,
    mu_type         = 'pat',
    default_value   = ROOT.VecOps.RVec('float')(),
    vector          = 'patmu_nMuons',
    priority        = priority,
)

# =======================
# PRIORIDAD 2
# =======================

priority = 2
t1.add_branch(
    'patmu_isPrompt',
    selectionMask,
    cut             = prompt_cut,
    default_value   = ROOT.VecOps.RVec('int')(),
    vector          = 'patmu_nMuons',
    priority        = priority
)

t1.add_branch(
    'mySelection',
    selectionMask,
    cut             = my_selection,
    default_value   = ROOT.VecOps.RVec('int')(),
    vector          = 'patmu_nMuons',
    priority        = priority
)


# =======================
# PRIORIDAD 1
# =======================

priority = 1
t1.add_branch(
    'patmu_nPrompt',
    nPassing,
    branch          = 'patmu_isPrompt',
    default_value   = ROOT.VecOps.RVec('int')(),
    priority        = priority
)

t1.add_branch(
    'patmu_isAnyPrompt',
    perEntry,
    branch          = 'patmu_isPrompt',
    default_value   = ROOT.VecOps.RVec('int')(),
    priority        = priority
)

t1.add_branch(
    'mySelection_Any',
    perEntry,
    branch          = 'mySelection',
    default_value   = ROOT.VecOps.RVec('int')(),
    priority        = priority
)
# =======================
# PRIORIDAD 0 (default)
# =======================
priority = 0


# =======================
# PRIORIDAD -1
# =======================

priority = -1
t1.add_branch(
    'patmu_mu*_pt',
    getNHighest,
    default_value   = ROOT.VecOps.RVec('int')(),
    mu_type         = 'pat',
    branch          = 'pt',
    n               = 2,
    priority        = priority
)

t1.add_branch(
    'patmu_mu*_d0',
    getNHighest,
    default_value   = ROOT.VecOps.RVec('int')(),
    mu_type         = 'pat',
    branch          = 'd0_pv',
    n               = 2,
    priority        = priority
)



t1.process_branches(verbose=False) # Pon esto a True para CADA ITERACIÓN saqque los valores antes y depsués
t1.close()