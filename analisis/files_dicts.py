from files import *


data_type = 'data'
signal_type = 'signal' 
bckg_type = 'background'

data_hist = {
    'file':data_full,
    #'filters':filters_data_disp,
    'label':"data",
    'friends':tree_src,
    'type': data_type
}

eraB_dict = {
    'file':data_eraB,
    'label':"era_B",
    'type':data_type,
    'data_lumi': lumi_DoubleMuonRun2022B,
    'friend':eraB_bruto,
}   

eraCDouble_dict = {
    'file': data_eraCDouble,
    'label': 'era_CDouble',
    'type':data_type,
    'data_lumi':lumi_DoubleMuonRun2022C,
    'friend': eraCDouble_bruto
}

eraC_dict = {
    'file': data_eraC,
    'label': 'era_C',
    'type':data_type,
    'data_lumi':lumi_MuonRun2022C,
    'friend': eraC_bruto
}

eraD_dict = {
    'file': data_eraD,
    'label': 'era_D',
    'type':data_type,
    'data_lumi':lumi_MuonRun2022D,
    'friend': eraD_bruto
}

eraE_dict = {
    'file': data_eraE,
    'label': 'era_E',
    'type':data_type,
    'data_lumi':lumi_MuonRun2022E,
    'friend': eraE_bruto
}

eraG_dict = {
    'file': data_eraG,
    'label': 'era_G',
    'type':data_type,
    'data_lumi':lumi_MuonRun2022G,
    'friend': eraG_bruto
}


data0_dict = {
    'file':data0,
    'label':"data0",
    'type':signal_type
}


data1e5_dict = {
    'file':data2e5,
    'label':"data1e5",
    'type':signal_type
}


# ----------------------------------------


signal_STop_500_1_hist = {
    'file':signal_STop_500_1,
    #'filters':filters_signal_disp,
    'label':"STop_500_1",
    'susy':'STop',
    'mass':500,
    
    'type': signal_type 
}

signal_SMuon_500_1_dict = {
    'file':signal_SMuon_500_1,
    #'filters':filters_signal_disp,
    'label':"SMuon_500_1",
    'susy':'SMuon',
    'mass':500,
    
    'type': signal_type
}


signal_STop_500_10_hist = {
    'file':signal_STop_500_10,
    #'filters':filters_signal_disp,
    'label':"STop_500_10",
    'susy':'STop',
    'mass':500,
    
    'type': signal_type 
}

signal_SMuon_500_10_dict = {
    'file':signal_SMuon_500_10,
    #'filters':filters_signal_disp,
    'label':"SMuon_500_10",
    'susy':'SMuon',
    'mass':500,
    
    'type': signal_type
}


signal_STop_500_100_hist = {
    'file':signal_STop_500_100,
    #'filters':filters_signal_disp,
    'label':"STop_500_100",
    'susy':'STop',
    'mass':500,
    
    'type': signal_type 
}

signal_SMuon_500_100_dict = {
    'file':signal_SMuon_500_100,
    #'filters':filters_signal_disp,
    'label':"SMuon_500_100",
    'susy':'SMuon',
    'mass':500,
    
    'type': signal_type
}



signal_STop_500_1000_hist = {
    'file':signal_STop_500_1000,
    #'filters':filters_signal_disp,
    'label':"STop_500_1000",
    'susy':'STop',
    'mass':500,
    
    'type': signal_type 
}

signal_SMuon_500_1000_dict = {
    'file':signal_SMuon_500_1000,
    #'filters':filters_signal_disp,
    'label':"SMuon_500_1000",
    'susy':'SMuon',
    'mass':500,
    
    'type': signal_type
}


signal_STop_500_10000_hist = {
    'file':signal_STop_500_10000,
    #'filters':filters_signal_disp,
    'label':"STop_500_10000",
    'susy':'STop',
    'mass':500,
    
    'type': signal_type 
}

signal_SMuon_500_10000_dict = {
    'file':signal_SMuon_500_10000,
    #'filters':filters_signal_disp,
    'label':"SMuon_500_10000",
    'susy':'SMuon',
    'mass':500,
    
    'type': signal_type
}

signal_STop_500_100000_hist = {
    'file':signal_STop_500_100000,
    #'filters':filters_signal_disp,
    'label':"STop_500_100000",
    'susy':'STop',
    'mass':500,
    
    'type': signal_type 
}

