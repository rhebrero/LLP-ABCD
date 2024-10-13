import ROOT as rt
import pdb
import cmsstyle as CMS
from functions import read_tree
from GenSignalAnalisis import trig_check, invMass
import random
from files_dicts import eraB_dict
import numpy as np
from Canvas import create_canvas

def PP_deltaPhi(event, mu1, mu2):
    '''
    computes delta phi for two given gen particles
    '''
    dphi = abs(event.patmu_phi[mu1]-event.patmu_phi[mu2])
    if dphi > np.pi: dphi = 2*np.pi-dphi
    return dphi

def PP_mass(event, mu1, mu2):
    '''
    computes the invariant mass for two given gen particles
    '''
    try:
        mass2 = 2*event.patmu_pt[mu1]*event.patmu_pt[mu2]*(np.cosh(event.patmu_eta[mu1]-event.patmu_eta[mu2]) - np.cos(PP_deltaPhi(event, mu1, mu2)))
    except IndexError:
        pdb.set_trace()    
    mass = np.sqrt(mass2)
    return mass

def lxy_gaussian(signal_dict, ):
    
    hist = rt.TH1D("histogram", "artif lxy", 150, -0.1, 0.1)
    triggers = [
                'HLT_DoubleL2Mu23NoVtx_2Cha_CosmicSeed_v2',
                'HLT_DoubleL2Mu23NoVtx_2Cha_v2',
                'HLT_DoubleL2Mu23NoVtx_2Cha_CosmicSeed_v3',
                'HLT_DoubleL2Mu23NoVtx_2Cha_v3',
                'HLT_DoubleL2Mu10NoVtx_2Cha_VetoL3Mu0DxyMax1cm_v1',
                'HLT_DoubleL3Mu16_10NoVtx_DxyMin0p01cm_v1',
            ]

    file, tree = read_tree(signal_dict['file'])


    def PP_cond(event):

        if len(event.dim_mu1_idx)==0: return 0, False

        for i in range(len(event.dim_mu1_idx)):
            trig = (trig_check(triggers, event))

            if trig and event.dim_mu1_idx[i] > 999 and event.dim_mu2_idx[i] > 999:
                idx1 = event.dim_mu1_idx[i] - 1000
                idx2 = event.dim_mu2_idx[i] - 1000
                # pdb.set_trace()
                dim_mass = PP_mass(event, idx1, idx2)

                pterr = (event.patmu_ptError[idx1]/event.patmu_pt[idx1]<1 and event.patmu_ptError[idx2]/event.patmu_pt[idx2]<1)
                pt = (event.patmu_pt[idx1]>10 and event.patmu_pt[idx2]>10)

                nMatchedStations = (event.patmu_nMatchedStations[idx1]>1 and event.patmu_nMatchedStations[idx1]>1)
                nTrackerLayers = (event.patmu_nTrackerLayers[idx1]>5 and event.patmu_nTrackerLayers[idx2]>5)
                
                d0sig = (4<event.patmu_d0sig_pv[idx1]<18 and 4<event.patmu_d0sig_pv[idx2]<18)

                mass = (dim_mass>15 and 70<dim_mass<110)

                d0sig = True
                

                if pterr and pt and nMatchedStations and nTrackerLayers and d0sig and mass:
                    return i, True
                
                else:
                    return i, False
            
            else: 
                return i, False


    for event in tree:
        # trig_cond = (trig_check(triggers, event))

        try:
            i, cond = PP_cond(event)
        except TypeError:
            pdb.set_trace() 

        if cond:
            # pdb.set_trace()
            lxyerr = event.dim_Lxy_rpv[i]/event.dim_LxySig_rpv[i]
            hist.Fill(lxyerr)
            hist.Fill(-lxyerr)

        else: continue


    print("Histogram events: ", hist.GetEntries())
    mean = hist.GetMean()
    std_dev = hist.GetStdDev()
    return hist, mean, std_dev

if __name__=='__main__':
    hist, mean, std_dev = lxy_gaussian(eraB_dict)
    print(mean, std_dev)

    gaussian = rt.TF1("gaussian", "gaus", -0.1, 0.1)
    gaussian.SetParameters(hist.GetMaximum(), mean, std_dev)
    hist.Fit(gaussian, "Q")

    y_max = hist.GetMaximum()

    canv = create_canvas('lxyerr', -0.1, 0.10, 'lxyerr', y_max)

    CMS.cmsDraw(gaussian, 'l')
    CMS.cmsDraw(hist, 'PE')

    CMS.SaveCanvas(canv, '/nfs/cms/rhebrero/work/analisis/vars_figs/lxyerr.png')
