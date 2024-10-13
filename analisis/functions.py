import ROOT as rt
import pdb
import numpy as np
from files import *
from files_dicts import *
import cmsstyle as CMS
from xsec import getCrossSection as gxsec
from xsec import json

def Get_weight(x_sec, events, data_lumi):
    if not (x_sec or events or data_lumi): return 1

    weight = data_lumi * x_sec /events * 1000
    return weight


def Check_trigger(
        trigger_list: list, 
        trig_hlt_path: list
        ):
    
    fired = False
    for trigger in trig_hlt_path: 
        if trigger in trigger_list:
            fired = True
            break
    return fired  


def read_tree(file):

    if type(file)==list:
        
        tree_chain = rt.TChain('SimpleMiniNTupler/DDTree')
        [tree_chain.Add(minisample) for minisample in file]
        
        return None, tree_chain
    
    elif isinstance(file, rt.TChain): 
        return None, file

    else: 
    
        f = rt.TFile.Open(file)
        key = f.GetListOfKeys() # si hay mas TDirs habria que cambiarlo, habria mas componenetes en file.GetListOfKeys
        TDir = f.Get(key[0].GetName())
        tree = TDir.Get('DDTree')

        return f, tree

def GetLumi(dicts):
        eras_lumi = 0
        for dict in dicts: eras_lumi += dict['data_lumi']

        return eras_lumi

def getSignalWeight(dict, tree, data_lumi):
        if dict['susy'] == 'STau':
                json_file = "pp13600_sleptons_1000015_-1000015_NNLL.json"
        if dict['susy'] == 'SMuon':
                json_file = "pp13600_sleptons_1000011_-1000011_NNLL.json" 
        if dict['susy'] == 'STop':
                json_file = "pp13600_stopsbottom_NNLO+NNLL.json"
        
        weight = gxsec.get_weight(json_file, dict['mass'], tree.GetEntries(), data_lumi) # Lumi in pb within Albertos function

        return weight

def AdjustOverflow(hist):
        last_bin_content = hist.GetBinContent(hist.GetNbinsX()) # plot overflow in last bin
        overflow_content = hist.GetBinContent(hist.GetNbinsX() + 1)

        hist.SetBinContent(hist.GetNbinsX(), last_bin_content + overflow_content)
        hist.SetBinContent(hist.GetNbinsX() + 1, 0) # Clean overflow

        hist.SetBinError(hist.GetNbinsX(), (last_bin_content + overflow_content)**0.5)
        # Each line of SetBinContent, idk why, adds 1 entry when you try hist.GetEntries(). It's important for final bkg estimation, I subtract 2 latter


def TransfErr(hist, TF, TFerr):
        
        for i in range(1, hist.GetNbinsX() + 1):
                content = hist.GetBinContent(i)
                
                original_error = hist.GetBinError(i)

                scaled_content = content * TF
                

                if content > 0:
                        propagated_error = scaled_content * np.sqrt((TFerr / TF)**2 + (original_error / content)**2)
                else:
                        propagated_error = 0
                hist.SetBinError(i, propagated_error)


def get_bining(var_name): 
    '''
    Get proper bining for each variable
    '''
            
    bining_dict = {
        #  'invMass': [30, 0, 450],
        'invMass': [40, 0, 400],
        # 'invMass': [20, 70, 110], # For Zmass validation
         'DeltaR':  [30, 0, 6],
         'hasVtx':  [2, 0, 2],
         'd0sig':   [32, 18, 500], # validation
        #  'd0sig':   [30, 18, 170], # era B
         'pt':      [25 , 0, 250], #EL BUENO
        #  'pt':      [18, 0, 90], # PRUEBAS
         'iso':     [45, 0, 4.5],
         'd0':      [21, 0, 30],
         'd0err':   [30, -0.004, 0.004],
         'lxyerr':  [30, -0.4, 0.4]
    }

    if var_name not in bining_dict: raise ValueError('Not valid branch for bin getting')

    nbin = bining_dict[var_name][0]
    inbin = bining_dict[var_name][1]
    endbin = bining_dict[var_name][2]

    return nbin, inbin, endbin

