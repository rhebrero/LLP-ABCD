import ROOT as rt
import pdb
import sys
import os
from files import *
from files_dicts import *
import cmsstyle as CMS
from functions import read_tree, Get_weight
import argparse
from ABCD_Filters import ABCD_Filters

curr_dir = os.path.dirname(os.path.abspath(__file__)) # Currently doing it like this, will need to add it to env var once it's organized
conf_dir = os.path.join(curr_dir, '..', 'config/')
conf_dir = os.path.normpath(conf_dir)
sys.path.append(conf_dir)
from config_test import *


# parser = argparse.ArgumentParser()
# parser.add_argument('--do', dest='todo', required=True)
# parser.add_argument('--dicts', dest='dicts', default=eraB_dict, required=False)

# args = parser.parse_args()


fig_name='ABCD_2D_eraB_4NA'
square = CMS.kSquare
iPos=0
dict_eraB = get_dict('data', 'data_eraB')
norm = False

# d0sig_max = 15
# d0sig_min = 1

        
inbin = 0
endbin = 32 #2 * d0sig_max
nbin = 24 #endbin # * 2

# filt = ABCD_Filters()
# filt.add_cuts(filt.SS_validation_cuts())
# filt.make_SS_filters()



def hists_2d(dicts, inbin, endbin, nbin, d0sig_min, d0sig_max, filt, verbose=False):


    full_hist2d_A_m_6to10 = rt.TH2F("full_hist2d_A_m_6to10", "d0 sig", nbin, inbin, endbin, nbin, inbin, endbin)
    full_hist2d_A_p_6to10 = rt.TH2F("full_hist2d_A_p_6to10", "d0 sig", nbin, inbin, endbin, nbin, inbin, endbin)

    full_hist2d_A_m_10to = rt.TH2F("full_hist2d_A_m_10to", "d0 sig", nbin, inbin, endbin, nbin, inbin, endbin)
    full_hist2d_A_p_10to = rt.TH2F("full_hist2d_A_p_10to", "d0 sig", nbin, inbin, endbin, nbin, inbin, endbin)

    full_hist2d_A_B = rt.TH2F("full_hist2d_A_B", "d0 sig", nbin, inbin, endbin, nbin, inbin, endbin)
    full_hist2d_A_D = rt.TH2F("full_hist2d_A_D", "d0 sig", nbin, inbin, endbin, nbin, inbin, endbin)

    full_hist2d_B_p = rt.TH2F("full_hist2d_B_p", "d0 sig",     nbin, inbin, endbin, nbin, inbin, endbin)
    full_hist2d_B_m = rt.TH2F("full_hist2d_B_m", "d0 sig",     nbin, inbin, endbin, nbin, inbin, endbin)

    full_hist2d_D_p = rt.TH2F("full_hist2d_D_p", "d0 sig",     nbin, inbin, endbin, nbin, inbin, endbin)
    full_hist2d_D_m = rt.TH2F("full_hist2d_D_m", "d0 sig",     nbin, inbin, endbin, nbin, inbin, endbin)

    full_hist2d_C_m = rt.TH2F("full_hist2d_C_m", "d0 sig", nbin, inbin, endbin, nbin, inbin, endbin)
    full_hist2d_C_p = rt.TH2F("full_hist2d_C_p", "d0 sig", nbin, inbin, endbin, nbin, inbin, endbin)

    full_hist2d_D2D2_m = rt.TH2F("full_hist2d_D2D2_m", "d0 sig", nbin, inbin, endbin, nbin, inbin, endbin)
    full_hist2d_D2D2_p = rt.TH2F("full_hist2d_D2D2_p", "d0 sig", nbin, inbin, endbin, nbin, inbin, endbin)

    full_hist2d_D2D6_B_p = rt.TH2F("full_hist2d_D2D6_B_p", "d0 sig",     nbin, inbin, endbin, nbin, inbin, endbin)
    full_hist2d_D2D6_D_p = rt.TH2F("full_hist2d_D2D6_D_p", "d0 sig",     nbin, inbin, endbin, nbin, inbin, endbin)

    full_hist2d_D2D6_B_m = rt.TH2F("full_hist2d_D2D6_B_m", "d0 sig",     nbin, inbin, endbin, nbin, inbin, endbin)
    full_hist2d_D2D6_D_m = rt.TH2F("full_hist2d_D2D6_D_m", "d0 sig",     nbin, inbin, endbin, nbin, inbin, endbin)

    full_hist2d_PD2_B = rt.TH2F("full_hist2d_PD2_B", "d0 sig",     nbin, inbin, endbin, nbin, inbin, endbin)
    full_hist2d_PD2_D = rt.TH2F("full_hist2d_PD2_D", "d0 sig",     nbin, inbin, endbin, nbin, inbin, endbin)



    if not isinstance(dicts, list): dicts = [dicts]
    for dict in dicts:

        f, tree = read_tree(dict['file'])
        if 'friend' in dict: tree.AddFriend('SimpleNTupler/DDTree', dict['friend'])
        if 'x_sec' in dict: w = Get_weight(dict['x_sec'], dict['events'], lumi_DoubleMuonRun2022B)
        else: w = 1

        hist2d_A_m_6to10 = rt.TH2F("hist2d_A_m_6to10", "d0 sig",nbin, inbin, endbin, nbin, inbin, endbin)
        tree.Draw("patmu_d0sig_pv[dimD6D6_mu1_idx]:patmu_d0sig_pv[dimD6D6_mu2_idx] >> hist2d_A_m_6to10", filt.filters_D6D6_under_limit_C_negmu1.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")

        hist2d_A_p_6to10 = rt.TH2F("hist2d_A_p_6to10", "d0 sig",nbin, inbin, endbin, nbin, inbin, endbin)
        tree.Draw("patmu_d0sig_pv[dimD6D6_mu2_idx]:patmu_d0sig_pv[dimD6D6_mu1_idx] >> hist2d_A_p_6to10", filt.filters_D6D6_under_limit_C_posmu1.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")

        hist2d_A_m_10to = rt.TH2F("hist2d_A_m_10to", "d0 sig",nbin, inbin, endbin, nbin, inbin, endbin)
        tree.Draw("patmu_d0sig_pv[dimD6D6_mu1_idx]:patmu_d0sig_pv[dimD6D6_mu2_idx] >> hist2d_A_m_10to", filt.filters_D6D6_over_limit_negmu1.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")

        hist2d_A_p_10to = rt.TH2F("hist2d_A_p_10to", "d0 sig",nbin, inbin, endbin, nbin, inbin, endbin)
        tree.Draw("patmu_d0sig_pv[dimD6D6_mu2_idx]:patmu_d0sig_pv[dimD6D6_mu1_idx] >> hist2d_A_p_10to", filt.filters_D6D6_over_limit_posmu1.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")

        hist2d_A_B = rt.TH2F("hist2d_A_B", "d0 sig",nbin, inbin, endbin, nbin, inbin, endbin)
        tree.Draw("patmu_d0sig_pv[dimD6D6_mu1_idx]:patmu_d0sig_pv[dimD6D6_mu2_idx] >> hist2d_A_B", filt.filters_D6D6_under_limit_B.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")

        hist2d_A_D = rt.TH2F("hist2d_A_D", "d0 sig",nbin, inbin, endbin, nbin, inbin, endbin)
        tree.Draw("patmu_d0sig_pv[dimD6D6_mu2_idx]:patmu_d0sig_pv[dimD6D6_mu1_idx] >> hist2d_A_D", filt.filters_D6D6_under_limit_D.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")


        hist2d_B_p = rt.TH2F("hist2d_B_p", "d0 sig",nbin, inbin, endbin, nbin, inbin, endbin)
        tree.Draw("patmu_d0sig_pv[dimD6D6_mu1_idx]:patmu_d0sig_pv[dimPP_mu1_idx] >> hist2d_B_p", filt.filters_PD6_over_limit_B.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")

        hist2d_B_m = rt.TH2F("hist2d_B_m", "d0 sig",nbin, inbin, endbin, nbin, inbin, endbin)
        tree.Draw("patmu_d0sig_pv[dimD6D6_mu1_idx]:patmu_d0sig_pv[dimPP_mu1_idx] >> hist2d_B_m", filt.filters_PD6_under_limit_B_C.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")



        hist2d_C_m = rt.TH2F("hist2d_C_m", "d0 sig",nbin, inbin, endbin, nbin, inbin, endbin)
        tree.Draw("patmu_d0sig_pv[dimPP_mu1_idx]:patmu_d0sig_pv[dimPP_mu2_idx] >> hist2d_C_m", filt.filters_PP_negmu1.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")

        hist2d_C_p = rt.TH2F("hist2d_C_p", "d0 sig",nbin, inbin, endbin, nbin, inbin, endbin)
        tree.Draw("patmu_d0sig_pv[dimPP_mu2_idx]:patmu_d0sig_pv[dimPP_mu1_idx] >> hist2d_C_p", filt.filters_PP_posmu1.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")



        hist2d_D_p = rt.TH2F("hist2d_D_p", "d0 sig",nbin, inbin, endbin, nbin, inbin, endbin)
        tree.Draw("patmu_d0sig_pv[dimPP_mu1_idx]:patmu_d0sig_pv[dimD6D6_mu1_idx] >> hist2d_D_p", filt.filters_PD6_over_limit_D.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")
        hist2d_D_m = rt.TH2F("hist2d_D_m", "d0 sig",nbin, inbin, endbin, nbin, inbin, endbin)
        tree.Draw("patmu_d0sig_pv[dimPP_mu1_idx]:patmu_d0sig_pv[dimD6D6_mu1_idx] >> hist2d_D_m", filt.filters_PD6_under_limit_D_C.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")


        hist2d_D2D2_m = rt.TH2F("hist2d_D2D2_m", "d0 sig", nbin, inbin, endbin, nbin, inbin, endbin)
        tree.Draw("patmu_d0sig_pv[dimD2D2_mu1_idx]:patmu_d0sig_pv[dimD2D2_mu2_idx] >> hist2d_D2D2_m", filt.filters_D2D2_C_negmu1.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")
        hist2d_D2D2_p = rt.TH2F("hist2d_D2D2_p", "d0 sig", nbin, inbin, endbin, nbin, inbin, endbin)
        tree.Draw("patmu_d0sig_pv[dimD2D2_mu2_idx]:patmu_d0sig_pv[dimD2D2_mu1_idx] >> hist2d_D2D2_p", filt.filters_D2D2_C_posmu1.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")


        hist2d_D2D6_D_p = rt.TH2F("hist2d_D2D6_D_p", "d0 sig",nbin, inbin, endbin, nbin, inbin, endbin)
        tree.Draw("patmu_d0sig_pv[dimD2D2_mu1_idx]:patmu_d0sig_pv[dimD6D6_mu1_idx] >> hist2d_D2D6_D_p", filt.filters_D2D6_over_limit_D.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")
        hist2d_D2D6_B_p = rt.TH2F("hist2d_D2D6_B_p", "d0 sig",nbin, inbin, endbin, nbin, inbin, endbin)
        tree.Draw("patmu_d0sig_pv[dimD6D6_mu1_idx]:patmu_d0sig_pv[dimD2D2_mu1_idx] >> hist2d_D2D6_B_p", filt.filters_D2D6_over_limit_B.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")


        hist2d_D2D6_D_m = rt.TH2F("hist2d_D2D6_D_m", "d0 sig",nbin, inbin, endbin, nbin, inbin, endbin)
        tree.Draw("patmu_d0sig_pv[dimD2D2_mu1_idx]:patmu_d0sig_pv[dimD6D6_mu1_idx] >> hist2d_D2D6_D_m", filt.filters_D2D6_under_limit_D_C.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")
        hist2d_D2D6_B_m = rt.TH2F("hist2d_D2D6_B_m", "d0 sig",nbin, inbin, endbin, nbin, inbin, endbin)
        tree.Draw("patmu_d0sig_pv[dimD6D6_mu1_idx]:patmu_d0sig_pv[dimD2D2_mu1_idx] >> hist2d_D2D6_B_m", filt.filters_D2D6_under_limit_B_C.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")


        hist2d_PD2_D = rt.TH2F("hist2d_PD2_D", "d0 sig",nbin, inbin, endbin, nbin, inbin, endbin)
        tree.Draw("patmu_d0sig_pv[dimD2D2_mu1_idx]:patmu_d0sig_pv[dimPP_mu1_idx] >> hist2d_PD2_D", filt.filters_PD2_D_C.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")

        hist2d_PD2_B = rt.TH2F("hist2d_PD2_B", "d0 sig",nbin, inbin, endbin, nbin, inbin, endbin)
        tree.Draw("patmu_d0sig_pv[dimPP_mu1_idx]:patmu_d0sig_pv[dimD2D2_mu1_idx] >> hist2d_PD2_B", filt.filters_PD2_B_C.format(signal_limit = d0sig_max, signal_inf = d0sig_min), "goff")

        hist2d_A_m_6to10.Scale(w)
        hist2d_A_p_6to10.Scale(w)
        hist2d_A_m_10to.Scale(w)
        hist2d_A_p_10to.Scale(w)
        hist2d_A_B.Scale(w)
        hist2d_A_D.Scale(w)

        hist2d_B_m.Scale(w)
        hist2d_B_m.Scale(w)

        hist2d_C_m.Scale(w)
        hist2d_C_p.Scale(w)

        hist2d_D_m.Scale(w)
        hist2d_D_p.Scale(w)

        hist2d_D2D2_m.Scale(w)
        hist2d_D2D2_p.Scale(w)

        hist2d_D2D6_B_p.Scale(w)
        hist2d_D2D6_D_p.Scale(w)

        hist2d_D2D6_B_m.Scale(w)
        hist2d_D2D6_D_m.Scale(w)

        hist2d_PD2_B.Scale(w)
        hist2d_PD2_D.Scale(w)

        full_hist2d_A_m_6to10.Add(hist2d_A_m_6to10)
        full_hist2d_A_p_6to10.Add(hist2d_A_p_6to10)
        full_hist2d_A_m_10to.Add(hist2d_A_m_10to)
        full_hist2d_A_p_10to.Add(hist2d_A_p_10to)
        full_hist2d_A_B.Add(hist2d_A_B)
        full_hist2d_A_D.Add(hist2d_A_D)

        full_hist2d_B_m.Add(hist2d_B_m)
        full_hist2d_B_p.Add(hist2d_B_p)

        full_hist2d_C_m.Add(hist2d_C_m)
        full_hist2d_C_p.Add(hist2d_C_p)

        full_hist2d_D_p.Add(hist2d_D_p)
        full_hist2d_D_m.Add(hist2d_D_m)

        full_hist2d_D2D2_p.Add(hist2d_D2D2_p)
        full_hist2d_D2D2_m.Add(hist2d_D2D2_m)

        full_hist2d_D2D6_B_p.Add(hist2d_D2D6_B_p)
        full_hist2d_D2D6_D_p.Add(hist2d_D2D6_D_p)
        
        full_hist2d_D2D6_B_m.Add(hist2d_D2D6_B_m)
        full_hist2d_D2D6_D_m.Add(hist2d_D2D6_D_m)

        full_hist2d_PD2_B.Add(hist2d_PD2_B)
        full_hist2d_PD2_D.Add(hist2d_PD2_D)

        if verbose: print(f"Peso para {dict['file']} es {w}")

    # pdb.set_trace()

    NAA = full_hist2d_A_m_10to. GetEntries() + full_hist2d_A_p_10to.GetEntries()
    NAB = full_hist2d_A_B.GetEntries()
    NAD = full_hist2d_A_D.GetEntries()
    NAC = full_hist2d_A_m_6to10.GetEntries() + full_hist2d_A_p_6to10.GetEntries()


    NB_m = full_hist2d_B_m.  GetEntries()
    NB_p = full_hist2d_B_p.  GetEntries()
    NC = full_hist2d_C_m.Integral() + full_hist2d_C_p.Integral()
    ND_m = full_hist2d_D_m.  GetEntries()
    ND_p = full_hist2d_D_p.  GetEntries()


    ND2D2 = full_hist2d_D2D2_p.GetEntries() + full_hist2d_D2D2_m.GetEntries()
    ND2D6_B_m = full_hist2d_D2D6_B_m.GetEntries()
    ND2D6_D_m = full_hist2d_D2D6_D_m.GetEntries()
    ND2D6_B_p = full_hist2d_D2D6_B_p.GetEntries()
    ND2D6_D_p = full_hist2d_D2D6_D_p.GetEntries()

    NPD2_B = full_hist2d_PD2_B.GetEntries()
    NPD2_D = full_hist2d_PD2_D.GetEntries()



    NA_tot = NAA
    NB_tot = ND2D6_B_p + NB_p + NAB
    ND_tot = ND2D6_D_p + ND_p + NAD
    NC_tot = NAC + NC + ND2D2 + NPD2_D + NPD2_B + ND2D6_D_m + ND2D6_B_m + ND_m + NB_m

    hists = [        
        full_hist2d_A_m_10to ,
        full_hist2d_A_p_10to ,
        full_hist2d_A_m_6to10,
        full_hist2d_A_p_6to10,
        full_hist2d_A_B      ,
        full_hist2d_A_D      ,
        full_hist2d_B_m      ,
        full_hist2d_B_p      ,
        full_hist2d_C_m      ,
        full_hist2d_C_p      ,
        full_hist2d_D_p      ,
        full_hist2d_D_m      ,
        full_hist2d_D2D2_p   ,
        full_hist2d_D2D2_m   ,
        full_hist2d_D2D6_B_p ,
        full_hist2d_D2D6_D_p ,
        full_hist2d_D2D6_B_m ,
        full_hist2d_D2D6_D_m ,
        full_hist2d_PD2_B    ,
        full_hist2d_PD2_D    ,
    ]


    return hists, NA_tot, NB_tot, NC_tot, ND_tot

if __name__ == "__main__":
    d0sig_max = 18
    d0sig_min = 10
    canv_name = f'ABCD_2Dmap_{d0sig_min}_{d0sig_max}'

    filt = ABCD_Filters()
    filt.add_cuts(filt.search_cuts())
    filt.add_cuts(filt.more_cuts())
    filt.make_filters()
    canv_name += '_IsoCut_B' 

    # FOR ERA B 2D MAP
    hists, NA_tot, NB_tot, NC_tot, ND_tot = hists_2d(eraB_dict, inbin, endbin, nbin, d0sig_min, d0sig_max, filt)

    # FOR BKG SIMS 2D MAPS
    # all_bkg_dicts = []
    # for kind in ['QCD', 'DYto2Tau', 'DYto2Mu200k']:
    #     all_bkg_dicts.extend(get_dict('background', kind, all=True))
    # hists,  NA_tot, NB_tot, NC_tot, ND_tot = hists_2d(all_bkg_dicts, inbin, endbin, nbin, d0sig_min, d0sig_min, verbose=True)

    CMS.SetExtraText("Private work")
    CMS.SetLumi("0.11")
    CMS.SetEnergy("13.6")

    # Allow to reduce the size of the lumi info
    scaleLumi = 0.80 if square else None #???
    canv = CMS.cmsCanvas(
        canv_name,
        inbin,
        endbin,
        inbin,
        endbin,
        "d_{0,#sigma}(#mu^{+})", # el tamaño de la etiqueta parece que esta definido fijo en el paquete cmsstyle, lo hace con el drawframe del canvas y no puedo ni llamarlo
        "d_{0,#sigma}(#mu^{-})",
        square=square,
        extraSpace=0.03,
        iPos=iPos,
        with_z_axis=True,
        # scaleLumi=scaleLumi, #???
        # scaleLumi=
    )

    # canv.SetLogz(True)


    hists[0].GetZaxis().SetTitle("Events")
    hists[0].GetZaxis().SetTitleOffset(1.2)
    hists[0].GetXaxis().SetTitleOffset(1.2)
    hists[0].GetXaxis().SetTitleSize(0.5)
    hists[0].GetXaxis().SetTitleSize(0.5)

    hists[0].SetMaximum(17)
    # hist2d_A_m_10to.SetMinimum(0)

    for hist in hists: hist.Draw("same colz")


    line1 = rt.TLine(0, d0sig_max, endbin, d0sig_max)
    line2 = rt.TLine(d0sig_max, 0, d0sig_max, endbin)
    line1.SetLineColor(rt.kBlack)
    line2.SetLineColor(rt.kBlack)
    line1.Draw()
    line2.Draw()

    latex = rt.TLatex()
    latex.SetTextFont(42)  # Puedes ajustar la fuente del texto si lo deseas
    latex.SetTextSize(0.065)  # Puedes ajustar el tamaño del texto si lo deseas
    # Añadir texto al histograma





    # latex.DrawLatex(d0sig_max*5/4, d0sig_max*6/4, f"N = {NA_tot}")
    # latex.DrawLatex(d0sig_max/2 - 2, d0sig_max/2, f"N = {NC_tot}")
    # latex.DrawLatex(d0sig_max*5/4, d0sig_max/2, f"N = {ND_tot}")
    # latex.DrawLatex(d0sig_max/4, d0sig_max*6/4, f"N = {NB_tot}")

    latex.DrawLatex(15, 15, "SR")
    # latex.DrawLatex(d0sig_max*5/4, d0sig_max*6/4, "SR")
    latex.SetTextSize(0.055)
    latex.DrawLatex(d0sig_max/2 - 2, d0sig_max/2, "CR_{C}")
    latex.DrawLatex(d0sig_max*5/4, d0sig_max/2, "CR_{D}")
    latex.DrawLatex(d0sig_max/2 - 2, d0sig_max*6/4, "CR_{B}")


    print(f"NA = {NA_tot}, NB = {NB_tot}, NC = {NC_tot}, ND = {ND_tot}")
    print(f"NA/ND = {NA_tot/ND_tot} y NB/NC = {NB_tot/NC_tot}")



    CMS.SaveCanvas(canv, '/nfs/cms/rhebrero/work/analisis/ABCD_figs/' + canv_name + ".png")





