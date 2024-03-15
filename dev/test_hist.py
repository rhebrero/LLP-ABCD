import ROOT as rt
import numpy as np
from llp.utils.macros import load_macro
import numpy as np
load_macro('invMass')
load_macro('pt')


file_hist = [
    '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_BC__000_1e5.root',
    '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_BC__1e5_2e5.root',
    '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_BC__2e5_3e5.root',
    '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_BC__3e5_4e5.root',
]
file_hist = [
    '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_BC__000_1e5.root',
]

# branch = 'dim_mass'
# nmu = 1
prefix = ''
branch = 'patmu_nDisplaced'
# output = f'patmu_pt__mu1L_d0_pv_idx'
output = branch+'__Z'
nbins = 30
range = (0,30)


data_triggers = [
        'HLT_DoubleL2Mu23NoVtx_2Cha_v2',                    # Para Era B
        'HLT_DoubleL2Mu23NoVtx_2Cha_v3',                    # para Era C
        'HLT_DoubleL2Mu10NoVtx_2Cha_VetoL3Mu0DxyMax1cm_v2', # From aescalante@github/work/DDM/SimpleTTree/plots_example.py
        'HLT_DoubleL3Mu16_10NoVtx_DxyMin0p01cm_v2'          # From aescalante@github/work/DDM/SimpleTTree/plots_example.py
    ]
triggers = '(trig_hlt_idx>=0) && ('+'||'.join([f'trig_hlt_path == \"{trigger}\"' for trigger in data_triggers])+')'


selection_list = [
    triggers,
    # '(dimPL_mass < 80) || (dimPL_mass > 110)',
    '(dimPL_mass > 80) && (dimPL_mass < 110)',
]






# =============================================================================================================



tree_rt = rt.TChain('SimpleNTupler/DDTree')
[tree_rt.Add(file) for file in file_hist]


file_src = [
    '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022B-ReReco-v2.root',
    '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022C-ReReco-v2.root'
]
tree_src = rt.TChain('SimpleNTupler/DDTree')
[tree_src.Add(file) for file in file_src]

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

hist.GetYaxis().SetRangeUser(0.8,np.power(10,np.ceil(np.log10(hist.GetMaximum()+1)))*1.2)
# hist.GetXaxis().SetRangeUser(0,100)
canvas.Draw()
canvas.SaveAs(f'/nfs/cms/martialc/Displaced2024/llp/sandbox/figs/{output}.pdf')
canvas.SaveAs(f'/nfs/cms/martialc/Displaced2024/llp/sandbox/figs/{output}.png')
canvas.SaveAs(f'/nfs/cms/martialc/Displaced2024/llp/sandbox/figs/current.pdf')