def get_vars(var_name, region):
        '''
        Get proper vars names for each region
        '''

        vars_dict = {
                'A': {
                        'invMass': 'dimD6D6_mass',
                        'DeltaR':  'dimD6D6_deltaR',
                        'hasVtx':  'dimD6D6_hasVtx',
                        'd0sig':   ['patmu_d0sig_pv[dimD6D6_mu1_idx]', 
                                    'patmu_d0sig_pv[dimD6D6_mu2_idx]'],
                        'pt':      ['patmu_pt[dimD6D6_mu1_idx]',
                                    'patmu_pt[dimD6D6_mu2_idx]'],
                        'iso':     ['patmu_trackIso[dimD6D6_mu1_idx]/patmu_pt[dimD6D6_mu1_idx]', 
                                    'patmu_trackIso[dimD6D6_mu2_idx]/patmu_pt[dimD6D6_mu2_idx]'],
                        'd0':      ['abs(patmu_d0_pv[dimD6D6_mu1_idx])', 
                                    'abs(patmu_d0_pv[dimD6D6_mu2_idx])']
                },
                
                'D': {
                        'invMass': ['dimPD6_mass', 
                                    'dimD2D6_mass', 
                                    'dimD6D6_mass'],
                        'DeltaR':  ['dimPD6_deltaR', 
                                    'dimD2D6_deltaR', 
                                    'dimD6D6_deltaR'],
                        'hasVtx':  ['dimPD6_hasVtx', 
                                    'dimD2D6_hasVtx', 
                                    'dimD6D6_hasVtx'],
                        'd0sig':   ['abs(patmu_d0sig_pv[dimD6D6_mu1_idx])'] * 3,
                        'pt':      ['patmu_pt[dimD6D6_mu1_idx]'] * 3,
                        'iso':     ['patmu_trackIso[dimD6D6_mu1_idx]/patmu_pt[dimD6D6_mu1_idx]'] * 3,
                        'd0':      ['abs(patmu_d0_pv[dimD6D6_mu1_idx])'] * 3
                },

                'B': {
                        'invMass': ['dimPD6_mass', 
                                    'dimD2D6_mass', 
                                    'dimD6D6_mass'],
                        'DeltaR': ['dimPD6_deltaR', 
                                   'dimD2D6_deltaR', 
                                   'dimD6D6_deltaR'],
                        'hasVtx': ['dimPD6_hasVtx', 
                                   'dimD2D6_hasVtx', 
                                   'dimD6D6_hasVtx'],
                        'd0sig': ['abs(patmu_d0sig_pv[dimD6D6_mu1_idx])'] * 3,
                        'pt': ['patmu_pt[dimD6D6_mu1_idx]'] * 3,
                        'd0': ['abs(patmu_d0_pv[dimD6D6_mu1_idx])'] * 3
                },

                'C': {
                        'invMass': ['dimPP_mass', 'dimD2D2_mass', 'dimD6D6_mass', 'dimPD2_mass', 'dimD2D6_mass', 'dimPD6_mass'],
                        'DeltaR': ['dimPP_deltaR', 'dimD2D2_deltaR', 'dimD6D6_deltaR', 'dimPD2_deltaR', 'dimD2D6_deltaR', 'dimPD6_deltaR'],
                        'hasVtx': ['dimPP_hasVtx', 'dimD2D2_hasVtx', 'dimD6D6_hasVtx', 'dimPD2_hasVtx', 'dimD2D6_hasVtx', 'dimPD6_hasVtx'],
                        'd0sig': [['patmu_d0sig_pv[dimPP_mu1_idx]', 'patmu_d0sig_pv[dimD2D2_mu1_idx]', 'patmu_d0sig_pv[dimD6D6_mu1_idx]'], 
                                  ['patmu_d0sig_pv[dimPP_mu2_idx]', 'patmu_d0sig_pv[dimD2D2_mu2_idx]', 'patmu_d0sig_pv[dimD6D6_mu2_idx]']],
                        'pt': [['patmu_pt[dimPP_mu1_idx]', 'patmu_pt[dimD2D2_mu1_idx]', 'patmu_pt[dimD6D6_mu1_idx]'],
                               ['patmu_pt[dimPP_mu2_idx]', 'patmu_pt[dimD2D2_mu2_idx]', 'patmu_pt[dimD6D6_mu2_idx]']],
                        'd0': [['abs(patmu_d0_pv[dimPP_mu1_idx])', 'abs(patmu_d0_pv[dimD2D2_mu1_idx])', 'abs(patmu_d0_pv[dimD6D6_mu1_idx])'],
                               ['abs(patmu_d0_pv[dimPP_mu2_idx])', 'abs(patmu_d0_pv[dimD2D2_mu2_idx])', 'abs(patmu_d0_pv[dimD6D6_mu2_idx])']],
                        'd0err': [['patmu_d0_pv[dimPP_mu1_idx]/patmu_d0sig_pv[dimPP_mu1_idx]', 'patmu_d0_pv[dimD2D2_mu1_idx]/patmu_d0sig_pv[dimD2D2_mu1_idx]', 'patmu_d0_pv[dimD6D6_mu1_idx]/patmu_d0sig_pv[dimD6D6_mu1_idx]'],
                                  ['patmu_d0_pv[dimPP_mu2_idx]/patmu_d0sig_pv[dimPP_mu2_idx]', 'patmu_d0_pv[dimD2D2_mu2_idx]/patmu_d0sig_pv[dimD2D2_mu2_idx]', 'patmu_d0_pv[dimD6D6_mu2_idx]/patmu_d0sig_pv[dimD6D6_mu2_idx]']],
                        'lxyerr': [['patmu_d0_pv[dimPP_mu1_idx]/patmu_d0sig_pv[dimPP_mu1_idx]', 'patmu_d0_pv[dimD2D2_mu1_idx]/patmu_d0sig_pv[dimD2D2_mu1_idx]', 'patmu_d0_pv[dimD6D6_mu1_idx]/patmu_d0sig_pv[dimD6D6_mu1_idx]'],
                                   ['patmu_d0_pv[dimPP_mu2_idx]/patmu_d0sig_pv[dimPP_mu2_idx]', 'patmu_d0_pv[dimD2D2_mu2_idx]/patmu_d0sig_pv[dimD2D2_mu2_idx]', 'patmu_d0_pv[dimD6D6_mu2_idx]/patmu_d0sig_pv[dimD6D6_mu2_idx]']]
                }
        }

        vars = vars_dict[region][var_name]
        return vars


