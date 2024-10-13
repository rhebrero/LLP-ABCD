#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# Example script to create 1-D plots of cross sections as function of mass from data in JSON format.
# 
# External requirements (Python modules):
# 
#   pandas (https://pandas.pydata.org/)
#   matplotlib (https://matplotlib.org/)
# 
# Run with:
# 
#   python plot_xsecs_from_json.py
# 
# (85) 
#
# $Id: plot_xsecs_from_json.py 3190 2019-05-28 17:21:31Z eis $

### imports
import os
import json
import argparse

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker #needed to configure the y-axis ticks

parser = argparse.ArgumentParser(description="produce SUSY cross section plots in various configurations.")
parser.add_argument('--xsec'    , dest='XSEC'    , default=True,  help='plot xsections (default mode)')
parser.add_argument('--lumi'    , dest='LUMI'    , default=-1,  help='compute the number of expected events given a luminiosity')
parser.add_argument('--gluino'  , dest='GLUINO'  , default = False,  action = 'store_true', help='plot all gg and gq')
parser.add_argument('--squark'  , dest='SQUARK'  , default = False,  action = 'store_true', help='plot squrks')
parser.add_argument('--slepton' , dest='SLEPTON' , default = False,  action = 'store_true', help='plot sleptons')
parser.add_argument('--stau'    , dest='STAU'    , default = False,  action = 'store_true', help='plot staus')
parser.add_argument('--xmin'    , dest='XMIN'    , default = 100,  help='x_axis minimum range')
parser.add_argument('--xmax'    , dest='XMAX'    , default = 3000,  help='x_axis minimum range')
parser.add_argument('--sqrt'    , dest='SQRT'    , default = 13.6,  required= True, help='centre of mass energy (13 TeV or 13.6 TeV)')
parser.add_argument('--debug'   , dest='DEBUG'   , default = False,  action = 'store_true', help='for squark plot add the xsecs from AN-23-050')
parser.add_argument('--limits'  , dest='LIMITS'  , default = False,  action = 'store_true', help='add vertical lines for current best high mass limits')

args = parser.parse_args()

sqrt = float(args.SQRT)
if sqrt not in [13, 13.6]:
  print ("ERROR: sqrt must be 13 or 13.6")
  exit()

# available json files (and models)
filenames_13 = [
  "pp13_gluino_NNLO+NNLL.json",
  "pp13_gluinosquark_NNLO+NNLL.json",
  "pp13_squark_NNLO+NNLL.json",
  "pp13_stopsbottom_NNLO+NNLL.json",
  ##
  "pp13_hino_NLO+NLL.json",
  "pp13_wino_C1C1_NLO+NLL.json",
  "pp13_winom_C1N2_NLO+NLL.json",
  "pp13_winop_C1N2_NLO+NLL.json",
  "pp13_winopm_C1N2_NLO+NLL.json",
  ##
  "pp13_slep_L_NLO+NLL_PDF4LHC.json",
  "pp13_slep_R_NLO+NLL_PDF4LHC.json",
  "pp13_snu-snu_NLO+NLL_PDF4LHC.json",
  "pp13_snuM-slep_NLO+NLL_PDF4LHC.json",
  "pp13_snuP-slep_NLO+NLL_PDF4LHC.json",
  "pp13_stau_L_NLO+NLL_PDF4LHC.json",
  "pp13_stau_R_NLO+NLL_PDF4LHC.json",
  "pp13_stau_LR_NLO+NLL_PDF4LHC.json",
  ## JSON files with 2 mas parameters cannot be plotted yet
  #"pp13_hinosplit_C1C1_NLO+NLL.json",
]
# define datasets (NOTE: files that are commented out do exist and can be used)
filenames_13600 = [
    ## 13.6 TeV
    #"pp13600_SGmodel_GGxsec_NNLOa+NNLL.json",
    ##"pp13600_SGmodel_SGincxsec_NNLOa+NNLL.json", # JSON files with 2 mass parameters cannot be plotted yet
    #"pp13600_SGmodel_SGxsec_NNLOa+NNLL.json",
    #"pp13600_SGmodel_SSxsec_NNLOa+NNLL.json",
    #"pp13600_SGmodel_STxsec_NNLOa+NNLL.json",
    "pp13600_gluino_NNLO+NNLL.json",
    "pp13600_gluinosquark_NNLO+NNLL.json",
    "pp13600_squark_NNLO+NNLL.json",
    "pp13600_stopsbottom_NNLO+NNLL.json",
    ##
    "pp13600_hino_deg_1000022_-1000024_NNLL.json",
    "pp13600_hino_deg_1000022_1000023_NNLL.json",
    "pp13600_hino_deg_1000022_1000024_NNLL.json",
    "pp13600_hino_deg_1000024_-1000024_NNLL.json",
    #"pp13600_hino_nondeg_1000022_1000023_NNLL.json", # JSON files with 2 mass parameters cannot be plotted yet
    #"pp13600_hino_nondeg_1000023_-1000024_NNLL.json", # JSON files with 2 mass parameters cannot be plotted yet
    #"pp13600_hino_nondeg_1000023_1000024_NNLL.json", # JSON files with 2 mass parameters cannot be plotted yet
    #"pp13600_hino_nondeg_1000024_-1000024_NNLL.json", # JSON files with 2 mass parameters cannot be plotted yet
    "pp13600_sleptons_1000011_-1000011_NNLL.json",
    "pp13600_sleptons_1000015_-1000015_NNLL.json",
    "pp13600_sleptons_2000011_-2000011_NNLL.json",
    "pp13600_wino_1000023_-1000024_NNLL.json",
    "pp13600_wino_1000023_1000024_NNLL.json",
    "pp13600_wino_1000024_-1000024_NNLL.json",
    #"pp13600_wino_sq_dep_1000023_-1000024_NNLL.json", # JSON files with 2 mass parameters cannot be plotted yet
    #"pp13600_wino_sq_dep_1000023_1000024_NNLL.json", # JSON files with 2 mass parameters cannot be plotted yet
    #"pp13600_wino_sq_dep_1000024_-1000024_NNLL.json", # JSON files with 2 mass parameters cannot be plotted yet
    ]