signal_SMuon_500_100000_dict = {
    'file':signal_SMuon_500_100000,
    #'filters':filters_signal_disp,
    'label':"SMuon_500_100000",
    'susy':'SMuon',
    'mass':500,
    
    'type': signal_type
}

# -----

signal_STop_100_1_hist = {
    'file':signal_STop_100_1,
    #'filters':filters_signal_disp,
    'label':"STop_100_1",
    'susy':'STop',
    'mass':100,
    
    'type': signal_type 
}

signal_SMuon_100_1_dict = {
    'file':signal_SMuon_100_1,
    #'filters':filters_signal_disp,
    'label':"SMuon_100_1",
    'susy':'SMuon',
    'mass':100,
    
    'type': signal_type
}


signal_STop_100_10_hist = {
    'file':signal_STop_100_10,
    #'filters':filters_signal_disp,
    'label':"STop_100_10",
    'susy':'STop',
    'mass':100,
    
    'type': signal_type 
}

signal_SMuon_100_10_dict = {
    'file':signal_SMuon_100_10,
    #'filters':filters_signal_disp,
    'label':"SMuon_100_10",
    'susy':'SMuon',
    'mass':100,
    
    'type': signal_type
}


signal_STop_100_100_hist = {
    'file':signal_STop_100_100,
    #'filters':filters_signal_disp,
    'label':"STop_100_100",
    'susy':'STop',
    'mass':100,
    
    'type': signal_type 
}

signal_SMuon_100_100_dict = {
    'file':signal_SMuon_100_100,
    #'filters':filters_signal_disp,
    'label':"SMuon_100_100",
    'susy':'SMuon',
    'mass':100,
    
    'type': signal_type
}



signal_STop_100_1000_hist = {
    'file':signal_STop_100_1000,
    #'filters':filters_signal_disp,
    'label':"STop_100_1000",
    'susy':'STop',
    'mass':100,
    
    'type': signal_type 
}

signal_SMuon_100_1000_dict = {
    'file':signal_SMuon_100_1000,
    #'filters':filters_signal_disp,
    'label':"SMuon_100_1000",
    'susy':'SMuon',
    'mass':100,
    
    'type': signal_type
}


signal_STop_100_10000_hist = {
    'file':signal_STop_100_10000,
    #'filters':filters_signal_disp,
    'label':"STop_100_10000",
    'susy':'STop',
    'mass':100,
    
    'type': signal_type 
}

signal_SMuon_100_10000_dict = {
    'file':signal_SMuon_100_10000,
    #'filters':filters_signal_disp,
    'label':"SMuon_100_10000",
    'susy':'SMuon',
    'mass':100,
    
    'type': signal_type
}

signal_STop_100_100000_hist = {
    'file':signal_STop_100_100000,
    #'filters':filters_signal_disp,
    'label':"STop_100_100000",
    'susy':'STop',
    'mass':100,
    
    'type': signal_type 
}

signal_SMuon_100_100000_dict = {
    'file':signal_SMuon_100_100000,
    #'filters':filters_signal_disp,
    'label':"SMuon_100_100000",
    'susy':'SMuon',
    'mass':100,
    
    'type': signal_type
}

SMuon_500_dicts_list = [
    signal_SMuon_500_1_dict, 
    signal_SMuon_500_10_dict,
    signal_SMuon_500_100_dict,
    signal_SMuon_500_1000_dict,
    signal_SMuon_500_10000_dict,
    signal_SMuon_500_100000_dict,
]

SMuon_100_dicts_list = [
    signal_SMuon_100_1_dict, 
    signal_SMuon_100_10_dict,
    signal_SMuon_100_100_dict,
    signal_SMuon_100_1000_dict,
    signal_SMuon_100_10000_dict,
    signal_SMuon_100_100000_dict,
]

# -----------------------------------------------

DYto2Mu_50to120_bruto_hist = {
    'file':DYto2Mu_50to120_bruto,
    'label':'DYto2Mu_50to120',
    'type':bckg_type,
    'kind': 'DYto2Mu',
    'x_sec':xsec_Zto2E_M_50_120,
    'events':10150330
}

