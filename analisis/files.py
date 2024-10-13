import ROOT as rt
import pdb
import os

# fb-1
lumi_DoubleMuonRun2022B = 0.11
lumi_DoubleMuonRun2022C = 0.61
lumi_MuonRun2022C = 5.56
lumi_MuonRun2022D = 3.28
lumi_MuonRun2022E = 5.93

lumi_MuonRun2022G = 3.08
lumi_MuonRun2022F = 18.12


# pb
xsec_Zto2E_M_10_50 = 6744
xsec_Zto2E_M_50_120 = 2219
xsec_Zto2E_M_120_200 = 21.65
xsec_Zto2E_M_200_400 = 3.058
xsec_Zto2E_M_400_800 = 0.2691
xsec_Zto2E_M_800_1500 = 1.915e-2

STopSignalFolder = '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/STopToMuB_v05/'


signal_STop_500_1 = STopSignalFolder + 'STopToMuB_500_1.root'
signal_STop_500_10 = STopSignalFolder + 'STopToMuB_500_10.root'
signal_STop_500_100 = STopSignalFolder + 'STopToMuB_500_100.root'
signal_STop_500_1000 = STopSignalFolder + 'STopToMuB_500_1000.root'
signal_STop_500_10000 = STopSignalFolder + 'STopToMuB_500_10000.root'
signal_STop_500_100000 = STopSignalFolder + 'STopToMuB_500_100000.root'

signal_STop_500 = [  signal_STop_500_1, 
                signal_STop_500_10,
                signal_STop_500_100,
                signal_STop_500_1000,
                signal_STop_500_10000,
                signal_STop_500_100000
                ]

signal_STop_100_1 = STopSignalFolder + 'STopToMuB_100_1.root'
signal_STop_100_10 = STopSignalFolder + 'STopToMuB_100_10.root'
signal_STop_100_100 = STopSignalFolder + 'STopToMuB_100_100.root'
signal_STop_100_1000 = STopSignalFolder + 'STopToMuB_100_1000.root'
signal_STop_100_10000 = STopSignalFolder + 'STopToMuB_100_10000.root'
signal_STop_100_100000 = STopSignalFolder + 'STopToMuB_100_100000.root'

signal_STop_100 = [  signal_STop_100_1, 
                signal_STop_100_10,
                signal_STop_100_100,
                signal_STop_100_1000,
                signal_STop_100_10000,
                signal_STop_100_100000
                ]

SMuonSignalFolder = '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202404_April24/SMuonToMuGravitino_v02/'

signal_SMuon_500_1 = SMuonSignalFolder + 'SMuonToMuGravitino_500_1.root' 
signal_SMuon_500_10 = SMuonSignalFolder + 'SMuonToMuGravitino_500_10.root' 
signal_SMuon_500_100 = SMuonSignalFolder + 'SMuonToMuGravitino_500_100.root' 
signal_SMuon_500_1000 = SMuonSignalFolder + 'SMuonToMuGravitino_500_1000.root' 
signal_SMuon_500_10000 = SMuonSignalFolder + 'SMuonToMuGravitino_500_10000.root' 
signal_SMuon_500_100000 = SMuonSignalFolder + 'SMuonToMuGravitino_500_100000.root' 

signal_SMuon_500 = [  signal_SMuon_500_1,
                signal_SMuon_500_10,
                signal_SMuon_500_100,
                signal_SMuon_500_1000,
                signal_SMuon_500_10000,
                signal_SMuon_500_100000
                ]


signal_SMuon_100_1 = SMuonSignalFolder + 'SMuonToMuGravitino_100_1.root' 
signal_SMuon_100_10 = SMuonSignalFolder + 'SMuonToMuGravitino_100_10.root' 
signal_SMuon_100_100 = SMuonSignalFolder + 'SMuonToMuGravitino_100_100.root' 
signal_SMuon_100_1000 = SMuonSignalFolder + 'SMuonToMuGravitino_100_1000.root' 
signal_SMuon_100_10000 = SMuonSignalFolder + 'SMuonToMuGravitino_100_10000.root' 
signal_SMuon_100_100000 = SMuonSignalFolder + 'SMuonToMuGravitino_100_100000.root' 

signal_SMuon_100 = [  signal_SMuon_100_1, 
                signal_SMuon_100_10,
                signal_SMuon_100_100,
                signal_SMuon_100_1000,
                signal_SMuon_100_10000,
                signal_SMuon_100_100000
                ]

DataErasFolder = '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/'
data0 = DataErasFolder + 'DiMuons_NPND_BC__000_1e5.root'
data1e5 = DataErasFolder + 'DiMuons_NPND_BC__1e5_2e5.root'
data2e5 = DataErasFolder + 'DiMuons_NPND_BC__2e5_3e5.root'
data3e5 = DataErasFolder + 'DiMuons_NPND_BC__3e5_4e5.root'
data4e5 = DataErasFolder + 'DiMuons_NPND_BC__4e5_5e5.root'
data = [data0, data1e5, data2e5, data3e5, data4e5]

data_eraB = DataErasFolder + 'DiMuons_NPND_B.root'

