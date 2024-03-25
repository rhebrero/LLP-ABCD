import ROOT as rt
import numpy as np
from llp.utils.macros import load_macro
from llp.pyroot.plots import Canvas, Histogram
import numpy as np

# Para que no muestre errores en ttreeformula
rt.RooMsgService.instance().setGlobalKillBelow(rt.RooFit.ERROR)


# =================================================================================================
data_triggers = [
    'HLT_DoubleL2Mu23NoVtx_2Cha_v2',                    # Para Era B
    'HLT_DoubleL2Mu23NoVtx_2Cha_v3',                    # para Era C
    'HLT_DoubleL2Mu10NoVtx_2Cha_VetoL3Mu0DxyMax1cm_v1', # From aescalante@github/work/DDM/SimpleTTree/plots_example.py
    'HLT_DoubleL3Mu16_10NoVtx_DxyMin0p01cm_v1'          # From aescalante@github/work/DDM/SimpleTTree/plots_example.py
]

signal_triggers = {
    'STop'      : [
        'HLT_DoubleL2Mu23NoVtx_2Cha_CosmicSeed_v3' ,
        'HLT_DoubleL2Mu23NoVtx_2Cha_v3' ,
        'HLT_DoubleL2Mu10NoVtx_2Cha_VetoL3Mu0DxyMax1cm_v2' ,
        'HLT_DoubleL3Mu16_10NoVtx_DxyMin0p01cm_v2'
    ],
    'SMuon'     : [
        'HLT_DoubleL2Mu23NoVtx_2Cha_CosmicSeed_v2' ,
        'HLT_DoubleL2Mu23NoVtx_2Cha_v2' ,
        'HLT_DoubleL2Mu10NoVtx_2Cha_VetoL3Mu0DxyMax1cm_v1' ,
        'HLT_DoubleL3Mu16_10NoVtx_DxyMin0p01cm_v1'
    ]
}


data_src    = '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_B.root'
data_friend = [
            '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022B-ReReco-v2.root',
            # '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022C-ReReco-v2.root'
        ]


signal_100          = {
    'STop'  : '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/StopToMuB_v05/StopToMuB_100_{ctau}.root',
    'SMuon' : '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/SMuonToMuGravitino_v01/SMuonToMuGravitino_100_{ctau}.root'
}
signal_100_friend   = {
    'STop'  : '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedLeptons/StopToMuB_v05/StopToMuB_100_{ctau}.root',
    'SMuon' : '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedLeptons/testProduction_March2024/merged_files/ntuple_2022_SMuon_100_{ctau}.root'
} 

signal_500          = {
    'STop'  : '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/StopToMuB_v05/StopToMuB_500_{ctau}.root',
    'SMuon' : '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/SMuonToMuGravitino_v01/SMuonToMuGravitino_500_{ctau}.root'
}
signal_500_friend   = {
    'STop'  : '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedLeptons/StopToMuB_v05/StopToMuB_500_{ctau}.root',
    'SMuon' : '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedLeptons/testProduction_March2024/merged_files/ntuple_2022_SMuon_500_{ctau}.root'
} 
signal_500_weigth_BC = 0.0269244036




# selection_list = [
#     # '1',
#     'patmu_nGood > 1',
#     # 'patmu_nDisplaced > 0',
#     # '(dimPD_mass < 80) || (dimPD_mass > 110)',                                # Introduce una depresión en la región 80-110 de dimDD si no se incluye lo de abajo porque se correlacionan
#     # 'patmu_charge[dimPP_mu1_idx] != patmu_charge[dimPP_mu1_idx]',                            # parece ser importante para discriminar fondo
#     # 'patmu_charge[patmu_mu1_isGood_d0_pv_idx] != patmu_charge[patmu_mu2_isGood_d0_pv_idx]',
#     # 'patmu_d0sig_pv[patmu_mu1_isGood_d0_pv_idx] / patmu_d0sig_pv[patmu_mu2_isGood_d0_pv_idx] > 0.8',
#     # 'patmu_pt[patmu_mu1_isGood_d0_pv_idx] > 10',
#     # 'patmu_pt[patmu_mu2_isGood_d0_pv_idx] > 10'
# ]
# ====================================================================================
ctau        = 1000 #mm
d0_min      = 0.01
D0Min       = str(d0_min).replace('.','p')
signal      = 'STop'
nbins       = 30
range       = (0,30)
branch      = 'patmu_nMuons'
output      = branch
global_cut  = {
    # 'OS'        :   '(dimPP_mu1_idx >= 0) && (dimPP_mu2_idx >= 0) && (patmu_charge[dimPP_mu1_idx] != patmu_charge[dimPP_mu2_idx])',
    '+2Good'        : 'patmu_nGood      > 1',
    f'MinD0_{D0Min}' : f'(abs(patmu_d0_pv[dimDD_mu1_idx]) > {d0_min}) && (abs(patmu_d0_pv[dimDD_mu2_idx]) > {d0_min})'

}
signal_cut  = {
    '+2Displaced'   : 'patmu_nDisplaced > 1'
}
data_cut    = {
    '+1Displaced'   : 'patmu_nDisplaced > 0',
    '+1Prompt'      : 'patmu_nPrompt    > 0',
}

