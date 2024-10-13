import ROOT as rt
import cmsstyle as CMS
import numpy as np
import pdb
from files_dicts import *
from files import * 
from functions import *
import argparse
from preds import N_hists
from Canvas import *
from ABCD_Filters import ABCD_Filters
from Canvas import Canvas_Class

from config_test import *




def All_good_hist(dicts, var_name, filt, d0sig_min, d0sig_max, data_lumi=lumi_DoubleMuonRun2022B):
        single_var = False

        nbin, inbin, endbin = get_bining(var_name)
        vars = get_vars(var_name, 'AllGood')

        total_histAll = rt.TH1D('total_histA', 'total_histA', nbin, inbin, endbin)
        histograms = {}
        trees = {}

        for dict in dicts:
                print(f"Corriendo sobre {dict['file']}")

                file, trees[f"{dict['label']}"]  = read_tree(dict['file'])
                if 'friend' in dict: trees[f"{dict['label']}"].AddFriend('SimpleNTupler/DDTree', dict['friend'])

                if 'SMuon' in dict['label']: # Temporary till Martin fixes the friend thing for smuons
                        mass = dict['label'].split('_')[1]
                        ctau = dict['label'].split('_')[2]
                        trees[f"{dict['label']}"].AddFriend('SimpleMiniNTupler/DDTree',f'/pnfs/ciemat.es/data/cms/store/user/escalant/displacedLeptons/testProduction_April_2024_v1/merged_files/ntuple_2022_SMuon_{mass}_{ctau}.root')
                        

                if 'x_sec' in dict: w = Get_weight(dict['x_sec'], dict['events'], data_lumi)
                elif 'susy' in dict: 
                        w = getSignalWeight(dict, trees[f"{dict['label']}"], data_lumi)
                        print('Signal weight: ', w)
                else: w=1


                if single_var:

                        histograms[f"hist_All{dict['label']}1"] = rt.TH1D( f"histAll{dict['label']}1", 'histAll1', nbin, inbin, endbin)
                        histograms[f"hist_All{dict['label']}2"] = rt.TH1D( f"histAll{dict['label']}2", 'histAll2', nbin, inbin, endbin)
                        
                        trees[f"{dict['label']}"].Draw(vars[1] + f">> histAll{dict['label']}2",  filt.Filters_All_muons + '&& (patmu_charge[patmu_isGood_d0_pv_idx[1]]==1)', "goff") # quitar lo ultimo para SS
                        trees[f"{dict['label']}"].Draw(vars[0] + f">> histAll{dict['label']}1",  filt.Filters_All_muons + '&& (patmu_charge[patmu_isGood_d0_pv_idx[0]]==1)', "goff")
                        
                        histograms[f"hist_All{dict['label']}1"].Scale(w)
                        histograms[f"hist_All{dict['label']}2"].Scale(w)
                        
                        
                        total_histAll.Add(histograms[f"hist_All{dict['label']}1"])
                        total_histAll.Add(histograms[f"hist_All{dict['label']}2"])
                else:
                        histograms[f"hist_All{dict['label']}"] = rt.TH1D( f"histAll{dict['label']}", 'histAll1', nbin, inbin, endbin)

                        trees[f"{dict['label']}"].Draw(vars + f">> histAll{dict['label']}",  filt.Filters_All_muons, "goff")

                        histograms[f"hist_All{dict['label']}"].Scale(w)

                        total_histAll.Add(histograms[f"hist_All{dict['label']}"])


                print(f'entries = {total_histAll.Integral()}, {total_histAll.GetEntries()}', w)



        del trees
        del histograms

        return total_histAll


