import ROOT as rt
import cmsstyle as CMS
import numpy as np
from array import array
import pdb
from files_dicts import *
from files import * 
from functions import *
import argparse
from ABCD_Filters import ABCD_Filters
from GenSignalAnalisis import artif_signal
from ABCD_plot import ABCD_pred
from Canvas import create_sig_canvas


parser = argparse.ArgumentParser()
parser.add_argument('--mass', dest='mass', required=False, default='')
parser.add_argument('--d0sig_max', dest='d0sig_max', required=False, default=18)
parser.add_argument('--ptCut500', dest='ptCut500', required=False, default='55')
parser.add_argument('--ptCut100', dest='ptCut100', required=False, default='37.5')
parser.add_argument('--massCut500', dest='massCut500', required=False, default='60')
parser.add_argument('--massCut100', dest='massCut100', required=False, default='30')


args = parser.parse_args()

mass = args.mass
ptCut100 = args.ptCut100
ptCut500 = args.ptCut500
massCut100 = args.massCut100
massCut500 = args.massCut500
d0sig_max = float(args.d0sig_max)

filt = ABCD_Filters()
filt.add_cuts(filt.search_cuts())
filt.add_cuts(filt.more_cuts())

Data_dicts = [eraCDouble_dict, eraD_dict, eraE_dict, eraG_dict]#, eraC_dict]
data_lumi = 0
for data_dict in Data_dicts: data_lumi += data_dict['data_lumi'] 

if mass =='100': 
    Signal_dicts = SMuon_100_dicts_list
    filt.add_cuts(filt.Smuon100_cuts(ptCut100, massCut100))
if mass =='500': 
    Signal_dicts = SMuon_500_dicts_list
    filt.add_cuts(filt.Smuon500_cuts(ptCut500, massCut500))
filt.make_filters()

N_sig = []

N_bkg = ABCD_pred({}, 'd0sig', '', True, filt, Data_dicts, give_N_bkg=True, dataFull=True, lumi=str(data_lumi), save_plot=False, d0sig_max=d0sig_max) # d0sig_max=35 for new 100GeV restriction 
# N_bkg = 24.41025641025641 #For era B no cuts


# N_bkg = 2.935483870967742 # para 100 con cortes finales
# N_bkg = 0.5 # para 500 con cortes finales 

for dict in Signal_dicts:
    hist, N = artif_signal(dict, 50, 0, 500, var_name='d0sig', give_N_sig=True, data_lumi=data_lumi, extra_cond=mass, 
                           d0sig_max_100=d0sig_max, 
                           ptCut100=ptCut100, 
                           ptCut500=ptCut500,
                           massCut100=massCut100,
                           massCut500=massCut500)
    N_sig.append(N)
    print('Significance for ', dict['label'], ':', N/np.sqrt(N_bkg))
    del hist

Sigs = [Nsig / np.sqrt(N_bkg) for Nsig in N_sig]


# N_bkg_100 = 100 * N_bkg / data_lumi # 100fb-1 extrapolation
# N_sig_100 = [100 * Nsig / data_lumi for Nsig in N_sig]
# Sigs_100 = [Nsig / np.sqrt(N_bkg_100) for Nsig in N_sig_100]


lumis = {
    # str(round(data_lumi, 2)): data_lumi,
    '150 fb^{-1}': 100,
    '300 fb^{-1}':300,
    # '300 fb^{-1}, background \n improve':1050
}