total_eff   = {'data' : {}, '100' : {}, '500' : {}}
cut_eff     = {'data' : {}, '100' : {}, '500' : {}}
trig_eff    = {'data' : {}, '100' : {}, '500' : {}}

ctau_list = [1,10,100,1000,10000,100000]
# ====================================================================
for ctau in ctau_list:
    c = Canvas(f'canvas__{branch}_{signal}_{ctau}',
        logy = True
    )

    h_data = c.make_plot(Histogram,
        data_src,
        'SimpleNTupler/DDTree',
        branch,
        friend_path = data_friend,
        range = range,
        nbins = nbins,
        logy = True,
        alias = 'Data_B',
        trigger = dict(trig_hlt_path = data_triggers),
        cut     = dict(**data_cut, **global_cut),
        title = 'Data Era B'
    )
    h_100 = c.make_plot(Histogram,
        signal_100[signal].format(ctau=ctau),
        'SimpleMiniNTupler/DDTree',
        branch,
        friend_path = signal_100_friend[signal].format(ctau=ctau),
        range = range,
        nbins = nbins,
        logy = True,
        alias = f'{signal}_100_{ctau}',
        trigger = dict(trig_hlt_path = signal_triggers[signal]),
        cut     = dict(**signal_cut, **global_cut)
    )
    h_500 = c.make_plot(Histogram,
        signal_500[signal].format(ctau=ctau),
        'SimpleMiniNTupler/DDTree',
        branch,
        friend_path = signal_500_friend[signal].format(ctau=ctau),
        range = range,
        nbins = nbins,
        logy = True,
        alias = f'{signal}_500_{ctau}',
        trigger = dict(trig_hlt_path = signal_triggers[signal]),
        cut     = dict(**signal_cut, **global_cut)
    )

    hist_list = [h_data,h_100,h_500]
    [hist.eff_study() for hist in hist_list]

    # Añadimos las eficiencias
    total_eff['data'][ctau] = h_data.efficiency
    total_eff['100'] [ctau] = h_100.efficiency
    total_eff['500'] [ctau] = h_500.efficiency
    
    trig_eff ['data'][ctau] = h_data.trig_eff
    trig_eff ['100'] [ctau] = h_100.trig_eff
    trig_eff ['500'] [ctau] = h_500.trig_eff
    
    cut_eff  ['data'][ctau] = h_data.cut_eff
    cut_eff  ['100'] [ctau] = h_100.cut_eff
    cut_eff  ['500'] [ctau] = h_500.cut_eff

    c.save_to('/nfs/cms/martialc/Displaced2024/llp/sandbox/Hist/current')
    c.save_to(f'/nfs/cms/martialc/Displaced2024/llp/sandbox/Hist/{output}_{signal}_{ctau}')

    h_data.canvas.Close()
    h_100.canvas.Close()
    h_500.canvas.Close()
    c.Close()
# ==============================================
import pickle

eff_dict = {
    'total'     : total_eff,
    'trigger'   : trig_eff,
    'selection' : cut_eff
}
with open(f'/nfs/cms/martialc/Displaced2024/llp/dev/eff/{signal}_D0Min_{D0Min}__1e0_1e5.eff','wb+') as file:
    pickle.dump(eff_dict,file)