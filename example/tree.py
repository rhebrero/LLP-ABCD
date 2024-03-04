from llp.pyroot.macros import mu_nPrompt, pt, nMuons, getNHighest
from llp.utils.macros import load_macro
from llp.pyroot import Tree
import ROOT
from array import array


files = [
    '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022B-ReReco-v2.root',
    '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022C-ReReco-v2.root'
]

t1 = Tree(
    'SimpleNTupler/DDTree',
    files = files,
    branches = {
            'patmu_d0_pv'   : ROOT.VecOps.RVec('float')(),
            'dsamu_d0_pv'   : ROOT.VecOps.RVec('float')(),
            'patmu_idx'     : ROOT.VecOps.RVec('int')(),
            'patmu_px'      : ROOT.VecOps.RVec('float')(),
            'patmu_py'      : ROOT.VecOps.RVec('float')()
        },
    debug = True,
    nentries = int(1e2),
    debug_step = int(1e1),
    output_path='test_1e2',
    overwrite=True
)

t1.add_branch(
    'patmu_nMuons',
    nMuons,
    default_value= ROOT.VecOps.RVec('int')(),
    mu_type = 'pat',
    priority = 1
)

t1.add_branch(
    'patmu_pt',
    pt,
    mu_type = 'pat',
    default_value = ROOT.VecOps.RVec('float')(),
    vector = 'patmu_nMuons',
    priority=1
)

t1.add_branch(
    'patmu_nPrompt',
    mu_nPrompt,
    default_value= ROOT.VecOps.RVec('int')(),
    d0_cut = 0.1,
    mu_type = 'pat',
)

t1.add_branch(
    'patmu_mu*_pt',
    getNHighest,
    default_value   = ROOT.VecOps.RVec('int')(),
    mu_type         = 'pat',
    branch          = 'pt',
    n               = 2,
    priority        =-1
)

t1.add_branch(
    'patmu_mu*_d0',
    getNHighest,
    default_value   = ROOT.VecOps.RVec('int')(),
    mu_type         = 'pat',
    branch          = 'd0_pv',
    n               = 2,
    priority        =-1
)


t1.process_branches(verbose=False) # Pon esto a True para CADA ITERACIÓN saqque los valores antes y depsués
t1.close()