def A_hist(dicts, var_name, filt, d0sig_min, d0sig_max, data_lumi=lumi_DoubleMuonRun2022B, SS=False):

        nbin, inbin, endbin = get_bining(var_name)
        vars = get_vars(var_name, 'A')
        if isinstance(vars, list): single_var = True # True if var isn't a dimuon var
        else: single_var = False

        total_histA = rt.TH1D('total_histA', 'total_histA', nbin, inbin, endbin)
        histograms = {}
        trees = {}
        
        for dict in dicts:
                print(f"Corriendo sobre {dict['file']}")

                file, trees[f"{dict['label']}"]  = read_tree(dict['file'])
                if 'friend' in dict: trees[f"{dict['label']}"].AddFriend('SimpleNTupler/DDTree', dict['friend'])

                if 'SMuon' in dict['label']: # Martins retupled eras don't have friends
                        mass = dict['label'].split('_')[1]
                        ctau = dict['label'].split('_')[2]
                        trees[f"{dict['label']}"].AddFriend('SimpleMiniNTupler/DDTree',f'/pnfs/ciemat.es/data/cms/store/user/escalant/displacedLeptons/testProduction_April_2024_v1/merged_files/ntuple_2022_SMuon_{mass}_{ctau}.root')
                        

                if 'x_sec' in dict: w = Get_weight(dict['x_sec'], dict['events'], data_lumi)
                elif 'susy' in dict: 
                        w = getSignalWeight(dict, trees[f"{dict['label']}"], data_lumi)
                        print('Signal weight: ', w)
                else: w=1


                if single_var: # Hist separation by charge is made in order to plot every event but always the positive muon info when var isn't a dimuon global

                        histograms[f"hist_D6D6{dict['label']}1"] = rt.TH1D( f"histD6D6{dict['label']}1", 'histD6D61', nbin, inbin, endbin)
                        histograms[f"hist_D6D6{dict['label']}2"] = rt.TH1D( f"histD6D6{dict['label']}2", 'histD6D62', nbin, inbin, endbin)
                        
                        
                        if SS:
                                trees[f"{dict['label']}"].Draw(vars[1] + f">> histD6D6{dict['label']}2",  filt.total_filters_DD.format(signal_limit=d0sig_max, signal_inf=d0sig_min), "goff") # esto si SI se pide SS
                                trees[f"{dict['label']}"].Draw(vars[0] + f">> histD6D6{dict['label']}1",  filt.total_filters_DD.format(signal_limit=d0sig_max, signal_inf=d0sig_min), "goff")
                                
                                histograms[f"hist_D6D6{dict['label']}1"].Scale(0.5) # esto solo para SS, se pintan los dos muones quitando la condicion en carga y luego se divide entre dos
                                histograms[f"hist_D6D6{dict['label']}2"].Scale(0.5)

                        else:
                                trees[f"{dict['label']}"].Draw(vars[1] + f">> histD6D6{dict['label']}2",  filt.total_filters_DD.format(signal_limit=d0sig_max, signal_inf=d0sig_min) + '&& (patmu_charge[dimD6D6_mu2_idx]==1)', "goff") # Esto si no se pide SS
                                trees[f"{dict['label']}"].Draw(vars[0] + f">> histD6D6{dict['label']}1",  filt.total_filters_DD.format(signal_limit=d0sig_max, signal_inf=d0sig_min) + '&& (patmu_charge[dimD6D6_mu1_idx]==1)', "goff")

                        histograms[f"hist_D6D6{dict['label']}1"].Scale(w)
                        histograms[f"hist_D6D6{dict['label']}2"].Scale(w)
                        
                        total_histA.Add(histograms[f"hist_D6D6{dict['label']}1"])
                        total_histA.Add(histograms[f"hist_D6D6{dict['label']}2"])

                else:
                        histograms[f"hist_D6D6{dict['label']}"] = rt.TH1D( f"histD6D6{dict['label']}", 'histD6D61', nbin, inbin, endbin)

                        trees[f"{dict['label']}"].Draw(vars + f">> histD6D6{dict['label']}",  filt.total_filters_DD.format(signal_limit=d0sig_max, signal_inf=d0sig_min), "goff")

                        histograms[f"hist_D6D6{dict['label']}"].Scale(w)

                        total_histA.Add(histograms[f"hist_D6D6{dict['label']}"])


                print(f'A Region: integrated entries = {total_histA.Integral()}, total entries = {total_histA.GetEntries()}, weight = {w}')

                # print( f"{dict['label']} entries del tree = ", trees[f"{dict['label']}"].GetEntries(),"entries corte = ",  histograms[f"hist_D6D6{dict['label']}"].GetEntries()," ---> entries que se pintan = ",  histograms[f"hist_D6D6{dict['label']}"].Integral(), f"(w = {w})")


        del trees
        del histograms

        return total_histA


def D_hist(dicts, var_name, filt, d0sig_min, d0sig_max, tfactor=None):

        nbin, inbin, endbin = get_bining(var_name)
        vars = get_vars(var_name, 'D')
        
        total_histD = rt.TH1D('total_histD', 'total_histD', nbin, inbin, endbin)
        histograms = {}
        trees = {}
        
        for dict in dicts:
                print(f"Corriendo sobre {dict['file']}")
                file, trees[f"{dict['label']}"]  = read_tree(dict['file'])
                # if 'friend' in dict: trees[f"{dict['label']}"].AddFriend(dict['friend'])

                if 'SMuon' in dict['label']: 
                        mass = dict['label'].split('_')[1]
                        ctau = dict['label'].split('_')[2]
                        trees[f"{dict['label']}"].AddFriend('SimpleMiniNTupler/DDTree',f'/pnfs/ciemat.es/data/cms/store/user/escalant/displacedLeptons/testProduction_April_2024_v1/merged_files/ntuple_2022_SMuon_{mass}_{ctau}.root') # Temporary till Martin fixes the friend thing for smuons
        
                if 'friend' in dict:
                    trees[f"{dict['label']}"].AddFriend('SimpleNTupler/DDTree', dict['friend'])


                if 'x_sec' in dict: w = Get_weight(dict['x_sec'], dict['events'], lumi_DoubleMuonRun2022B)
                else: w=1

                histograms[f"hist_PD6{dict['label']}"] = rt.TH1D( f"histPD6{dict['label']}", 'histPD6', nbin, inbin, endbin)
                histograms[f"hist_D2D6{dict['label']}"] = rt.TH1D(f"histD2D6{dict['label']}", 'histD2D6', nbin, inbin, endbin)
                histograms[f"hist_D6D6{dict['label']}"] = rt.TH1D(f"histD6D6{dict['label']}", 'histD6D6', nbin, inbin, endbin)
                
                trees[f"{dict['label']}"].Draw(vars[0] + f">> histPD6{dict['label']}", filt.filters_PD6_over_limit_D.format(signal_limit=d0sig_max, signal_inf=d0sig_min)    , "goff") # doesn't contribute actually with current DD def
                trees[f"{dict['label']}"].Draw(vars[1] + f">> histD2D6{dict['label']}", filt.filters_D2D6_over_limit_D.format(signal_limit=d0sig_max, signal_inf=d0sig_min)  , "goff")
                trees[f"{dict['label']}"].Draw(vars[2] + f">> histD6D6{dict['label']}", filt.filters_D6D6_under_limit_D.format(signal_limit=d0sig_max, signal_inf=d0sig_min) , "goff")
                

                histograms[f"hist_PD6{dict['label']}"].Scale(w)
                histograms[f"hist_D2D6{dict['label']}"].Scale(w)
                histograms[f"hist_D6D6{dict['label']}"].Scale(w)
               
                total_histD.Add(histograms[f"hist_PD6{dict['label']}"])
                total_histD.Add(histograms[f"hist_D2D6{dict['label']}"])
                total_histD.Add(histograms[f"hist_D6D6{dict['label']}"])

                if tfactor: print(f'Predicted Bckg events = {total_histD.GetEntries() * tfactor}')
                else: print(f'D Region: integrated entries = {total_histD.Integral()}, total entries = {total_histD.GetEntries()}, weight = {w}')

        del trees
        del histograms
        
        return total_histD


