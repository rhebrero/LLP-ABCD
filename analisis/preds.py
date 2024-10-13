import ROOT as rt
import pdb
from files import *
from files_dicts import *
import cmsstyle as CMS
from functions import read_tree, Get_weight
import argparse
import os 
import sys
from ABCD_Filters import ABCD_Filters

curr_dir = os.path.dirname(os.path.abspath(__file__)) # Currently doing it like this, will need to add it to env var once it's organized
conf_dir = os.path.join(curr_dir, '..', 'config/')
conf_dir = os.path.normpath(conf_dir)
sys.path.append(conf_dir)
from config_test import *


dicts = {}


bkg_label = 'QCD_prueba'

sim_dict = QCD_dicts
data_dict = eraB_dict
fig_name = bkg_label


# filt.add_cuts(filt.Zmass_validation_cuts())
# filt.make_filters()

# pdb.set_trace()

def N_hists(dicts, d0sig_min, d0sig_max, filt, inbin=0, endbin=30, nbin=30, Tfactor=True):

    NA_tot = 0
    NB_tot = 0
    ND_tot = 0
    NC_tot = 0

    # pdb.set_trace()
    if not isinstance(dicts, list): dicts = [dicts]
    for dict in dicts:

        f, tree = read_tree(dict['file'])
        if 'x_sec' in dict: w = Get_weight(dict['x_sec'], dict['events'], lumi_DoubleMuonRun2022B)
        else: w = 1
        if 'SMuon' in dict['label']: # Temporary till Martin fixes the friend thing for smuons
            mass = dict['label'].split('_')[1]
            ctau = dict['label'].split('_')[2]
            tree.AddFriend('SimpleMiniNTupler/DDTree',f'/pnfs/ciemat.es/data/cms/store/user/escalant/displacedLeptons/testProduction_April_2024_v1/merged_files/ntuple_2022_SMuon_{mass}_{ctau}.root')
        if 'friend' in dict:
            tree.AddFriend('SimpleNTupler/DDTree', dict['friend'])

                    
        # pdb.set_trace()
        print(f"Peso para {dict['file']} es {w}")

        if not Tfactor:
            # ------A REGION-----------
            hist2d_A_m_10to = rt.TH1F("hist2d_A_m_10to", "d0 sig",nbin, inbin, endbin)
            tree.Draw("patmu_nGood >> hist2d_A_m_10to", filt.filters_D6D6_over_limit.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")

            NAA = hist2d_A_m_10to.Integral() 

            # ------D REGION-----------

            hist2d_D2D6_D_p = rt.TH1F("hist2d_D2D6_D_p", "d0 sig",nbin, inbin, endbin)
            tree.Draw("patmu_nGood >> hist2d_D2D6_D_p", filt.filters_D2D6_over_limit_D.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")

            hist2d_D_p = rt.TH1F("hist2d_D_p", "d0 sig",nbin, inbin, endbin)
            tree.Draw("patmu_nGood >> hist2d_D_p", filt.filters_PD6_over_limit_D.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")

            hist2d_A_D = rt.TH1F("hist2d_A_D", "d0 sig",nbin, inbin, endbin)
            tree.Draw("patmu_nGood >> hist2d_A_D", filt.filters_D6D6_under_limit_D.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")

            ND2D6_D_p = hist2d_D2D6_D_p.Integral()
            ND_p = hist2d_D_p.Integral()
            NAD = hist2d_A_D.Integral()

            NA_tot += NAA * w
            ND_tot += (ND2D6_D_p + ND_p + NAD) * w



        # ------B REGION-----------
        hist2d_D2D6_B_p = rt.TH1F("hist2d_D2D6_B_p", "d0 sig",nbin, inbin, endbin)
        tree.Draw("patmu_nGood >> hist2d_D2D6_B_p", filt.filters_D2D6_over_limit_B.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")

        hist2d_B_p = rt.TH1F("hist2d_B_p", "d0 sig",nbin, inbin, endbin)
        tree.Draw("patmu_nGood >> hist2d_B_p", filt.filters_PD6_over_limit_B.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")

        hist2d_A_B = rt.TH1F("hist2d_A_B", "d0 sig",nbin, inbin, endbin)
        tree.Draw("patmu_nGood >> hist2d_A_B", filt.filters_D6D6_under_limit_B.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")



        # ------C REGION-----------
        hist2d_C_m = rt.TH1F("hist2d_C_m", "d0 sig",nbin, inbin, endbin)
        tree.Draw("patmu_nGood >> hist2d_C_m", filt.filters_PP.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")

        hist2d_D2D2_m = rt.TH1F("hist2d_D2D2_m", "d0 sig", nbin, inbin, endbin)
        tree.Draw("patmu_nGood >> hist2d_D2D2_m", filt.filters_D2D2_C.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")
        
        hist2d_A_m_6to10 = rt.TH1F("hist2d_A_m_6to10", "d0 sig",nbin, inbin, endbin)
        tree.Draw("patmu_nGood >> hist2d_A_m_6to10", filt.filters_D6D6_under_limit_C.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")

        hist2d_B_m = rt.TH1F("hist2d_B_m", "d0 sig",nbin, inbin, endbin)
        tree.Draw("patmu_nGood >> hist2d_B_m", filt.filters_PD6_under_limit_B_C.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")

        hist2d_D_m = rt.TH1F("hist2d_D_m", "d0 sig",nbin, inbin, endbin)
        tree.Draw("patmu_nGood >> hist2d_D_m", filt.filters_PD6_under_limit_D_C.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")

        hist2d_D2D6_D_m = rt.TH1F("hist2d_D2D6_D_m", "d0 sig",nbin, inbin, endbin)
        tree.Draw("patmu_nGood >> hist2d_D2D6_D_m", filt.filters_D2D6_under_limit_D_C.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")

        hist2d_D2D6_B_m = rt.TH1F("hist2d_D2D6_B_m", "d0 sig",nbin, inbin, endbin)
        tree.Draw("patmu_nGood >> hist2d_D2D6_B_m", filt.filters_D2D6_under_limit_B_C.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")

        hist2d_PD2_D = rt.TH1F("hist2d_PD2_D", "d0 sig",nbin, inbin, endbin)
        tree.Draw("patmu_nGood >> hist2d_PD2_D", filt.filters_PD2_D_C.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")

        hist2d_PD2_B = rt.TH1F("hist2d_PD2_B", "d0 sig",nbin, inbin, endbin)
        tree.Draw("patmu_nGood >> hist2d_PD2_B", filt.filters_PD2_B_C.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")


        
        NAB = hist2d_A_B.Integral()
        NAC = hist2d_A_m_6to10.Integral() 
        


        NB_m = hist2d_B_m.Integral()
        NB_p = hist2d_B_p.Integral()
        NC =   hist2d_C_m.Integral() 
        ND_m = hist2d_D_m.Integral()
     
        ND2D2 =      hist2d_D2D2_m.Integral()
        ND2D6_B_m = hist2d_D2D6_B_m.Integral()
        ND2D6_D_m = hist2d_D2D6_D_m.Integral()
        ND2D6_B_p = hist2d_D2D6_B_p.Integral()
        

        NPD2_B = hist2d_PD2_B.Integral()
        NPD2_D = hist2d_PD2_D.Integral()


        NB_tot += (ND2D6_B_p + NB_p + NAB) * w
        NC_tot += (NAC + NC + ND2D2 + NPD2_D + NPD2_B + ND2D6_D_m + ND2D6_B_m + ND_m + NB_m) * w

        
 
    return NA_tot, NB_tot, NC_tot, ND_tot


def main():
    filt = ABCD_Filters()
    filt.add_cuts(filt.search_cuts())
    # filt.add_cuts(filt.more_cuts())
    # filt.add_cuts(filt.Smuon500_cuts())
    filt.make_filters()

    Data_dict = [eraB_dict]#, eraCDouble_dict, eraD_dict, eraE_dict, eraG_dict]
    # all_bkg_dicts = []
    # for kind in ['QCD', 'DYto2Mu200k', 'DYto2Tau']:
    #     all_bkg_dicts.extend(get_dict('background', kind, all=True))

    # NA_tot, NB_tot, NC_tot, ND_tot = N_hists(all_bkg_dicts, 4, 18, filt)
    NA_tot, NB_tot, NC_tot, ND_tot = N_hists(Data_dict, 4, 18, filt, Tfactor=False)

    # from map_ABCD_2D import hists_2d
    # hists,  NA_2d, NB_2d, NC_2d, ND_2d = hists_2d(eraB_dict, 0, 32, 32, 4, 18)
    print('For the search cuts')
    print(NA_tot, NB_tot, NC_tot, ND_tot)
    print('TF = ', NB_tot/NC_tot, ', SR/CR = ', NA_tot/ND_tot)



if __name__ == "__main__":
    main()

    #   


# NA_tot_data, NB_tot_data, NC_tot_data, ND_tot_data = N_hists(eraB_dict, 10, 0)
# NA_tot_sim, NB_tot_sim, NC_tot_sim, ND_tot_sim = N_hists(sim_dict, 0, 30, 30, 0, 15)


# print(NA_tot_sim/ND_tot_sim, NB_tot_sim/NC_tot_sim)
# print(NA_tot_data, ND_tot_data, NB_tot_data, NC_tot_data)


# f, data_tree = read_tree(data_dict['file']) # solo se pintan los datos, pero pesados con los cocientes

# hist_data = rt.TH1D('data', 'data', nbin, inbin, endbin)
# # data_tree.SetWeight(0.001)
# data_tree.Draw('dimD6D6_mass >> data', filt.filters_A_m_10to + "||" + filt.filters_A_p_10to, "goff")

# hist_data_pred = rt.TH1D('data pred', 'PD over PP data', nbin, inbin, endbin)
# data_tree.Draw('dimPD_mass >> data pred', filt.filters_D2D6_D_p + "||" + filt.filters_D_p + "||" + filt.filters_A_D, "goff")

# hist_PD_over_PP = rt.TH1D('PD_over_PP', 'PD over PP sim', nbin, inbin, endbin)
# data_tree.Draw('dimPD_mass >> PD_over_PP', filt.filters_D2D6_D_p + "||" + filt.filters_D_p + "||" + filt.filters_A_D, "goff")

# hist_D6D6_over_PD = rt.TH1D('D6D6_over_PD', 'D6D6 over PD sim', nbin, inbin, endbin)
# data_tree.Draw('dimPD_mass >> D6D6_over_PD', filt.filters_D2D6_D_p + "||" + filt.filters_D_p + "||" + filt.filters_A_D, "goff")

# hist_data_pred.Scale(NB_tot_data/NC_tot_data)
# hist_PD_over_PP.Scale(NB_tot_sim/NC_tot_sim)
# hist_D6D6_over_PD.Scale(NA_tot_sim/ND_tot_sim)

# y_max = 10 * max(hist_data.GetMaximum(), hist_data_pred.GetMaximum(), hist_D6D6_over_PD.GetMaximum(), hist_PD_over_PP.GetMaximum())


# Plot(
#     hist_data,
#     [hist_data_pred,
#     hist_D6D6_over_PD,
#     hist_PD_over_PP,],
#     0,500,
#     y_max,
#     f'ABCD_figs/ABCD_predictions{fig_name}',
#     bkg_label=fig_name
#     )