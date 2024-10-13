import ROOT as rt
import random
import argparse
import numpy as np
import pdb
from preds import N_hists
from functions import *
from files_dicts import *
from ABCD_Filters import ABCD_Filters
from ABCD_plot import C_hist, ABCD_pred

from config_test import *


# d0err_hist = C_hist([eraB_dict], 'd0err', filt, d0sig_min, d0sig_max)
# Dict = {'data': d0err_hist}
# # pdb.set_trace()
# mean = d0err_hist.GetMean()
# std_dev = d0err_hist.GetStdDev()


# HISTOGRAM FILLING-----------------------------------------------------------------------------------------------------------------------------------------------------

# Para las simulaciones de señal, en la informacion a nivel generador se tienen siempre 4 particulas, los índices 0 y 1 siempre corresponden a los Smuons y los idx 2 y 3 a los muones,
# ademas, el muon con idx 2 siempre es el de carga negativa y el de idx 3 de carga positiva


def artif_signal(signal_dict, 
                 nbin, 
                 inbin, 
                 endbin, 
                 var_name, 
                 data_lumi, 
                 give_N_sig=True, 
                 eff=False, 
                 weight=True, 
                 extra_cond=None,
                 d0sig_max_100=18,
                 ptCut100=37.5,
                 ptCut500=55,
                 massCut100=15,
                 massCut500=70):
    '''
    Function shoud return a dicts list and plot_hist should be able to plot no matter how many hists with their respectives labels and stuff
    '''
    hist = rt.TH1D("histogram", "artif d0sig", nbin, inbin, endbin)
    triggers = [
                'HLT_DoubleL2Mu23NoVtx_2Cha_CosmicSeed_v2',
                'HLT_DoubleL2Mu23NoVtx_2Cha_v2',
                'HLT_DoubleL2Mu23NoVtx_2Cha_CosmicSeed_v3',
                'HLT_DoubleL2Mu23NoVtx_2Cha_v3',
                'HLT_DoubleL2Mu10NoVtx_2Cha_VetoL3Mu0DxyMax1cm_v1',
                'HLT_DoubleL3Mu16_10NoVtx_DxyMin0p01cm_v1',
            ]

    file, tree = read_tree(signal_dict['file'])
    sig_label = signal_dict['label']

    if 'SMuon' in signal_dict['label']: # Temporary till Martin fixes the friend thing for smuons
        mass = sig_label.split('_')[1]
        ctau = sig_label.split('_')[2]
        tree.AddFriend('SimpleMiniNTupler/DDTree', f'/pnfs/ciemat.es/data/cms/store/user/escalant/displacedLeptons/testProduction_April_2024_v1/merged_files/ntuple_2022_SMuon_{mass}_{ctau}.root')
                        

    for i, event in enumerate(tree):
        sig_d0_mu1 = random.gauss(mu=-9.998090498152706e-05, sigma=0.0015517924005089628) #gaussian vlues obtained for sigma d0
        sig_d0_mu2 = random.gauss(mu=-9.998090498152706e-05, sigma=0.0015517924005089628)
        sig_lxy_vtx_mu1 = random.gauss(mu=0, sigma=0.0061734081784551404)
        sig_lxy_vtx_mu2 = random.gauss(mu=0, sigma=0.0061734081784551404)

        if len(event.gen_d0)==4: # gen info in signal ntuples is always given for the both smuons (idx=0,1) and the both muons (idx=2,3)
            artif_d0sig_mu1 = abs(event.gen_d0[2]/sig_d0_mu1)
            artif_d0sig_mu2 = abs(event.gen_d0[3]/sig_d0_mu2)

            resol_artif_lxysig_vtx = abs(sig_lxy_vtx_mu1) + abs(sig_lxy_vtx_mu2)
            delta_artif_lxysig_vtx = abs(event.gen_Lxy[0] - event.gen_Lxy[1])

            dim_mass = invMass(event)
            delta_R = deltaR(event)

            # The usual old cuts
            mass_cond = (dim_mass>15 and (dim_mass>110 or dim_mass<70))
            d0sig_cond = (artif_d0sig_mu1>18 and artif_d0sig_mu2>18)
            d0cond = True #(abs(event.gen_d0[2])>0.1 and abs(event.gen_d0[3])>0.1)
            pt_cond = (event.gen_pt[2]>10 and event.gen_pt[3]>10)
            trig_cond = (trig_check(triggers, event))
            lxy_cond = (event.gen_Lxy[0]<60 and event.gen_Lxy[1]<60)

            # The other search's cuts
            hasVtx_cond = (delta_artif_lxysig_vtx < resol_artif_lxysig_vtx) # if true, both muons are considered to come from same vtx in resolution terms. I do it that way in order to match with Martins branch
            if extra_cond=='100':
                mass_cond = (dim_mass>float(massCut100) and (dim_mass>110 or dim_mass<70))
                pt_cond = (event.gen_pt[2]>float(ptCut100) and event.gen_pt[3]>float(ptCut100))
                d0sig_cond = (artif_d0sig_mu1>d0sig_max_100 and artif_d0sig_mu2>d0sig_max_100) # New d0sig condition for 100GeV

            elif extra_cond=='500':
                
                mass_cond = (dim_mass>float(massCut500) and (dim_mass>110 or dim_mass<70))
                pt_cond = (event.gen_pt[2]>float(ptCut500) and event.gen_pt[3]>float(ptCut500))
            # ...
            
            if d0sig_cond and mass_cond and pt_cond and trig_cond and lxy_cond and not hasVtx_cond and d0cond:
                
                if var_name=='d0sig':hist.Fill(artif_d0sig_mu2) # filled with the d0 of the positive muon, which is always the one with idx==3
                elif var_name=='invMass':hist.Fill(dim_mass)
                elif var_name=='pt':hist.Fill(event.gen_pt[3])
                elif var_name=='hasVtx':hist.Fill(delta_artif_lxysig_vtx < resol_artif_lxysig_vtx)
                elif var_name=='d0':hist.Fill(event.gen_d0[3])
                elif var_name=='DeltaR': hist.Fill(delta_R)

                else: raise ValueError('Invalid branch')

        else: #there are some empty events in each sim
            print('Event number', i, 'is empty')


    
    w = getSignalWeight(signal_dict, tree, data_lumi)
    
    print(f'Peso para la señal {sig_label}: ', w)

    if weight:
        hist.Scale(w)
    else: pass

    print("Signal histogram events: ", hist.GetEntries(), ", painted events: ", hist.GetEntries() * w)

    if eff: 
         effi = hist.GetEntries() / tree.GetEntries()
         print(f'Signal effinciency: {effi}')
         return effi
    
    elif give_N_sig: return hist, hist.GetEntries() * w
    else:return hist

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--branch', dest='branch', required=False, default='d0sig')
    parser.add_argument('--mass', dest='mass', required=False, default='')

    args = parser.parse_args()
    mass = args.mass

    filt = ABCD_Filters()
    filt.add_cuts(filt.search_cuts())
    filt.add_cuts(filt.more_cuts())


    Data_dicts = [eraB_dict]
    # Data_dicts = [eraCDouble_dict, eraD_dict, eraE_dict, eraG_dict]#, eraC_dict]
    data_lumi = 0
    for data_dict in Data_dicts: data_lumi += data_dict['data_lumi'] 

    dict_SMuon_500_1000 = signal_SMuon_500_1000_dict
    dict_SMuon_100_1000 = signal_SMuon_100_1000_dict
    dict_SMuon_100_10000 = signal_SMuon_100_10000_dict

    region = 'A'
    var_name = args.branch
    
    d0sig_min = 4
    d0sig_max = 18
    
    nbin, inbin, endbin = get_bining(var_name)

    if mass=='100': 
        filt.add_cuts(filt.Smuon100_cuts())
        filt.make_filters()
        hist_SMuon_100_1000, N_SMuon_100_1000 = artif_signal(dict_SMuon_100_1000, nbin, inbin, endbin, var_name=var_name, give_N_sig=True, data_lumi=data_lumi, extra_cond='100')
        Ns = {'SMuon_100_1000': N_SMuon_100_1000}
        
        Dict = {
            "#tilde{#mu}#rightarrow#mu#tilde{G}, m_{#tilde{#mu}} = 100 GeV, c#tau = 100cm": hist_SMuon_100_1000,
        }

    elif mass=='500':
        filt.add_cuts(filt.Smuon500_cuts())
        filt.make_filters()
        hist_SMuon_500_1000, N_SMuon_500_1000 = artif_signal(dict_SMuon_500_1000, nbin, inbin, endbin, var_name=var_name, give_N_sig=True, data_lumi=data_lumi, extra_cond='500')
        Ns = {'SMuon_500_1000': N_SMuon_500_1000}

        Dict = {
        "#tilde{#mu}#rightarrow#mu#tilde{G}, m_{#tilde{#mu}} = 500 GeV, c#tau = 100cm": hist_SMuon_500_1000,
        }

    else: 
        filt.make_filters()
        hist_SMuon_100_1000, N_SMuon_100_1000 = artif_signal(dict_SMuon_100_1000, nbin, inbin, endbin, var_name=var_name, give_N_sig=True, data_lumi=data_lumi)
        hist_SMuon_500_1000, N_SMuon_500_1000 = artif_signal(dict_SMuon_500_1000, nbin, inbin, endbin, var_name=var_name, give_N_sig=True, data_lumi=data_lumi)
        Ns = {'SMuon_100_1000':N_SMuon_100_1000, 
              'SMuon_500_1000': N_SMuon_500_1000}

        Dict = {
            "#tilde{#mu}#rightarrow#mu#tilde{G}, m_{#tilde{#mu}} = 500 GeV, c#tau = 100cm": hist_SMuon_500_1000,
            "#tilde{#mu}#rightarrow#mu#tilde{G}, m_{#tilde{#mu}} = 100 GeV, c#tau = 100cm": hist_SMuon_100_1000,
        }


    N_bkg = ABCD_pred(Dict, var_name, f'BCDEG_MoreCuts_{mass}{var_name}_{region}', True, filt, Data_dicts, give_N_bkg=True, dataFull=True, lumi=str(data_lumi), path='CutsToDataFull/')#, d0sig_max=35)


    print(f'There are {N_bkg} predicted bkg events in the sinal region')

    for key, N in Ns.items(): 
        print(f'Signal events for {key}: ', N)
        print(f'Signal significance for {key}: ', N/N_bkg**0.5)