def B_hist(dicts, var_name, filt, d0sig_min, d0sig_max):

        vars = get_vars(var_name, 'B')
        nbin, inbin, endbin = get_bining(var_name)

        total_histB = rt.TH1D('total_histB', 'total_histB', nbin, inbin, endbin)
        histograms = {}
        trees = {}
        
        for dict in dicts:
                print(f"Corriendo sobre {dict['file']}")

                file, trees[f"{dict['label']}"]  = read_tree(dict['file'])
                if 'friend' in dict: trees[f"{dict['label']}"].AddFriend('SimpleNTupler/DDTree', dict['friend'])


                histograms[f"hist_PD6{dict['label']}"] = rt.TH1D( f"histPD6{dict['label']}", 'histPD6', nbin, inbin, endbin)
                histograms[f"hist_D2D6{dict['label']}"] = rt.TH1D(f"histD2D6{dict['label']}", 'histD2D6', nbin, inbin, endbin)
                histograms[f"hist_D6D6{dict['label']}"] = rt.TH1D(f"histD6D6{dict['label']}", 'histD6D6', nbin, inbin, endbin)
                 
                
                if 'x_sec' in dict: w = Get_weight(dict['x_sec'], dict['events'], lumi_DoubleMuonRun2022B)
                else: w=1

                trees[f"{dict['label']}"].Draw(vars[0] + f">> histPD6{dict['label']}", filt.filters_PD6_over_limit_B.format(signal_limit=d0sig_max, signal_inf=d0sig_min), "goff")
                trees[f"{dict['label']}"].Draw(vars[1] + f">> histD2D6{dict['label']}", filt.filters_D2D6_over_limit_B.format(signal_limit=d0sig_max, signal_inf=d0sig_min), "goff")
                trees[f"{dict['label']}"].Draw(vars[2] + f">> histD6D6{dict['label']}", filt.filters_D6D6_under_limit_B.format(signal_limit=d0sig_max, signal_inf=d0sig_min), "goff")
                
                histograms[f"hist_PD6{dict['label']}"].Scale(w)
                histograms[f"hist_D2D6{dict['label']}"].Scale(w)
                histograms[f"hist_D6D6{dict['label']}"].Scale(w)
               
                total_histB.Add(histograms[f"hist_PD6{dict['label']}"])
                total_histB.Add(histograms[f"hist_D2D6{dict['label']}"])
                total_histB.Add(histograms[f"hist_D6D6{dict['label']}"])

                print(f'B Region: integrated entries = {total_histB.Integral()}, total entries = {total_histB.GetEntries()}, weight = {w}')


        del trees
        del histograms

        return total_histB