if sqrt == 13:
  filenames = filenames_13
if sqrt == 13.6:
  filenames = filenames_13600

if args.GLUINO == True:
  if sqrt == 13:   filenames = ["pp13_gluino_NNLO+NNLL.json", "pp13_gluinosquark_NNLO+NNLL.json"]
  if sqrt == 13.6: filenames = ["pp13600_gluino_NNLO+NNLL.json", "pp13600_gluinosquark_NNLO+NNLL.json"]

if args.SQUARK == True:
  if sqrt == 13:   filenames = ["pp13_squark_NNLO+NNLL.json", "pp13_stopsbottom_NNLO+NNLL.json"]
  if sqrt == 13.6: filenames = ["pp13600_squark_NNLO+NNLL.json", "pp13600_stopsbottom_NNLO+NNLL.json"]

if args.SLEPTON == True:
  if sqrt == 13: filenames = ["pp13_slep_L_NLO+NLL_PDF4LHC.json", "pp13_slep_R_NLO+NLL_PDF4LHC.json", "pp13_stau_L_NLO+NLL_PDF4LHC.json", "pp13_stau_R_NLO+NLL_PDF4LHC.json"]
  if sqrt == 13.6: filenames = ["pp13600_sleptons_1000011_-1000011_NNLL.json", "pp13600_sleptons_1000015_-1000015_NNLL.json", "pp13600_sleptons_2000011_-2000011_NNLL.json"]

if args.STAU == True:
  if sqrt == 13: filenames = ["pp13_stau_L_NLO+NLL_PDF4LHC.json", "pp13_stau_R_NLO+NLL_PDF4LHC.json", "pp13_stau_LR_NLO+NLL_PDF4LHC.json"]
  if sqrt == 13.6: filenames = ["pp13600_sleptons_2000011_-2000011_NNLL.json"]

#https://arxiv.org/pdf/2111.06296.pdf
### helpers
def PlotEvents(df, label, lumi, filename):
  plt.yscale("log")
  scale = 1000*lumi
  baseline = plt.plot(df.mass_GeV, df.xsec_pb*scale, label = label)
  # check which uncertainty type we have
  if "unc_up_pb" in df.columns:
    # asymmetric
    band = plt.fill_between(df.mass_GeV, (df.xsec_pb + df.unc_down_pb)*scale, (df.xsec_pb + df.unc_up_pb)*scale, alpha = 0.2, facecolor = baseline[0].get_color(), linewidth=0)
  else:
    # assume symmetric always present
    band = plt.fill_between(df.mass_GeV, (df.xsec_pb - df.unc_pb)*scale     , (df.xsec_pb + df.unc_pb)*scale   , alpha = 0.2, facecolor = baseline[0].get_color(), linewidth=0)

    if filename == "pp13_winopm_C1N2_NLO+NLL.json":
      Br = 0.04279
      print (label)
      baseline = plt.plot(df.mass_GeV, df.xsec_pb*scale*Br, label = "$\sigma(\\tilde\chi_1^\pm\\tilde\chi_2^0)$ $B(\\tilde\chi_2^0 \\to \mu \mu \\tilde\chi_1^0)$")
    
