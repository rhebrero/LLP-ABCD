import ROOT as rt
import numpy as np
from llp.utils.macros import load_macro
load_macro('invMass')
load_macro('pt')


file_path = '/nfs/cms/martialc/Displaced2024/llp/data/DiMuons_1PM_1e5.root'

# branch = 'dim_mass'
# nmu = 1
branch = 'patmu_nPrompt'
# output = f'patmu_pt__mu1L_d0_pv_idx'
output = branch
nbins = 10
range = (0,10)


data_triggers = [
        'HLT_DoubleL2Mu23NoVtx_2Cha_v2',                    # Para Era B
        'HLT_DoubleL2Mu23NoVtx_2Cha_v3',                    # para Era C
        'HLT_DoubleL2Mu10NoVtx_2Cha_VetoL3Mu0DxyMax1cm_v2', # From aescalante@github/work/DDM/SimpleTTree/plots_example.py
        'HLT_DoubleL3Mu16_10NoVtx_DxyMin0p01cm_v2'          # From aescalante@github/work/DDM/SimpleTTree/plots_example.py
    ]
triggers = '(trig_hlt_idx>=0) && ('+'||'.join([f'trig_hlt_path == \"{trigger}\"' for trigger in data_triggers])+')'


selection_list = [
    # triggers
    'patmu_isAnyGood',
    # '(dimPL_mass < 80) || (dimPL_mass > 110)'
]






# =============================================================================================================



file_rt = rt.TFile.Open(file_path)
tree_rt = file_rt.Get('SimpleNTupler/DDTree')

files = [
    '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022B-ReReco-v2.root',
    '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022C-ReReco-v2.root'
]

tree_src = rt.TChain('SimpleNTupler/DDTree')
[tree_src.Add(file) for file in files]

tree_rt.AddFriend(tree_src)
# mass = rt.TTreeFormula(
#     'dim_mass_ClosestFurthest',
#     'invMass(patmu_pt[patmu_mu1L_d0_pv],patmu_eta[patmu_mu1L_d0_pv],patmu_phi[patmu_mu1L_d0_pv],patmu_pt[patmu_mu1_d0_pv],patmu_eta[patmu_mu1_d0_pv],patmu_phi[patmu_mu1_d0_pv])',
#     tree_rt
# )







canvas = rt.TCanvas('c')
canvas.SetLogy()
hist = rt.TH1D('h',f'{output} hist',nbins,*range)
if len(selection_list) > 0:
    tree_rt.Draw(
        f'{branch} >> h',
        '(' + ') && ('.join(selection_list) + ')'
    )
else:
    tree_rt.Draw(f'{branch} >> h')
print(hist.Integral())
hist.Draw('SAMES',)

# hist.GetXaxis().SetRangeUser(0,100)
canvas.Draw()
canvas.SaveAs(f'/nfs/cms/martialc/Displaced2024/llp/sandbox/figs/{output}.pdf')
canvas.SaveAs(f'/nfs/cms/martialc/Displaced2024/llp/sandbox/figs/{output}.png')
canvas.SaveAs(f'/nfs/cms/martialc/Displaced2024/llp/sandbox/figs/current.pdf')