def C_hist(dicts, var_name, filt, d0sig_min, d0sig_max):
        nbin, inbin, endbin = get_bining(var_name)
        vars = get_vars(var_name, 'C')
        if isinstance(vars[0], list): single_var = True # True if var isn't a dimuon var
        else: single_var = False

        total_histC = rt.TH1D('total_histC', 'total_histC', nbin, inbin, endbin)
        histograms = {}
        trees = {}

        for dict in dicts:
                print(f"Corriendo sobre {dict['file']}")
                file, trees[f"{dict['label']}"]  = read_tree(dict['file'])
                if 'friend' in dict: trees[f"{dict['label']}"].AddFriend('SimpleNTupler/DDTree', dict['friend'])


                if 'SMuon' in dict['label']: # Martin's signal ntuples don't have friends
                        mass = dict['label'].split('_')[1]
                        ctau = dict['label'].split('_')[2]
                        trees[f"{dict['label']}"].AddFriend('SimpleMiniNTupler/DDTree',f'/pnfs/ciemat.es/data/cms/store/user/escalant/displacedLeptons/testProduction_April_2024_v1/merged_files/ntuple_2022_SMuon_{mass}_{ctau}.root')


                if 'x_sec' in dict: w = Get_weight(dict['x_sec'], dict['events'], lumi_DoubleMuonRun2022B)
                else: w=1
                
                if single_var:  # one hist for each branch composing PP region, includig +/- separation of the simetric ones (D2D2, D6D6, PP)
                        
                        # This juggling of filters has to be done due to the tricky definitions of the regions
                        histograms[f"hist_PP{dict['label']}1"] = rt.TH1D( f"histPP{dict['label']}1", 'histPP', nbin, inbin, endbin)
                        histograms[f"hist_PP{dict['label']}2"] = rt.TH1D( f"histPP{dict['label']}2", 'histPP', nbin, inbin, endbin)

                        histograms[f"hist_D2D2{dict['label']}1"] = rt.TH1D( f"histD2D2{dict['label']}1", 'histD2D2', nbin, inbin, endbin)
                        histograms[f"hist_D2D2{dict['label']}2"] = rt.TH1D( f"histD2D2{dict['label']}2", 'histD2D2', nbin, inbin, endbin)

                        histograms[f"hist_D6D6{dict['label']}1"] = rt.TH1D(f"histD6D6{dict['label']}1", 'histD6D6', nbin, inbin, endbin)
                        histograms[f"hist_D6D6{dict['label']}2"] = rt.TH1D(f"histD6D6{dict['label']}2", 'histD6D6', nbin, inbin, endbin)

                        histograms[f"hist_PD2{dict['label']}1"] = rt.TH1D( f"histPD2{dict['label']}1", 'histPD2', nbin, inbin, endbin)
                        histograms[f"hist_PD6{dict['label']}1"] = rt.TH1D(f"histPD6{dict['label']}1", 'histPD6', nbin, inbin, endbin)
                        histograms[f"hist_D2D6{dict['label']}1"] = rt.TH1D( f"histD2D6{dict['label']}1", 'histD2D6', nbin, inbin, endbin)

                        histograms[f"hist_PD2{dict['label']}2"] = rt.TH1D( f"histPD2{dict['label']}2", 'histPD2', nbin, inbin, endbin)
                        histograms[f"hist_PD6{dict['label']}2"] = rt.TH1D(f"histPD6{dict['label']}2", 'histPD6', nbin, inbin, endbin)
                        histograms[f"hist_D2D6{dict['label']}2"] = rt.TH1D( f"histD2D6{dict['label']}2", 'histD2D6', nbin, inbin, endbin)
                        

                        trees[f"{dict['label']}"].Draw(vars[0][0] + f">> histPP{dict['label']}1", filt.filters_PP.format(signal_limit=d0sig_max, signal_inf=d0sig_min) + ' && patmu_charge[dimPP_mu1_idx]==1', "goff") # + ' && patmu_charge[dimPP_mu1_idx]==1', "goff")
                        trees[f"{dict['label']}"].Draw(vars[1][0] + f">> histPP{dict['label']}2", filt.filters_PP.format(signal_limit=d0sig_max, signal_inf=d0sig_min) + ' && patmu_charge[dimPP_mu2_idx]==1', "goff") # + ' && patmu_charge[dimPP_mu2_idx]==1', "goff")
                        
                        trees[f"{dict['label']}"].Draw(vars[0][1] + f">> histD2D2{dict['label']}1", filt.filters_D2D2_C.format(signal_limit=d0sig_max, signal_inf=d0sig_min) + ' && patmu_charge[dimD2D2_mu1_idx]==1', "goff") # + ' && patmu_charge[dimD2D2_mu1_idx]==1', "goff")
                        trees[f"{dict['label']}"].Draw(vars[1][1] + f">> histD2D2{dict['label']}2", filt.filters_D2D2_C.format(signal_limit=d0sig_max, signal_inf=d0sig_min) + ' && patmu_charge[dimD2D2_mu2_idx]==1', "goff") # + ' && patmu_charge[dimD2D2_mu2_idx]==1', "goff")

                        trees[f"{dict['label']}"].Draw(vars[1][2] + f">> histD6D6{dict['label']}2", filt.filters_D6D6_under_limit_C.format(signal_limit=d0sig_max, signal_inf=d0sig_min) + ' && (patmu_charge[dimD6D6_mu2_idx]==1)', "goff") # + ' && patmu_charge[dimD6D6_mu2_idx]==1', "goff")
                        trees[f"{dict['label']}"].Draw(vars[0][2] + f">> histD6D6{dict['label']}1", filt.filters_D6D6_under_limit_C.format(signal_limit=d0sig_max, signal_inf=d0sig_min) + ' && (patmu_charge[dimD6D6_mu1_idx]==1)', "goff") # + ' && patmu_charge[dimD6D6_mu1_idx]==1', "goff")
                        
                        trees[f"{dict['label']}"].Draw(vars[0][0] + f">> histPD2{dict['label']}1", filt.filters_PD2_B_C.format(signal_limit=d0sig_max, signal_inf=d0sig_min), "goff")
                        trees[f"{dict['label']}"].Draw(vars[0][1] + f">> histPD2{dict['label']}2", filt.filters_PD2_D_C.format(signal_limit=d0sig_max, signal_inf=d0sig_min), "goff")
                        
                        trees[f"{dict['label']}"].Draw(vars[0][1] + f">> histD2D6{dict['label']}1", filt.filters_D2D6_under_limit_B_C.format(signal_limit=d0sig_max, signal_inf=d0sig_min), "goff")
                        trees[f"{dict['label']}"].Draw(vars[0][2] + f">> histD2D6{dict['label']}2", filt.filters_D2D6_under_limit_D_C.format(signal_limit=d0sig_max, signal_inf=d0sig_min), "goff")
                        
                        trees[f"{dict['label']}"].Draw(vars[0][0] + f">> histPD6{dict['label']}1", filt.filters_PD6_under_limit_B_C.format(signal_limit=d0sig_max, signal_inf=d0sig_min), "goff")
                        trees[f"{dict['label']}"].Draw(vars[0][2] + f">> histPD6{dict['label']}2", filt.filters_PD6_under_limit_D_C.format(signal_limit=d0sig_max, signal_inf=d0sig_min), "goff")

                        histograms[f"hist_PP{dict['label']}1"].Scale(w)
                        histograms[f"hist_PP{dict['label']}2"].Scale(w)

                        histograms[f"hist_D2D2{dict['label']}1"].Scale(w)
                        histograms[f"hist_D2D2{dict['label']}2"].Scale(w)
                        
                        histograms[f"hist_D6D6{dict['label']}1"].Scale(w)
                        histograms[f"hist_D6D6{dict['label']}2"].Scale(w)

                        histograms[f"hist_PD2{dict['label']}1"].Scale(w)
                        histograms[f"hist_PD6{dict['label']}1"].Scale(w)
                        histograms[f"hist_D2D6{dict['label']}1"].Scale(w)
                        
                        histograms[f"hist_PD2{dict['label']}2"].Scale(w)
                        histograms[f"hist_PD6{dict['label']}2"].Scale(w)
                        histograms[f"hist_D2D6{dict['label']}2"].Scale(w)

                        total_histC.Add(histograms[f"hist_PP{dict['label']}1"])
                        total_histC.Add(histograms[f"hist_PP{dict['label']}2"])
                        
                        total_histC.Add(histograms[f"hist_D2D2{dict['label']}1"])
                        total_histC.Add(histograms[f"hist_D2D2{dict['label']}2"])
                        
                        total_histC.Add(histograms[f"hist_D6D6{dict['label']}1"]) 
                        total_histC.Add(histograms[f"hist_D6D6{dict['label']}2"]) 
                        
                        total_histC.Add(histograms[f"hist_PD2{dict['label']}1"])                
                        total_histC.Add(histograms[f"hist_PD2{dict['label']}2"])

                        total_histC.Add(histograms[f"hist_PD6{dict['label']}1"])
                        total_histC.Add(histograms[f"hist_PD6{dict['label']}2"])

                        total_histC.Add(histograms[f"hist_D2D6{dict['label']}1"])
                        total_histC.Add(histograms[f"hist_D2D6{dict['label']}2"])

                        # Basically what I do is, since to obtain the C region I have to join several regions of the definitions, if I want to always paint the positive muon, in the regions without 
                        # explicit imposition of the charge, I add the charge condition for the cases to the filters in which dim1 is positive and cases in which dim2 is positive. 
                        # In regions with an explicit charge condition (i.e B,D) this is not necessary, I simply take the least or most displaced, depending on whether it is region B or D respectively.

                else :

                        histograms[f"hist_PP{dict['label']}"] = rt.TH1D( f"histPP{dict['label']}", 'histPP', nbin, inbin, endbin)
                        histograms[f"hist_D2D2{dict['label']}"] = rt.TH1D( f"histD2D2{dict['label']}", 'histD2D2', nbin, inbin, endbin)
                        histograms[f"hist_D6D6{dict['label']}"] = rt.TH1D(f"histD6D6{dict['label']}", 'histD6D6', nbin, inbin, endbin)

                        histograms[f"hist_PD2{dict['label']}1"] = rt.TH1D( f"histPD2{dict['label']}1", 'histPD2', nbin, inbin, endbin)
                        histograms[f"hist_PD6{dict['label']}1"] = rt.TH1D(f"histPD6{dict['label']}1", 'histPD6', nbin, inbin, endbin)
                        histograms[f"hist_D2D6{dict['label']}1"] = rt.TH1D( f"histD2D6{dict['label']}1", 'histD2D6', nbin, inbin, endbin)

                        histograms[f"hist_PD2{dict['label']}2"] = rt.TH1D( f"histPD2{dict['label']}2", 'histPD2', nbin, inbin, endbin)
                        histograms[f"hist_PD6{dict['label']}2"] = rt.TH1D(f"histPD6{dict['label']}2", 'histPD6', nbin, inbin, endbin)
                        histograms[f"hist_D2D6{dict['label']}2"] = rt.TH1D( f"histD2D6{dict['label']}2", 'histD2D6', nbin, inbin, endbin)
                        
                        trees[f"{dict['label']}"].Draw(vars[0] + f">> histPP{dict['label']}", filt.filters_PP.format(signal_limit=d0sig_max, signal_inf=d0sig_min), "goff")
                        trees[f"{dict['label']}"].Draw(vars[1] + f">> histD2D2{dict['label']}", filt.filters_D2D2_C.format(signal_limit=d0sig_max, signal_inf=d0sig_min), "goff")
                        trees[f"{dict['label']}"].Draw(vars[2] + f">> histD6D6{dict['label']}", filt.filters_D6D6_under_limit_C.format(signal_limit=d0sig_max, signal_inf=d0sig_min), "goff")
                        
                        trees[f"{dict['label']}"].Draw(vars[3] + f">> histPD2{dict['label']}1", filt.filters_PD2_B_C.format(signal_limit=d0sig_max, signal_inf=d0sig_min), "goff")
                        trees[f"{dict['label']}"].Draw(vars[3] + f">> histPD2{dict['label']}2", filt.filters_PD2_D_C.format(signal_limit=d0sig_max, signal_inf=d0sig_min), "goff")
                        
                        trees[f"{dict['label']}"].Draw(vars[4] + f">> histD2D6{dict['label']}1", filt.filters_D2D6_under_limit_B_C.format(signal_limit=d0sig_max, signal_inf=d0sig_min), "goff")
                        trees[f"{dict['label']}"].Draw(vars[4] + f">> histD2D6{dict['label']}2", filt.filters_D2D6_under_limit_D_C.format(signal_limit=d0sig_max, signal_inf=d0sig_min), "goff")
                       
                        trees[f"{dict['label']}"].Draw(vars[5] + f">> histPD6{dict['label']}1", filt.filters_PD6_under_limit_B_C.format(signal_limit=d0sig_max, signal_inf=d0sig_min), "goff")
                        trees[f"{dict['label']}"].Draw(vars[5] + f">> histPD6{dict['label']}2", filt.filters_PD6_under_limit_D_C.format(signal_limit=d0sig_max, signal_inf=d0sig_min), "goff")


                        histograms[f"hist_PP{dict['label']}"].Scale(w)
                        histograms[f"hist_D2D2{dict['label']}"].Scale(w)
                        histograms[f"hist_D6D6{dict['label']}"].Scale(w)
                        

                        histograms[f"hist_PD2{dict['label']}1"].Scale(w)
                        histograms[f"hist_PD2{dict['label']}2"].Scale(w)

                        histograms[f"hist_PD6{dict['label']}1"].Scale(w)
                        histograms[f"hist_PD6{dict['label']}2"].Scale(w)
                
                        histograms[f"hist_D2D6{dict['label']}1"].Scale(w)
                        histograms[f"hist_D2D6{dict['label']}2"].Scale(w)


                        total_histC.Add(histograms[f"hist_PP{dict['label']}"])
                        total_histC.Add(histograms[f"hist_D2D2{dict['label']}"])
                        total_histC.Add(histograms[f"hist_D6D6{dict['label']}"])
                        
                        total_histC.Add(histograms[f"hist_PD2{dict['label']}1"])                
                        total_histC.Add(histograms[f"hist_PD2{dict['label']}2"])                

                        total_histC.Add(histograms[f"hist_PD6{dict['label']}1"])
                        total_histC.Add(histograms[f"hist_PD6{dict['label']}2"])

                        total_histC.Add(histograms[f"hist_D2D6{dict['label']}1"])
                        total_histC.Add(histograms[f"hist_D2D6{dict['label']}2"])

                print(f'C Region: integrated entries = {total_histC.Integral()}, total entries = {total_histC.GetEntries()}, weight = {w}')



        del trees
        del histograms

        return total_histC
 