# Funcitons for events iterations ---------------------------------------------------------------------------------------------------------

def deltaPhi(phi1,phi2):
    '''
    computes delta phi for two given gen particles
    '''
    dphi = abs(phi1-phi2)
    if dphi > np.pi: dphi = 2*np.pi-dphi
    return dphi

def deltaR(event):
    pt1 = event.gen_pt[2]
    pt2 = event.gen_pt[3]
    eta1 = event.gen_eta[2]
    eta2 = event.gen_eta[3]
    phi1 = event.gen_phi[2]
    phi2 = event.gen_phi[3]

    muMass = 0.105660

    mu1 = rt.TLorentzVector()
    mu2 = rt.TLorentzVector()

    mu1.SetPtEtaPhiM(pt1, eta1, phi1, muMass)
    mu2.SetPtEtaPhiM(pt2, eta2, phi2, muMass)

    return mu1.DeltaR(mu2)

def invMass(event):
    pt1 = event.gen_pt[2]
    pt2 = event.gen_pt[3]
    eta1 = event.gen_eta[2]
    eta2 = event.gen_eta[3]
    phi1 = event.gen_phi[2]
    phi2 = event.gen_phi[3]

    muMass = 0.105660

    mu1 = rt.TLorentzVector()
    mu2 = rt.TLorentzVector()

    mu1.SetPtEtaPhiM(pt1, eta1, phi1, muMass)
    mu2.SetPtEtaPhiM(pt2, eta2, phi2, muMass)

    dim = mu1 + mu2

    rtinvariant_mass = dim.M()

    return rtinvariant_mass

def trig_check(triggers, event): # trigger checking for envets iterations
    for trig in triggers:
        if trig in event.trig_hlt_path:
            return True
    return False