DYto2Mu_50to120_dict = {
    'file':DYto2Mu_50to120,
    'label':'DYto2Mu_50to120',
    'type':bckg_type,
    'kind': 'DYto2Mu',
    'x_sec':xsec_Zto2E_M_50_120,
} 
DYto2Mu_120to200_dict = {
    'file':DYto2Mu_120to200,
    'label':'DYto2Mu_120to200',
    'type':bckg_type,
    'kind': 'DYto2Mu',
    'x_sec':xsec_Zto2E_M_120_200,
    'events':4999610
} 
DYto2Mu_200to400_dict = {
    'file':DYto2Mu_200to400,
    'label':'DYto2Mu_200to400',
    'type':bckg_type,
    'kind': 'DYto2Mu',
} 
# DYto2Mu_10to50_dict = {
#     'file':DYto2Mu_10to50,
#     'label':'DYto2Mu_10to50',
#     'type':bckg_type,
#     'kind': 'DYto2Mu',
# } 


DYto2Mu_400to800_dict = {
    'file':DYto2Mu_400to800,
    'label':'DYto2Mu_400to800',
    'type':bckg_type,
    'kind': 'DYto2Mu',
} 
DYto2Mu_800to1500_dict = {
    'file':DYto2Mu_800to1500,
    'label':'DYto2Mu_800to1500',
    'type':bckg_type,
    'kind': 'DYto2Mu',
} 

DYto2Mu_50to120_500k_dict = {
    'file':DYto2Mu_50to120_500k,
    'label':'DYto2Mu_50to120_500k',
    'type':bckg_type,
    'kind': 'DYto2Mu',
    'x_sec':xsec_Zto2E_M_50_120,
    'events': 5e5 / 3243545 * 10150330 # cogidas por martin / las del tree original * generadas originales 
}

DYto2Mu_120to200_500k_dict = {
    'file':DYto2Mu_120to200_500k,
    'label':'DYto2Mu_120to200_500k',
    'type':bckg_type,
    'kind': 'DYto2Mu',
    'x_sec':xsec_Zto2E_M_120_200,
    'events':5e5 / 2068737 * 4999610
}

DYto2Mu_10to50_500k_dict = {
    'file':DYto2Mu_10to50_500k,
    'label':'DYto2Mu_10to50_500k',
    'type':bckg_type,
    'kind': 'DYto2Mu',
    'x_sec':xsec_Zto2E_M_10_50,
    'events':5e5 / 9950 * 5026256
}

DYto2Mu_200to400_500k_dict = {
    'file':DYto2Mu_200to400_500k,
    'label':'DYto2Mu_200to400_500k',
    'type':bckg_type,
    'kind': 'DYto2Mu',
    'x_sec':xsec_Zto2E_M_200_400,
    'events':5e5 / 1517314 * 3051242
}

DYto2Mu_400to800_500k_dict = {
    'file':DYto2Mu_400to800_500k,
    'label':'DYto2Mu_400to800_500k',
    'type':bckg_type,
    'kind': 'DYto2Mu',
    'x_sec':xsec_Zto2E_M_400_800,
    'events':5e5 / 1771926 * 2930748
}

DYto2Mu_800to1500_500k_dict = {
    'file':DYto2Mu_800to1500_500k,
    'label':'DYto2Mu_800to1500_500k',
    'type':bckg_type,
    'kind': 'DYto2Mu',
    'x_sec':xsec_Zto2E_M_800_1500,
    'events':5e5 / 1464746 * 2088496
}

DYto2Mu_dicts = [
    # DYto2Mu_10to50_dict,
    DYto2Mu_50to120_dict,
    DYto2Mu_120to200_dict,
    DYto2Mu_200to400_dict,
    DYto2Mu_400to800_dict,
    DYto2Mu_800to1500_dict
]

DYto2Mu_dicts_500k = [
    DYto2Mu_10to50_500k_dict,
    DYto2Mu_120to200_500k_dict,
    DYto2Mu_50to120_500k_dict,
    DYto2Mu_200to400_500k_dict,
    DYto2Mu_400to800_500k_dict,
    DYto2Mu_800to1500_500k_dict
]

DYto2Tau_10to50_dict = {
    'file':DYto2Tau_10to50,
    'label':'DYto2Tau_10to50',
    'type':bckg_type,
    'kind': 'DYto2Tau',
    'x_sec':xsec_Zto2E_M_10_50,
    'events': 5249261,
} 

DYto2Tau_50to120_dict = {
    'file':DYto2Tau_50to120,
    'label':'DYto2Tau_50to120',
    'type':bckg_type,
    'kind': 'DYto2Tau',
    'x_sec':xsec_Zto2E_M_50_120,
    'events': 10293446,
} 

