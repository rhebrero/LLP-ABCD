import ROOT as rt
import numpy as np
from files import *
import pdb
from array import array
from functions import *

import os
import sys
curr_dir = os.path.dirname(os.path.abspath(__file__)) # Currently doing it like this, will need to add it to env var once it's organized
conf_dir = os.path.join(curr_dir, '..', 'config/')
conf_dir = os.path.normpath(conf_dir)
sys.path.append(conf_dir)
from config_test import *
# file = rt.TFile.Open('/pnfs/ciemat.es/data/cms/store/user/escalant/displacedLeptons/StopToMuB_v05/StopToMuB_500_10.root')
# tree = file.Get('SimpleMiniNTupler/DDTree')



# file = rt.TFile.Open(signal_SMuon_500_1000)
# tree = file.Get('SimpleMiniNTupler/DDTree')
# file = rt.TFile.Open('/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_BC__000_1e5.root')
# tree = file.Get('SimpleNTupler/DDTree')

# tree.Scan('dim_mu1_idx:dim_mu2_idx')

# file = rt.TFile.Open('/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_BC__1e5_2e5.root')
# tree = file.Get('SimpleNTupler/DDTree')

# chain = rt.TChain('SimpleNTupler/DDTree')
# chain.Add('/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_BC__000_1e5.root')
# chain.Add('/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_BC__1e5_2e5.root')

# value = rt.std.vector('string')()
# tree.SetBranchAddress('trig_hlt_idx',value)


# tree.Scan('patmu_mu1_d0_pv_idx:patmu_isGood_idx:patmu_d0_pv_idx:patmu_pt')

# tree.Scan('patmu_isGood_d0_pv_idx:patmu_d0_pv')
# print(tree.GetEntries())


# dir = file.Get('SimpleNTupler')
# dir.ls()
# file.ls()

# keys = file.GetListOfKeys()

# DYto2Mu_50to120
# file = rt.TFile.Open(DYto2Tau_50to120)
# file.ls()
# dir = file.Get('SimpleMiniNTupler')
# dir.ls()
# tree.Scan('trig_hlt_path')
# for branch in tree.GetListOfBranches():
#     print(branch.GetName())

path = '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/'

file = rt.TFile.Open(path + 'ntuple_2022_DoubleMuonRun2022C-ReReco-v2.root')
tree = file.Get('SimpleNTupler/DDTree')

fileDY = rt.TFile.Open('/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202404_April24/DYto2Mu/DYto2Mu_10to50_500k.root')
# fileDY_not500 = rt.TFile.Open('/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202404_April24/DYto2Mu/DYto2Mu_50to120.root')
treeDY = fileDY.Get('SimpleMiniNTupler/DDTree')
# treeDY_not500 = fileDY_not500.Get('SimpleMiniNTupler/DDTree')

fileB = rt.TFile.Open(data_eraB)
treeB = fileB.Get('SimpleNTupler/DDTree')
# treeB.Scan('patmu_d0sig_pv:dimPP_mu1_idx')

fileC = rt.TFile.Open(data_eraCDouble)
treeC = fileC.Get('SimpleNTupler/DDTree')


fileC_bruto = rt.TFile.Open('/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022C-ReReco-v2.root')
treeC_bruto = fileC_bruto.Get('SimpleNTupler/DDTree')


fileD = rt.TFile.Open('/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202407_July24/Run3_2022/ntuple_2022_MuonRun2022D-ReReco-v1/ntuple_2022_MuonRun2022D-ReReco-v1_000.root')
treeD = fileD.Get('SimpleNTupler/DDTree')

file1 = rt.TFile.Open(data1e5)
tree1 = file1.Get('SimpleNTupler/DDTree')

file0 = rt.TFile.Open(data0)
tree0 = file1.Get('SimpleNTupler/DDTree')

file_smuon = rt.TFile.Open(signal_SMuon_500_100)
tree_smuon = file_smuon.Get('SimpleMiniNTupler/DDTree')

file_stop = rt.TFile.Open(signal_STop_100_100)
tree_stop = file_stop.Get('SimpleMiniNTupler/DDTree')


file_bruto = rt.TFile.Open(DYto2Tau_800to1500)
tree_bruto = file_bruto.Get('SimpleMiniNTupler/DDTree')

file_eraB_bruto = rt.TFile.Open('/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022B-ReReco-v2.root')
treeB_bruto = file_eraB_bruto.Get('SimpleNTupler/DDTree')

file_friend_smuon = rt.TFile.Open('/pnfs/ciemat.es/data/cms/store/user/escalant/displacedLeptons/testProduction_April_2024_v1/merged_files/ntuple_2022_SMuon_100_10000.root')
tree_friend_smuon = file_friend_smuon.Get('SimpleMiniNTupler/DDTree')

file_gen = rt.TFile.Open('/pnfs/ciemat.es/data/cms/store/user/escalant/SMuonToMuGravitino-M_500_ctau_10mm_TuneCP5_13p6TeV_pythia8/AODSIM-November2023_v1/231122_095334/0000/AODSIM_1.root')
tree_gen = file_gen.Get('Events')

# from DataFormats.FWLite import Handle, Events
# events = Events(file_gen)

# treeC.AddFriend('SimpleNTupler/DDTree', '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022C-ReReco-v2.root')
# for event in treeC:
#     pdb.set_trace()
# pdb.set_trace()

# f, t = read_tree(DYto2Mu_10to50)

# tree_smuon.Scan('patmu_nDisplaced:patmu_isDisplaced_idx:dimDD_mass')#, "", "", 100, 1000)

# print(tree_bruto.GetEntries())


for branch in tree_friend_smuon.GetListOfBranches():
    print(branch.GetName())
pdb.set_trace()

for event in tree_friend_smuon:
    pdb.set_trace()

# for event in treeB:
#     if event.dimPP_mu1_idx[0]>-1 and event.patmu_d0sig_pv[event.dimPP_mu1_idx[0]]>1.2:print(event.patmu_d0sig_pv[event.dimPP_mu1_idx[0]])

res_dict = get_dict('background', 'DYto2Mu200k', mass_i=10, mass_f = 50)
file_DY200 = rt.TFile.Open(res_dict['file'])
tree_DY200 = file_DY200.Get('SimpleMiniNTupler/DDTree')