def ABCD_pred(hists_dict, var_name, label, pred, filt, 
              data_dict,
              d0sig_min=4, 
              d0sig_max=18, 
              give_N_bkg=False, 
              dataFull=False,
              lumi='0.11',
              save_plot=True,
              path = '',
              pred_label = 'Background',
              SS=False,
              Zmass=False):
              
        path = '/nfs/cms/rhebrero/work/analisis/' + path
        y_max = 0
        
        # leg = rt.TLegend(0.57, 0.66, 0.92, 0.81)
        leg = rt.TLegend(0.57, 0.75, 0.9, 0.88)

        colors = [rt.kRed, rt.kBlue, rt.kGreen, rt.kCyan, rt.kCyan+1, rt.kCyan+2, rt.kCyan+3]
        stack = rt.THStack("stack", "Stacked")
        stack_dic = {}

        Canvas = Canvas_Class(lumi=lumi)

        for i, (key, hist) in enumerate(hists_dict.items()):         
                if key in ["QCD", "DY #rightarrow #tau#tau", "DY #rightarrow #mu#mu"]: stack_dic[key] = hist

        
        if pred: 
                

                NA_data, NB_data, NC_data, ND_data = N_hists(data_dict, d0sig_min=4, d0sig_max=18, filt=filt) 
                print(NA_data, NB_data, NC_data, ND_data)
                err_C = np.sqrt(NC_data) 
                err_B = np.sqrt(NB_data)

                TransFactor = NB_data/NC_data
                err_TransFactor = TransFactor * np.sqrt((err_C / NC_data) ** 2 + (err_B / NB_data) ** 2)

                
                hist_D = D_hist(data_dict, f'{var_name}', filt, d0sig_min, d0sig_max, tfactor=TransFactor)

                AdjustOverflow(hist_D)
                TransfErr(hist_D, TransFactor, err_TransFactor) # Propagated error to bkg pred

                print("Transfer factor: ", TransFactor)

                hist_D.Scale(TransFactor)
                N_background = (hist_D.GetEntries() - 2) * TransFactor #Substract 2 because of the 2 entries addition in AdjustOverflow(hist_D)

                leg.AddEntry(hist_D, pred_label, 'f')

        

                if dataFull:
                        inbin =  hist_D.GetXaxis().GetXmin()
                        endbin = hist_D.GetXaxis().GetXmax()

                        if len(hists_dict)>0: y_max = max(max(hist.GetMaximum() for hist in hists_dict.values()), hist_D.GetMaximum())
                        else: y_max = hist_D.GetMaximum()

                        # canv = create_canvas(var_name, inbin, endbin, label, y_max, logy=True, lumi=lumi)
                        canv = Canvas.create_canvas(var_name, inbin, endbin, label, y_max, logy=True)

                        label = 'dataFull_' + label
                        CMS.cmsDraw(hist_D, 'hist', mcolor=0)

                        g_errors = rt.TGraphErrors(hist_D)
                        CMS.cmsDraw(g_errors, "2", fstyle=3002, fcolor=rt.kGray+3, lcolor=0, marker=0)    


                else:   
                        AdjustOverflow(hists_dict["data"])
                        inbin =  hists_dict["data"].GetXaxis().GetXmin()
                        endbin = hists_dict["data"].GetXaxis().GetXmax()
                        y_max = hists_dict["data"].GetMaximum()

                        canv = Canvas.create_ratio_canvas(var_name, inbin, endbin, label, y_max, logy=True)
                        
                        label = 'pred_' + label

                        canv.cd(1)

                        rt.gPad.SetPad(0.0, 0.32, 1.0, 1.0)  # Margen superior
                        rt.gPad.SetLogy()

                        latex = rt.TLatex()
                        latex.SetTextFont(42)
                        latex.SetTextSize(0.046)
                        latex.SetNDC()

                        if Zmass: 
                                latex.DrawLatex(0.19, 0.78, r"#bf{70 GeV < m_{#mu#mu} < 110 GeV}") # For Zmass Val
                                pred_color = 1181
                        if SS: 
                                latex.DrawLatex(0.25, 0.8, "#bf{SS (#mu^{+}#mu^{+} + #mu^{-}#mu^{-})}") # SS Val
                                pred_color = 1180
                        else: pred_color = rt.kYellow + 1
                        
                        CMS.cmsDraw(hist_D, 'hist', mcolor=0, fcolor=pred_color)
                        g_errors = rt.TGraphErrors(hist_D)
                        CMS.cmsDraw(g_errors, "2", fstyle=3002, fcolor=rt.kGray+3, lcolor=0, marker=0)    
                        

                        canv.Update()

                        ratio_hist = hists_dict['data'].Clone("ratio_hist")
                        ratio_hist.Divide(hist_D)
                        self_ratio_hist_ = hists_dict['data'].Clone("ratio_hist")
                        self_ratio_hist_.Divide(hists_dict['data'])

                        
                        canv.cd(2) # For some reason I have to draw cd(2) stuff afterwards, ratio points aren't painted correctly otherwise
                        
                        rt.gPad.SetPad(0.0, 0.02, 1.0, 0.3)
                        CMS.cmsDraw(ratio_hist, 'p')
                        ratio_hist.SetMarkerStyle(21)
                        ratio_hist.GetXaxis().SetTitleSize(1.2)

                        line = rt.TLine(inbin, 1, endbin, 1)
                        CMS.cmsDrawLine(line, lcolor=rt.kBlack, lstyle=rt.kDotted)

                        canv.cd(1)
                        
                        leg.AddEntry(hists_dict['data'], 'Data', 'p')
                        CMS.cmsDraw(hists_dict['data'], 'PE')
                        
                        canv.Update()


        else: # Just for normal plots of any region muons

                # Code below is just for d0err gaussian
                # mean = hists_dict['data'].GetMean()
                # std_dev = hists_dict['data'].GetStdDev()
                # gaussian = rt.TF1("gaussian", "gaus", inbin, endbin)
                # gaussian.SetParameters(hists_dict['data'].GetMaximum(), mean, std_dev)
                # hists_dict['data'].Fit(gaussian, "Q")


                y_max = max(hist.GetMaximum() for hist in hists_dict.values())
                inbin =  hists_dict['data'].GetXaxis().GetXmin()
                endbin = hists_dict['data'].GetXaxis().GetXmax()

                canv = Canvas.create_canvas(var_name, inbin, endbin, label, y_max)
                canv.SetLogy(True)
                leg.AddEntry(hists_dict['data'], 'Data', 'p')     
                CMS.cmsDrawStack(stack, leg, stack_dic)        
                CMS.cmsDraw(hists_dict['data'], 'PE')

        # # Code below is just for d0err gaussian  
        # leg.AddEntry(gaussian, 'Gaussian fit', 'f')
        # CMS.cmsDraw(gaussian, 'l') # just for d0err gaussian

        



        for i, (key, hist) in enumerate(hists_dict.items()):         
                if 'GeV' in key:        
                        AdjustOverflow(hist)
                        CMS.cmsDraw(hists_dict[key], 'hist F2', mcolor=colors[i]) #Temporary
                        leg.AddEntry(hist, key ,'l')
                        # CMS.cmsDraw(hists_dict["#tilde{t}, 100 GeV, 100mm"], 'hist F2', mcolor=rt.kBlue)
                
                if key == 'data': continue
                
                # else:
                #         leg.AddEntry(hist, key ,'l')
                #         # CMS.cmsDraw(hist, 'hist F2', mcolor=rt.kBlue)

        
        CMS.fixOverlay()
        leg.SetBorderSize(0)
        leg.Draw()
        canv.Draw()
                

        if save_plot: CMS.SaveCanvas(canv, path + label + ".png")

        if give_N_bkg: return N_background