eraB_bruto = '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022B-ReReco-v2.root'
eraCDouble_bruto = '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022C-ReReco-v2.root'
eraC_bruto = '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_MuonRun2022C-ReReco-v1.root'
eraD_bruto = '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_MuonRun2022D-ReReco-v1.root'
eraE_bruto = '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_MuonRun2022E-ReReco-v2.root'
eraG_bruto = '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_MuonRun2022G-PromptReco-v1.root'

data_full = rt.TChain('SimpleNTupler/DDTree')
[data_full.Add(dat) for dat in data]

# EraDFolder = "/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202407_July24/Run3_2022/ntuple_2022_MuonRun2022D-ReReco-v1/"
# eraDChain = rt.TChain('SimpleNTupler/DDTree')
data_eraCDouble = '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202407_July24/Run3_2022/merged_files/DoubleMuonRun2022C-ReReco-v2.root'
data_eraC = '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202407_July24/Run3_2022/merged_files/MuonRun2022C-ReReco-v1.root'
data_eraD = '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202407_July24/Run3_2022/merged_files/MuonRun2022D-ReReco-v1.root'
data_eraE = '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202407_July24/Run3_2022/merged_files/MuonRun2022E-ReReco-v2.root'
data_eraG = '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202407_July24/Run3_2022/merged_files/MuonRun2022G-PromptReco-v1.root'
# eraD_bruto = '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_MuonRun2022D-ReReco-v1.root'


files_src = [
    '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022B-ReReco-v2.root',
    '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022C-ReReco-v2.root'
]
tree_src = rt.TChain('SimpleNTupler/D6D6Tree')
[tree_src.Add(file) for file in files_src]

dataBC = DataErasFolder + 'DiMuons_NPND_BC.root'



Folder_background = '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202404_April24/'

DYto2Mu_50to120_bruto = '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedLeptons/testProduction_March2024/merged_files/ntuple_2022_DYto2Mu_MLL-50to120.root'
DYto2Mu_120to200_bruto = '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedLeptons/testProduction_March2024/merged_files/ntuple_2022_DYto2Mu_MLL-120to200.root'

DYto2Mu_10to50 =        Folder_background +'DYto2Mu/DYto2Mu_10to50.root'
DYto2Mu_50to120 =       Folder_background +'DYto2Mu/DYto2Mu_50to120.root'
DYto2Mu_120to200 =      Folder_background +'DYto2Mu/DYto2Mu_120to200.root'
DYto2Mu_200to400 =      Folder_background +'DYto2Mu/DYto2Mu_200to400.root'
DYto2Mu_400to800 =      Folder_background +'DYto2Mu/DYto2Mu_400to800.root'
DYto2Mu_800to1500 =     Folder_background +'DYto2Mu/DYto2Mu_800to1500.root'
    
DYto2Tau_10to50 =       Folder_background +'DYto2Tau/DYto2Tau_10to50.root'
DYto2Tau_50to120 =      Folder_background +'DYto2Tau/DYto2Tau_50to120.root'
DYto2Tau_120to200 =     Folder_background +'DYto2Tau/DYto2Tau_120to200.root'
DYto2Tau_200to400 =     Folder_background +'DYto2Tau/DYto2Tau_200to400.root'
DYto2Tau_400to800 =     Folder_background +'DYto2Tau/DYto2Tau_400to800.root'
DYto2Tau_800to1500 =    Folder_background +'DYto2Tau/DYto2Tau_800to1500.root'

DYto2Mu_10to50_500k = Folder_background + 'DYto2Mu/DYto2Mu_10to50_500k.root'
DYto2Mu_50to120_500k = Folder_background + 'DYto2Mu/DYto2Mu_50to120_500k.root'
DYto2Mu_120to200_500k = Folder_background + 'DYto2Mu/DYto2Mu_120to200_500k.root'
DYto2Mu_200to400_500k = Folder_background + 'DYto2Mu/DYto2Mu_200to400_500k.root'
DYto2Mu_400to800_500k = Folder_background + 'DYto2Mu/DYto2Mu_400to800_500k.root'
DYto2Mu_800to1500_500k = Folder_background + 'DYto2Mu/DYto2Mu_800to1500_500k.root'

QCD_15to20 = Folder_background + 'QCD/QCD_15to20.root'
QCD_20to30 = Folder_background + 'QCD/QCD_20to30.root'
QCD_30to50 = Folder_background + 'QCD/QCD_30to50.root'
QCD_50to80 = Folder_background + 'QCD/QCD_50to80.root'
QCD_80to120 = Folder_background + 'QCD/QCD_80to120.root'
QCD_120to170 = Folder_background + 'QCD/QCD_120to170.root'
QCD_170to300 = Folder_background + 'QCD/QCD_170to300.root'
QCD_300to470 = Folder_background + 'QCD/QCD_300to470.root'
QCD_470to600 = Folder_background + 'QCD/QCD_470to600.root'
QCD_600to800 = Folder_background + 'QCD/QCD_600to800.root'
QCD_800to1000 = Folder_background + 'QCD/QCD_800to1000.root'
QCD_1000toInf = Folder_background + 'QCD/QCD_1000toInf.root'

