from llp.pyroot.macros import *
from llp.pyroot import Tree
import ROOT
from array import array
entries = -1

prompt_cut   = 'abs(patmu_d0_pv) < 0.1'
verbose = False

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
trigger = '(trig_hlt_idx.size() > 0) && ('+'||'.join([f'trig_hlt_path == \"{trigger}\"' for trigger in triggers])+')'

filters = [
        # trigger,
        'patmu_nMatchedStations > 1',
        'patmu_nTrackerLayers > 5',
        'patmu_pt > 10', # Se carga muchos muones
        '(patmu_ptError/patmu_pt) < 1',
        # 'patmu_d0sig_pv > 6',
    ]

my_selection = '(' + ') && ('.join(filters) + ')'
# print(my_selection)






# files = [
#     '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022B-ReReco-v2.root',
#     '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022C-ReReco-v2.root'
# ]

# tree_path = 'SimpleNTupler/DDTree'
# output_path = 'DiMuons_1PM_1e5'
# nentries = 1e5


files = [
    '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedLeptons/testProduction_March2024/merged_files/ntuple_2022_SMuon_500_10.root'
]
tree_path = 'SimpleMiniNTupler/DDTree'
output_path = 'STop_500_10_1PM'

entries = 10
debug_step = 1e3
verbose = True
# ====================================================================================================================
t1 = Tree(
    tree_path,
    files = files,
    branches = {
            'evt_event'                 : ROOT.std.vector('int')(),
            'patmu_d0_pv'               : ROOT.std.vector('float')(),
            'patmu_d0_bs'               : ROOT.std.vector('float')(),
            'patmu_idx'                 : ROOT.std.vector('int')(),
            'patmu_px'                  : ROOT.std.vector('float')(),
            'patmu_py'                  : ROOT.std.vector('float')(),
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
# PRIORIDAD 3
# =======================

priority = 3
t1.add_branch(
    'patmu_nMuons',
    nMuons,
    mu_type         = 'pat',
    default_value   = ROOT.std.vector('int')(),
    priority        = priority
)

t1.add_branch(
    'patmu_pt',
    pt,
    mu_type         = 'pat',
    default_value   = ROOT.std.vector('float')(),
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
    n_muons         = 'patmu_nMuons',
    cut             = prompt_cut,
    default_value   = ROOT.std.vector('int')(),
    vector          = 'patmu_nMuons',
    priority        = priority,
)

t1.add_branch(
    'patmu_isGood',
    selectionMask,
    n_muons         = 'patmu_nMuons',
    cut             = my_selection,
    default_value   = ROOT.std.vector('int')(),
    vector          = 'patmu_nMuons',
    priority        = priority,
)


# =======================
# PRIORIDAD 1
# =======================

priority = 1
t1.add_branch(
    'patmu_nPrompt',
    nPassing,
    branch          = 'patmu_isPrompt',
    n_muons         = 'patmu_nMuons',
    default_value   = ROOT.std.vector('int')(),
    priority        = priority
)

t1.add_branch(
    'patmu_isAnyPrompt',
    perEntry,
    branch          = 'patmu_isPrompt',
    default_value   = ROOT.std.vector('int')(),
    priority        = priority
)

t1.add_branch(
    'patmu_isAnyGood',
    perEntry,
    branch          = 'patmu_isGood',
    default_value   = ROOT.std.vector('int')(),
    priority        = priority
)
# =======================
# PRIORIDAD 0 (default)
# =======================
priority = 0
t1.add_branch(
    'patmu_isGood_idx',
    selectionIdx,
    n_muons         = 'patmu_nMuons',
    branch          = 'patmu_isGood',
    default_value   = ROOT.std.vector('int')(),
    priority        = priority,
    vector          = True
)

t1.add_branch(
    'patmu_isPrompt_idx',
    selectionIdx,
    n_muons         = 'patmu_nMuons',
    branch          = 'patmu_isPrompt',
    default_value   = ROOT.std.vector('int')(),
    priority        = priority,
    vector          = True
)

# =======================
# PRIORIDAD -1
# =======================

priority = -1
t1.add_branch(
    'patmu_mu*_pt_idx',
    getNHighest,
    default_value   = ROOT.std.vector('int')(),
    mu_type         = 'pat',
    branch          = 'pt',
    n               = 2,
    mu_idx          = 'patmu_isGood_idx',
    priority        = priority
)

t1.add_branch(
    'patmu_mu*L_d0_pv_idx',
    getNLowest,
    default_value   = ROOT.std.vector('int')(),
    mu_type         = 'pat',
    branch          = 'd0_pv',
    n               = 1,
    do_abs          = True,
    mu_idx          = 'patmu_isGood_idx',
    priority        = priority
)

t1.add_branch(
    'patmu_mu*_d0_pv_idx',
    getNHighest,
    default_value   = ROOT.std.vector('int')(),
    mu_type         = 'pat',
    branch          = 'd0_pv',
    n               = 1,
    do_abs          = True,
    mu_idx          = 'patmu_isGood_idx',
    priority        = priority
)

t1.add_branch(
    'patmu_mu*L_d0_bs_idx',
    getNLowest,
    default_value   = ROOT.std.vector('int')(),
    mu_type         = 'pat',
    branch          = 'd0_bs',
    n               = 1,
    do_abs          = True,
    mu_idx          = 'patmu_isGood_idx',
    priority        = priority
)

t1.add_branch(
    'patmu_mu*_d0_bs_idx',
    getNHighest,
    default_value   = ROOT.std.vector('int')(),
    mu_type         = 'pat',
    branch          = 'd0_bs',
    n               = 1,
    do_abs          = True,
    mu_idx          = 'patmu_isGood_idx',
    priority        = priority
)

# =======================
# PRIORIDAD -2
# =======================

priority = -2
t1.add_branch(
    'dimPL_mass',
    invMass_MuMu,
    default_value   = ROOT.std.vector('double')(),
    mu_type         = 'pat',
    mu_idx1         = 'patmu_mu1_d0_pv_idx',
    mu_idx2         = 'patmu_mu1L_d0_pv_idx',
    priority        = priority
)


# print(t1.total_branches)
# exit()


t1.process_branches(verbose=verbose) # Pon esto a True para CADA ITERACIÓN saqque los valores antes y depsués
t1.close()