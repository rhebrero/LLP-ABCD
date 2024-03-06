import ROOT as rt
import numpy as np
file_rt = rt.TFile.Open('/nfs/cms/martialc/Displaced2024/llp/data/DiMuons_1PM_all.root')
tree_rt = file_rt.Get('SimpleNTupler/DDTree')

files = [
    '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022B-ReReco-v2.root',
    '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022C-ReReco-v2.root'
]

tree_src = rt.TChain('SimpleNTupler/DDTree')
[tree_src.Add(file) for file in files]

tree_rt.AddFriend(tree_src)


branch = 'patmu_nMuons - patmu_nPrompt'
selection_list = [
    'mySelection == 1', # Triggers
    'patmu_nPrompt > 0',
    'patmu_nMuons >= 2',
    'patmu_nMuonHits > 12',
    # 'patmu_nMatchedStation > 1',
    'patmu_pt > 10',
    '(patmu_ptError/patmu_pt) < 1',
    '(patmu_d0sig_pv/patmu_d0_pv) > 6'
]
nbins = 30
range = (0,30)

canvas = rt.TCanvas('c')
canvas.SetLogy()
hist = rt.TH1D('h',f'{branch} hist',nbins,*range)
tree_rt.Draw(
    f'{branch} >> h',
    '(' + ') && ('.join(selection_list) + ')'
)
print(hist.Integral())
hist.Draw('SAMES',)

# hist.GetXaxis().SetRangeUser(0,100)
canvas.Draw()
canvas.SaveAs(f'/nfs/cms/martialc/Displaced2024/llp/sandbox/figs/{branch}.pdf')