import ROOT as rt
import pdb
from map_ABCD_2D import hists_2d
import cmsstyle as CMS
import argparse
from array import array
from files_dicts import *
from array import array
from ABCD_Filters import ABCD_Filters
from preds import N_hists
# from files import *
# from functions import read_tree, Get_weight



parser = argparse.ArgumentParser()

# parser.add_argument('--d0sig_max', type=list, dest='d0sig_max', required=True)
parser.add_argument('--d0sig_min', type=float, dest='d0sig_min', required=True)

args = parser.parse_args()

# d0lims = args.d0sig_max
inf = args.d0sig_min

filt = ABCD_Filters()
filt.add_cuts(filt.search_cuts())
filt.add_cuts(filt.more_cuts())
filt.make_filters()

# filt.add_cuts(filt.SS_validation_cuts())
# filt.add_cuts(filt.more_cuts())
# filt.make_SS_filters()


# d0lims = [6+i for i in range(0, 16, 3)]
# d0lims = [6, 9, 12, 15, 18, 21]
d0lims = [21]
d0infs = [2, 4, 8, 12, 16]
# for inf in d0infs:
PD_over_PP = []
DD_over_PD = []

i=0
for infs in d0infs:
    for lim in d0lims:
        NA_tot, NB_tot, NC_tot, ND_tot = N_hists([eraB_dict], infs, lim, filt, Tfactor=False)


        if NC_tot != 0: PD_over_PP.append(NB_tot/NC_tot)
        else: PD_over_PP.append(-1)
        if ND_tot != 0: DD_over_PD.append(NA_tot/ND_tot)
        else: DD_over_PD.append(-1)

        print(f"PARA D0_MIN = {infs}, D0_MAX = {lim}")
        print(f"NA = {NA_tot}, NB = {NB_tot}, NC = {NC_tot}, ND = {ND_tot}")
        print(f"NA/ND = {DD_over_PD[i]} y NB/NC = {PD_over_PP[i]}")
        i+=1
    # for hist in hists_data: hist.Delete()


# pdb.set_trace()

# PD_over_PP = [1, 2, 4, 6, 10]
# DD_over_PD = [1, 2, 4, 6, 10]

graph = []
legend = CMS.cmsLeg(0.6, 0.2, 0.9, 0.55)

errors_x = array('d', [0])
errors_y = array('d', [0])

for j in range(len(d0infs)):
    y_values = array('d', [PD_over_PP[j]])
    x_values = array('d', [DD_over_PD[j]])
    graph.append(rt.TGraphErrors(1, x_values, y_values, errors_x, errors_y))

    graph[j].SetMarkerStyle(21 + j)
    graph[j].SetMarkerSize(1.4)  
    graph[j].SetMarkerColor(1+j)  
    try:
        # legend.AddEntry(graph[j], f'CRs: d_{{0,#sigma}} > {d0infs[j]}', 'p')
        legend.AddEntry(graph[j], f'd_{{0,#sigma}} > {d0infs[j]}', 'p')
    except IndexError:
        pdb.set_trace()

DiagLine = rt.TGraph(2, array("d", [0, 5]), array("d", [0, 5]))

CMS.SetExtraText("Private work")
CMS.SetLumi("0.11")
CMS.SetEnergy("13.6")

y_max = 1.2 * max(DD_over_PD)
x_max = 1.2 * max(PD_over_PP)

max_xy = max(y_max, x_max)

canv_name = 'N_progression_'
# Allow to reduce the size of the lumi info
# scaleLumi = 0.80 if square else None #???
canv = CMS.cmsCanvas(
    canv_name,
    0,
    5,
    0,
    5,
    "SR/CR",
    "TF",
    square=CMS.kSquare,
    extraSpace=0.01,
    iPos=0,
    
)
canv.SetGrid()

latex = rt.TLatex()
# latex.SetTextSize(0.5)
# latex.DrawLatex(0.3, 4, f"d_{{0,#sigma}} > {d0lims[0]}")
latex.DrawLatex(0.3, 4, f"SR > {d0lims[0]}")

for g in graph: g.Draw('P')
DiagLine.Draw('l')
legend.Draw()


CMS.SaveCanvas(canv, '/nfs/cms/rhebrero/work/analisis/ABCD_figs/' + 'IsoCut_' + canv_name + 'd0sig_min_' + f'{int(inf)}' + ".png")