def signal_significances_exclusions(Nsignal, Nbkg, mass, lumis=lumis):

    if mass == '100' : 
        ctau = [0.1, 1, 10, 100, 1000, 10000] # cm  
        min_tau=ctau[1]
        legend = rt.TLegend(0.65, 0.9, 0.9, 0.75)
        ptCut = ptCut100
        massCut = massCut100
    if mass == '500' : 
        ctau = [0.1, 1, 10, 100, 1000, 10000] # cm
        min_tau=ctau[1]
        legend = rt.TLegend(0.65, 0.9, 0.9, 0.75)
        ptCut = ptCut500
        massCut = massCut500

    legend = rt.TLegend(0.65, 0.9, 0.9, 0.75)
    legend.SetEntrySeparation(0.5)
    legend.SetTextSize(0.025)
    legend.SetBorderSize(0)

    grafs = {}
    splines = {}
    grafs_inter = {}
    y_max = 0
    y_min = 1
    for key, lumi in lumis.items():
        
        N_bkg = lumi * Nbkg / data_lumi
        N_sig = [lumi * Nsig / data_lumi for Nsig in Nsignal]
        sigs = [Nsig / np.sqrt(N_bkg) for Nsig in N_sig]

        grafs_inter[key] = rt.TGraph(len(ctau[2:-1]), array('d', ctau[2:-1]), array('d', sigs[2:-1]))
        splines[key] = rt.TSpline3("spline", grafs_inter[key])


        grafs[key] = rt.TGraph(len(ctau), array('d', ctau), array('d', sigs))

        legend.AddEntry(grafs[key], key, 'l')
        y_max = max(rt.TMath.MaxElement(grafs[key].GetN(), grafs[key].GetY()), y_max, 3)
        if min(rt.TMath.MinElement(grafs[key].GetN(), grafs[key].GetY()), y_min)!=0: y_min = min(rt.TMath.MinElement(grafs[key].GetN(), grafs[key].GetY()), y_min)

    
    # legend.SetTextAlign(22)
    # y_min = max(y_min, 1e-1)
    y_min = 1
    canv = create_sig_canvas(min_tau, ctau[-1], y_max, y_min, 'Significance', log=True)

    color = [rt.kBlue, rt.kRed, rt.kRed]
    for i, (key, graf) in enumerate(grafs.items()):
        if i==2: lstyle = 2
        else: lstyle = 1
        CMS.cmsDraw(graf, "PC", mcolor=color[i], lwidth=2, msize=0.5, marker=21, lstyle=lstyle)
        

    latex = rt.TLatex()
    latex.SetTextFont(42)
    latex.SetTextSize(0.042)
    latex.SetNDC()

    if mass== '100':
        ex_up_CMS =   rt.TGraph(2, array('d', [200,200]), array('d', [3, y_max*10]))
        CMS.cmsDraw(ex_up_CMS, 'C', mcolor=426, fstyle=3004, lwidth=1002, fcolor=426)
        
        latex.DrawLatex(0.22, 0.85, r"#bf{TMS-TMS}")
        latex.DrawLatex(0.21, 0.8, f"#bf{{m_{{#tilde{{#mu}}}} = {mass} GeV}}")

    if mass == '500':
        ex_up_CMS = rt.TGraph(2, array('d', [15,15]), array('d', [3, y_max*10]))
        ex_down_CMS = rt.TGraph(2, array('d', [0.1,0.1]), array('d', [3, y_max*10]))
        CMS.cmsDraw(ex_up_CMS, 'C', mcolor=426, fstyle=3005, lwidth=1002, fcolor=426)
        CMS.cmsDraw(ex_down_CMS, 'C', mcolor=426, fstyle=3004, lwidth=-1002, fcolor=426)

        latex.DrawLatex(0.66, 0.65, r"#bf{TMS-TMS}")
        latex.DrawLatex(0.65, 0.6, f"#bf{{m_{{#tilde{{#mu}}}} = {mass} GeV}}")



    sigMin = rt.TLine(min_tau, 3, ctau[-1], 3)
    CMS.cmsDrawLine(sigMin, lcolor=rt.kBlack, lwidth=2)

    legend.AddEntry(ex_up_CMS, "c#tau excluded by CMS", "f")


    legend.Draw()
    canv.Draw()

    CMS.SaveCanvas(canv, f'/nfs/cms/rhebrero/work/analisis/sigsigPlots/SigSigera{mass}BCDEG_{d0sig_max}_ptCut{ptCut}_massCut{massCut}.png')


signal_significances_exclusions(N_sig, N_bkg, mass)