if __name__=='__main__':

        parser = argparse.ArgumentParser()

        parser.add_argument('--branch', required=True)
        parser.add_argument('--region')
        parser.add_argument('--d0sig_min', default=4, type=int)
        parser.add_argument('--d0sig_max', default=18, type=int)
        parser.add_argument('--pred', default=False, action='store_true', help='If want the ABCD pred on the region')
        parser.add_argument('--dataFull', default=False, action='store_true', help='For using just the 13fb pred')
        parser.add_argument('--create_sigma', default=False, action='store_true', help='for artificial err vars on signal MC')
        parser.add_argument('--Zmass', default=False, action='store_true', help='For validation regions')
        parser.add_argument('--SS', default=False, action='store_true', help='For validation regions')
        parser.add_argument('--EraB', default=False, action='store_true', help='For validation regions')
        
        args = parser.parse_args()

        d0sig_min = args.d0sig_min
        d0sig_max = args.d0sig_max
        var_name = args.branch
        region = args.region
        pred = args.pred
        dataFull = args.dataFull
        create_sigma = args.create_sigma
        Zmass = args.Zmass
        SS = args.SS
        EraB = args.EraB

        print(d0sig_min, d0sig_max)

        All_bkg_dicts =  QCD_dicts #+ get_dict('background', 'DYto2Mu200k', all=True) + DYto2Tau_dicts 

        if dataFull: Data_dict = [eraB_dict]#, eraCDouble_dict, eraD_dict, eraE_dict, eraG_dict]#, eraC_dict]
        else:  
                Data_dict = [eraB_dict]#, eraCDouble_dict, eraD_dict, eraE_dict, eraG_dict]#, eraC_dict]

        eras_lumi = GetLumi(Data_dict)

        # Initialize filters from ABCD_Filters Class
        filt = ABCD_Filters()

        if EraB:
                Data_dict = [eraB_dict]
                filt.add_cuts(filt.search_cuts())
                # filt.add_cuts(filt.more_cuts())
                filt.make_filters()
                path = 'EraBValidation/Testing_'
                pred_label = 'Background'
                pred_label = 'ABCD Prediction'
        
        elif Zmass:
                Data_dict = [eraCDouble_dict, eraD_dict, eraE_dict, eraG_dict]
                filt.add_cuts(filt.Zmass_validation_cuts())
                # filt.add_cuts(filt.more_cuts())
                filt.make_filters()
                path = 'ZmassValidation/IsoCut_'
                pred_label = 'DY like background'

        elif SS:
                Data_dict = [eraCDouble_dict, eraD_dict, eraE_dict, eraG_dict]
                filt.add_cuts(filt.SS_validation_cuts())
                # filt.add_cuts(filt.more_cuts())
                filt.make_SS_filters()
                path = 'SSValidation/IsoCut_'
                pred_label = 'QCD like background'
        
        else:
                filt.add_cuts(filt.search_cuts())
                # filt.add_cuts(filt.more_cuts())

        

        if region == 'A':
                
                Dict = {
                        "data" : A_hist(Data_dict, f'{var_name}', filt, d0sig_min, d0sig_max, SS=SS),
                        # "#tilde{#mu}, 100 GeV, 100mm": A_hist([signal_SMuon_100_100_hist], f'{var_name}', filt, d0sig_min, d0sig_max),
                        # "#tilde{t}, 100 GeV, 100mm": A_hist([signal_STop_100_100_hist], f'{var_name}', filt, d0sig_min, d0sig_max),
                        # "DY #to #tau Simulation" : A_hist(DYto2Tau_dicts, f'{var_name}', filt, d0sig_min, d0sig_max, data_lumi=eras_lumi),
                        # "QCD Simulation" : A_hist(QCD_dicts, f'{var_name}', filt, d0sig_min, d0sig_max, data_lumi=eras_lumi),
                        # "DY #to #mu Simulation" : A_hist(get_dict('background', 'DYto2Mu200k', all=True), f'{var_name}', filt, d0sig_min, d0sig_max, data_lumi=eras_lumi),
                        # "data": A_hist(All_bkg_dicts, f'{var_name}'),
                }
                ABCD_pred(Dict, var_name, f'{var_name}_{region}_{d0sig_min}_{d0sig_max}', pred, filt, Data_dict, 
                          dataFull=dataFull, 
                          lumi=eras_lumi, 
                          path=path, 
                          pred_label=pred_label,
                          SS=SS, Zmass=Zmass)

        elif region == 'B':

                Dict = {
                        "data" : B_hist([eraB_dict], f'{var_name}', filt, d0sig_min, d0sig_max),
                        # "DY_Tau" : B_hist(DYto2Tau_dicts, f'{var_name}'),
                        # "QCD" : B_hist(QCD_dicts, f'{var_name}'),
                        # "DY_Mu" : C_hist(get_dict('background', 'DYto2Mu200k', all=True), f'{var_name}'),
                }

                ABCD_pred(Dict, var_name, f'{var_name}_{region}_{d0sig_min}_{d0sig_max}', pred, filt, Data_dict)

        elif region == 'C':

                Dict = {
                        "data" : C_hist([eraB_dict], f'{var_name}', filt, d0sig_min, d0sig_max),
                        "DY_Tau" : C_hist(DYto2Tau_dicts, f'{var_name}', filt, d0sig_min, d0sig_max),
                        "QCD" : C_hist(QCD_dicts, f'{var_name}', filt, d0sig_min, d0sig_max),
                        "DY_Mu" : C_hist(get_dict('background', 'DYto2Mu200k', all=True), f'{var_name}', filt, d0sig_min, d0sig_max),
                }

                ABCD_pred(Dict, var_name, f'{var_name}_{region}_{d0sig_min}_{d0sig_max}', pred, filt, Data_dict)

        elif region == 'D':

                Dict = {
                        "data" : D_hist([eraB_dict], f'{var_name}', filt=filt),
                        # "DY_Tau" : D_hist(DYto2Tau_dicts, f'{var_name}'),
                        # "QCD" : D_hist(QCD_dicts, f'{var_name}'),
                        # "DY_Mu" : D_hist(get_dict('background', 'DYto2Mu200k', all=True), f'{var_name}'),
                        # "data": D_hist(All_bkg_dicts, f'{var_name}'),
                }
                ABCD_pred(Dict, var_name, f'{var_name}_{region}_{d0sig_min}_{d0sig_max}', pred, filt, Data_dict)

        elif region == 'All':
                Dict = {
                        "data" : All_good_hist(Data_dict, f'{var_name}', filt, d0sig_min, d0sig_max),
                        "#tilde{#mu}, 100 GeV, 1000mm": All_good_hist([signal_SMuon_100_1000_dict], f'{var_name}', filt, d0sig_min, d0sig_max),
                        "#tilde{#mu}, 100 GeV, 100mm": All_good_hist([signal_SMuon_100_100_dict], f'{var_name}', filt, d0sig_min, d0sig_max),
                        "#tilde{#mu}, 100 GeV, 10mm": All_good_hist([signal_SMuon_100_10_dict], f'{var_name}', filt, d0sig_min, d0sig_max),

                        "#tilde{#mu}, 500 GeV, 1000mm": All_good_hist([signal_SMuon_500_1000_dict], f'{var_name}', filt, d0sig_min, d0sig_max),
                        "#tilde{#mu}, 500 GeV, 100mm": All_good_hist([signal_SMuon_500_100_dict], f'{var_name}', filt, d0sig_min, d0sig_max),
                        "#tilde{#mu}, 500 GeV, 10mm": All_good_hist([signal_SMuon_500_10_dict], f'{var_name}', filt, d0sig_min, d0sig_max),

                        # "#tilde{t}, 100 GeV, 100mm": A_hist([signal_STop_100_100_hist], f'{var_name}', filt, d0sig_min, d0sig_max),

                        # "DY #rightarrow #tau#tau" : All_hist(DYto2Tau_dicts, f'{var_name}', filt, d0sig_min, d0sig_max, data_lumi=eras_lumi),
                        # "QCD" : All_hist(QCD_dicts, f'{var_name}', filt, d0sig_min, d0sig_max, data_lumi=eras_lumi),
                        # "DY #rightarrow #mu#mu" : All_hist(get_dict('background', 'DYto2Mu200k', all=True), f'{var_name}', filt, d0sig_min, d0sig_max, data_lumi=eras_lumi),
                        # "data": A_hist(All_bkg_dicts, f'{var_name}'),
                }
                ABCD_pred(Dict, var_name, f'Signal_tests_{var_name}_{region}_{d0sig_min}_{d0sig_max}', pred, filt, Data_dict, dataFull=dataFull, lumi=eras_lumi)

        elif create_sigma:

                d0err_hist = C_hist([eraB_dict], 'd0err', filt, d0sig_min, d0sig_max)
                lxyerr_hist = C_hist([eraB_dict], 'lxyerr', filt, d0sig_min, d0sig_max)

                Dict_d0 = {'data': d0err_hist}
                Dict_lxy = {'data': lxyerr_hist}


                # mean = d0err_hist.GetMean()
                # std_dev = d0err_hist.GetStdDev()
                
                mean = lxyerr_hist.GetMean()
                std_dev = lxyerr_hist.GetStdDev()


                print(mean, std_dev)
                ABCD_pred(Dict_lxy, var_name, f'gauss_sigma_{var_name}_{region}_{d0sig_min}_{d0sig_max}', False, filt, Data_dict)