DYto2Tau_120to200_dict = {
    'file':DYto2Tau_120to200,
    'label':'DYto2Tau_120to200',
    'type':bckg_type,
    'kind': 'DYto2Tau',
    'x_sec':xsec_Zto2E_M_120_200,
    'events': 5249271,
} 


DYto2Tau_200to400_dict = {
    'file':DYto2Tau_200to400,
    'label':'DYto2Tau_200to400',
    'type':bckg_type,
    'kind': 'DYto2Tau',
    'x_sec':xsec_Zto2E_M_200_400,
    'events': 5249271, # El mismo numero que para 120to50, sospechoso
} 

DYto2Tau_400to800_dict = {
    'file':DYto2Tau_400to800,
    'label':'DYto2Tau_400to800',
    'type':bckg_type,
    'kind': 'DYto2Tau',
    'x_sec':xsec_Zto2E_M_400_800,
    'events': 3110408, 
} 

DYto2Tau_800to1500_dict = {
    'file':DYto2Tau_800to1500,
    'label':'DYto2Tau_800to1500',
    'type':bckg_type,
    'kind': 'DYto2Tau',
    'x_sec':xsec_Zto2E_M_800_1500,
    'events': 2205546,
} 

DYto2Tau_dicts = [
    DYto2Tau_10to50_dict,
    DYto2Tau_50to120_dict,
    DYto2Tau_120to200_dict,
    DYto2Tau_200to400_dict,
    DYto2Tau_400to800_dict,
    DYto2Tau_800to1500_dict,
]

QCD_15to20_dict = {
    'file':QCD_15to20,
    'label':'QCD_15to20',
    'type':bckg_type,
    'kind': 'QCD',
    'x_sec':2982000,
    'events': 16043927,
} 

QCD_20to30_dict = {
    'file':QCD_20to30,
    'label':'QCD_20to30',
    'type':bckg_type,
    'kind': 'QCD',
    'x_sec':2679000,
    'events': 111483708,
}

QCD_30to50_dict = {
    'file':QCD_30to50,
    'label':'QCD_30to50',
    'type':bckg_type,
    'kind': 'QCD',
    'x_sec':1465000,
    'events': 102293835,
}

QCD_50to80_dict = {
    'file':QCD_50to80,
    'label':'QCD_50to80',
    'type':bckg_type,
    'kind': 'QCD',
    'x_sec':402900,
    'events': 39602741,
}

QCD_80to120_dict = {
    'file':QCD_80to120,
    'label':'QCD_80to120',
    'type':bckg_type,
    'kind': 'QCD',
    'x_sec':95130,
    'events': 99098535,
}

QCD_120to170_dict = {
    'file':QCD_120to170,
    'label':'QCD_120to170',
    'type':bckg_type,
    'kind': 'QCD',
    'x_sec':22980,
    'events': 71567256,
}

QCD_170to300_dict = {
    'file':QCD_170to300,
    'label':'QCD_170to300',
    'type':bckg_type,
    'kind': 'QCD',
    'x_sec':7763,
    'events': 109948078,
}

QCD_300to470_dict = {
    'file':QCD_300to470,
    'label':'QCD_300to470',
    'type':bckg_type,
    'kind': 'QCD',
    'x_sec':699.1,
    'events': 103765161,
}

QCD_470to600_dict = {
    'file':QCD_470to600,
    'label':'QCD_470to600',
    'type':bckg_type,
    'kind': 'QCD',
    'x_sec':68.24,
    'events': 72202598,
}

QCD_600to800_dict = {
    'file':QCD_600to800,
    'label':'QCD_600to800',
    'type':bckg_type,
    'kind': 'QCD',
    'x_sec':21.37,
    'events': 72565100,
}

QCD_800to1000_dict = {
    'file':QCD_800to1000,
    'label':'QCD_800to1000',
    'type':bckg_type,
    'kind': 'QCD',
    'x_sec':3.913,
    'events': 131481400,
}

QCD_1000toInf_dict = {
    'file':QCD_1000toInf,
    'label':'QCD_1000toInf',
    'type':bckg_type,
    'kind': 'QCD',
    # 'x_sec':,
    'events': 45333749,
}

QCD_dicts = [
    QCD_15to20_dict,
    QCD_20to30_dict,
    QCD_30to50_dict,
    QCD_50to80_dict,
    QCD_80to120_dict,
    QCD_120to170_dict,
    QCD_170to300_dict,
    QCD_300to470_dict,
    QCD_470to600_dict,
    QCD_600to800_dict,
    QCD_800to1000_dict,
    # QCD_1000toInf,
]

