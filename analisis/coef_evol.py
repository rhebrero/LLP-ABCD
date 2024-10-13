import ROOT as rt
from array import array
import cmsstyle as CMS
import argparse


from functions import *
from files import *
from files_dicts import *
from ABCD_plot import B_hist, C_hist, D_hist, A_hist, get_bining
from ABCD_Filters import ABCD_Filters
from Canvas import create_canvas
from preds import N_hists
from Canvas import Canvas_Class

# Hacer una clase canvas universal para cosasa asi 

parser = argparse.ArgumentParser()
parser.add_argument('--var', dest = 'var', default='invMass', required = False)

args = parser.parse_args()

variable = args.var

# inmass = 0
# endmass = 150
# nmass = 30

nbin, inbin, endbin = get_bining(variable)

PD_over_PP = []
DD_over_PD = []

PD_over_PP_err = []
DD_over_PD_err = []

m = []

filt = ABCD_Filters()
filt.add_cuts(filt.search_cuts())
filt.make_filters()

Data_dict = [eraB_dict, eraCDouble_dict, eraD_dict, eraE_dict, eraG_dict]

A,B,C,D = N_hists(Data_dict, 4, 18, filt, Tfactor=False)
print('SEGUN N_hist:', A, B, C, D)

# full_hist_A = A_hist([eraB_dict], variable, filt, 4, 18)
full_hist_B = B_hist(Data_dict, variable, filt, 4, 18)
full_hist_C = C_hist(Data_dict, variable, filt, 4, 18)
# full_hist_D = D_hist([eraB_dict], variable, filt, 4, 18)



for i in range(nbin-1):

    NA = full_hist_A.Integral(i, i+1)
    NB = full_hist_B.Integral(i, i+1)
    NC = full_hist_C.Integral(i, i+1)
    ND = full_hist_D.Integral(i, i+1)

    if NC!= 0 and NB!= 0:
        NB_over_NC = NB/NC
        NB_over_NC_err = NB/NC*((NB**0.5 / NB)**2 + (NC**0.5 / NC)**2)**0.5

    else: 
        NB_over_NC = 0
        NB_over_NC_err = 0

    if ND!=0 and NA!= 0: 
        NA_over_ND = NA/ND
        NA_over_ND_err = NA/ND*((NA**0.5 / NA)**2 + (ND**0.5 / ND)**2)**0.5
    else: 
        NA_over_ND = 0
        NA_over_ND_err = 0


    print(NA_over_ND, NB_over_NC) #, NB_over_NC_data)

    m.append(float(inbin + (endbin - inbin) / nbin * i))

    PD_over_PP.append(NB_over_NC)
    DD_over_PD.append(NA_over_ND)

    PD_over_PP_err.append(NB_over_NC_err)
    DD_over_PD_err.append(NA_over_ND_err)


print(m)

graf_PD_over_PP = rt.TGraphErrors(len(m), array("d", m), array("d", PD_over_PP), array("d", [0] * len(m)), array("d", PD_over_PP_err))
graf_DD_over_PD = rt.TGraphErrors(len(m), array("d", m), array("d", DD_over_PD), array("d", [0] * len(m)), array("d", DD_over_PD_err))


colors = [rt.kRed, rt.kGreen, rt.kBlue, rt.kViolet, rt.kCyan, rt.kCyan] # meter generador de colores 

canv_name = f'TF_Evol_{variable}'

y_max = 1.2
Canvas = Canvas_Class(lumi=GetLumi(Data_dict))
canv = Canvas.create_canvas(variable, inbin, endbin, 'TF_Evol', y_max, False, ylabel='TF')

leg = CMS.cmsLeg(0.55, 0.89 - 0.04 * 4, 0.89, 0.89, textSize=0.04)


CMS.cmsDraw(graf_PD_over_PP, "PE", mcolor=rt.kBlack)


CMS.SaveCanvas(canv, f"/nfs/cms/rhebrero/work/analisis/{canv_name}.png")