def PlotXsec(df, label):
  plt.yscale("log")
  baseline = plt.plot(df.mass_GeV, df.xsec_pb, label = label)  
  # check which uncertainty type we have
  if "unc_up_pb" in df.columns:
    # asymmetric
    band = plt.fill_between(df.mass_GeV, df.xsec_pb + df.unc_down_pb, df.xsec_pb + df.unc_up_pb, alpha = 0.2, facecolor = baseline[0].get_color(), linewidth=0)
  else:
    # assume symmetric always present
    band = plt.fill_between(df.mass_GeV, df.xsec_pb - df.unc_pb     , df.xsec_pb + df.unc_pb   , alpha = 0.2, facecolor = baseline[0].get_color(), linewidth=0)

  
### main

# init plotting
plt.ion()
use_latex = False
if use_latex:
  plt.rc('text', usetex=True)
  plt.rc('font', size=18)
  plt.rc('legend', fontsize=14)
  plt.rc('text.latex', preamble=r'\usepackage{cmbright}')
else:
  plt.rcParams.update({'font.size': 10})

# load data and plot
dfs = {}
for idx, filename in enumerate(filenames):
  print(filename)
  data = json.load(open(os.path.join("json", filename)))
  df   = pd.DataFrame.from_dict(data["data"], orient = "index")
  # restore mass as column and sort 
  df["mass_GeV"] = df.index.astype(int)
  df = df.sort_values("mass_GeV")
  df.reset_index(inplace = True, drop = True)
  # plot
  if int(args.LUMI) < 0:  
    PlotXsec(df, data["process_latex"])
  else:
    PlotEvents(df, data["process_latex"], int(args.LUMI), filename)
  # 
  dfs[filename] = df

# draw legend and style plot
plt.xlabel("particle mass [GeV]")
if int(args.LUMI) < 0:  
  plt.ylabel("cross section [pb]")
else:
  plt.ylabel("$N_{events}$")

# increase the number of grid lines
plt.grid(True, which='both', linestyle='--', linewidth=0.4, alpha=0.6)

plt.xlim(float(args.XMIN), float(args.XMAX))
if int(args.LUMI) < 0: 
  plt.ylim(1e-5, 1e3)
  plt.axhline(y=1e-3, color='red', linestyle='--')
  if args.DEBUG == True and sqrt == 13.6 and args.SQUARK == True:
    plt.axhline(y=7232, color='gray', linestyle='--') #debug lines
    plt.axhline(y=835.7, color='gray', linestyle='--')  
    plt.axhline(y=0.941, color='gray', linestyle='--') 
    plt.axhline(y=0.0313, color='gray', linestyle='--')
    plt.axhline(y=0.0313, color='gray', linestyle='--')
    plt.axhline(y=0.00215, color='gray', linestyle='--')
  if args.DEBUG == True and sqrt == 13 and args.SQUARK == True:
    plt.axhline(y=6589, color='gray', linestyle='--') #debug lines
    plt.axhline(y=755, color='gray', linestyle='--')  
    plt.axhline(y=44.6, color='gray', linestyle='--') 
    plt.axhline(y=0.798, color='gray', linestyle='--')
    plt.axhline(y=0.0239, color='gray', linestyle='--')
    plt.axhline(y=0.00144, color='gray', linestyle='--')

else:
  plt.ylim(1e-1, 1e4)
  plt.gca().yaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=15))
  # Add a horizontal blue line at y=1
  plt.axhline(y=1, color='green', linestyle='--')
  if args.LIMITS == True and args.SQUARK == True:
    plt.axvline(x=1500, color='orange', linestyle='--')
  if args.LIMITS == True and args.SLEPTON == True:
    plt.axvline(x=700, color='blue', linestyle='--')
  
plt.legend(ncol = 2, framealpha = 1)
if int(args.LUMI) < 0:  
  plt.title(r"$pp$, $\sqrt{s}$ = "+str(sqrt)+r" TeV, NLO+NLL - NNLO$_\mathregular{approx}$+NNLL", fontsize = 9, loc = "right")
else:
  plt.title(r"$pp$, $\sqrt{s}$ = "+str(sqrt)+r" TeV, "+str(int(args.LUMI))+r" fb$^{-1}$", fontsize = 9, loc = "right")

plt.rcParams['text.usetex'] = True # add this line to enable LaTeX rendering

for format in ["pdf", "png", "eps"]:
  if int(args.LUMI) < 0:  
    label = "xsec"
  else:
    label = "lumi_{LUMINOSITY}".format(LUMINOSITY = str(int(args.LUMI)))

  model = "all"
  if args.GLUINO == True: model = "gluino"
  if args.SQUARK == True: model = "squark"
  if args.SLEPTON == True: model = "slepton"
  if args.STAU == True: model = "stau"
  if args.DEBUG == True and args.SQUARK == True: model = model + "_debug"
  if args.LIMITS == True: model = model + "_limits"

  plt.savefig("plots/SUSY_sqrt_{SQRT}_{LABEL}_{MODEL}.{FORMAT}".format(SQRT=sqrt, LABEL = label, MODEL = model, FORMAT = format))
  plt.clf()

