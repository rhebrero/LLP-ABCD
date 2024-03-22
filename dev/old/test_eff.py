import ROOT as rt
import numpy as np
from llp.utils.macros import load_macro
from llp.pyroot.plots.classes.Hist import Hist
import numpy as np
import matplotlib.pyplot as plt
# signal = 'STop'
signal = 'SMuon'
effs = {
    100 : [],
    500 : []
}


data_src    = '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_BC__1e5_2e5.root'

signal_ctau_list         = [1,10,100,1000,10000,100000] #mm

#===================================================
# CONSTANTES
#===================================================

signal_trigger_dict = dict(
    SMuon = [
        'HLT_DoubleL2Mu23NoVtx_2Cha_CosmicSeed_v2' ,
        'HLT_DoubleL2Mu23NoVtx_2Cha_v2' ,
        'HLT_DoubleL2Mu10NoVtx_2Cha_VetoL3Mu0DxyMax1cm_v1' ,
        'HLT_DoubleL3Mu16_10NoVtx_DxyMin0p01cm_v1'
    ],
    STop = [
        'HLT_DoubleL2Mu23NoVtx_2Cha_CosmicSeed_v3' ,
        'HLT_DoubleL2Mu23NoVtx_2Cha_v3' ,
        'HLT_DoubleL2Mu10NoVtx_2Cha_VetoL3Mu0DxyMax1cm_v1' ,
        'HLT_DoubleL3Mu16_10NoVtx_DxyMin0p01cm_v1'
    ]   
)

data_triggers = [
        'HLT_DoubleL2Mu23NoVtx_2Cha_v2',                    # Para Era B
        'HLT_DoubleL2Mu23NoVtx_2Cha_v3',                    # para Era C
        'HLT_DoubleL2Mu10NoVtx_2Cha_VetoL3Mu0DxyMax1cm_v2', # From aescalante@github/work/DDM/SimpleTTree/plots_example.py
        'HLT_DoubleL3Mu16_10NoVtx_DxyMin0p01cm_v2'          # From aescalante@github/work/DDM/SimpleTTree/plots_example.py
    ]

def join_triggers(trig_list):
    return ' || '.join([f'trig_hlt_path == \"{trigger}\"' for trigger in trig_list])

def join_selection(sel_list):
    return '('+') && ('.join(sel_list)+')'

data_friend = [
            '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022B-ReReco-v2.root',
            '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022C-ReReco-v2.root'
        ]


# signal_100          = f'/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/StopToMuB_v05/StopToMuB_100_{signal_ctau}.root'
# signal_100_friend   = f'/pnfs/ciemat.es/data/cms/store/user/escalant/displacedLeptons/StopToMuB_v05/StopToMuB_100_{signal_ctau}.root'
# signal_100_weigth_BC = 73.648152

# signal_500          = f'/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/StopToMuB_v05/StopToMuB_500_{signal_ctau}.root'
# signal_500_friend   = f'/pnfs/ciemat.es/data/cms/store/user/escalant/displacedLeptons/StopToMuB_v05/StopToMuB_500_{signal_ctau}.root'
# signal_500_weigth_BC = 0.0269244036
for signal_ctau in signal_ctau_list:
    signal_100          = f'/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/SMuonToMuGravitino_01/SMuonToMuGravitino_100_{signal_ctau}.root'
    signal_100_friend   = f'/pnfs/ciemat.es/data/cms/store/user/escalant/displacedLeptons/testProduction_March2024/merged_files/ntuple_2022_SMuon_100_{signal_ctau}.root'
    signal_100_weigth_BC = 73.648152

    signal_500          = f'/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/SMuonToMuGravitino_01/SMuonToMuGravitino_500_{signal_ctau}.root'
    signal_500_friend   = f'/pnfs/ciemat.es/data/cms/store/user/escalant/displacedLeptons/testProduction_March2024/merged_files/ntuple_2022_SMuon_500_{signal_ctau}.root'
    signal_500_weigth_BC = 0.0269244036




    selection_list = [
        # '1',
        'patmu_nGood > 1',
        'patmu_nDisplaced > 1',
        # '(dimPD_mass < 80) || (dimPD_mass > 110)',                                # Introduce una depresión en la región 80-110 de dimDD si no se incluye lo de abajo porque se correlacionan
        # 'patmu_charge[dimPP_mu1_idx] != patmu_charge[dimPP_mu1_idx]',                            # parece ser importante para discriminar fondo
        # 'patmu_charge[patmu_mu1_isGood_d0_pv_idx] != patmu_charge[patmu_mu2_isGood_d0_pv_idx]',
        # 'patmu_d0sig_pv[patmu_mu1_isGood_d0_pv_idx] / patmu_d0sig_pv[patmu_mu2_isGood_d0_pv_idx] > 0.8',
        # 'patmu_pt[patmu_mu1_isGood_d0_pv_idx] > 10',
        # 'patmu_pt[patmu_mu2_isGood_d0_pv_idx] > 10'
    ]

    selection_global    = join_selection(selection_list)
    # selection_global    = None

    selection_data      = join_triggers(data_triggers)
    # selection_data      = None

    selection_signal    = join_triggers(signal_trigger_dict[signal])
    # selection_signal    = None


    branch = 'patmu_charge[patmu_mu1_isGood_d0_pv_idx] * patmu_charge[patmu_mu2_isGood_d0_pv_idx]'
    branch = 'patmu_d0sig_pv[patmu_mu1_isGood_d0_pv_idx] / patmu_d0sig_pv[patmu_mu2_isGood_d0_pv_idx]'

    # branch = 'patmu_d0sig_pv[patmu_mu1_isGood_d0_pv_idx]'
    branch = 'patmu_nDisplaced'
    # output = 'patmu_d0sig_pv__comparison'
    output = branch
    h = Hist(
        range       = (0,10)      ,
        nbins       = 10          ,
        logy        = True          ,
        # logx        = True          ,
        # norm        = True          ,
        selection   = selection_global,
    )

    h.add_data(branch,
        f'Data Eras B & C',
        data_src,
        'SimpleNTupler/DDTree',
        selection = selection_data,
        friend_path = data_friend,
        alias = 'Data_BC'
    )

    h.add_signal(branch,
        f'Stop 100 GeV {signal_ctau} mm',
        signal_100,
        'SimpleMiniNTupler/DDTree',
        selection = selection_signal,
        friend_path = signal_100_friend,
        # weight = signal_100_weigth_BC,
        alias=f'{signal}_100',
        # plot_type = "hist SAMES"
        
    )
    h.add_signal(branch,
        f'Stop 500 GeV {signal_ctau} mm',
        signal_500,
        'SimpleMiniNTupler/DDTree',
        selection = selection_signal,
        friend_path = signal_500_friend,
        # weight = signal_500_weigth_BC,
        alias = f'{signal}_500',
        # plot_type = 'hist SAMES'
    )
    # h.save_to('/nfs/cms/martialc/Displaced2024/llp/sandbox/figs/current')
    # h.save_to(f'/nfs/cms/martialc/Displaced2024/llp/sandbox/figs/{output}')
    effs[100].append(h.effs[f'{signal}_100'])
    effs[500].append(h.effs[f'{signal}_500'])
    del h

plt.plot(signal_ctau_list,effs[100],label='100 GeV')
plt.plot(signal_ctau_list,effs[500],label='500 GeV')
plt.savefig(f'{signal}_effs.png')
plt.show()