import ROOT as rt
from Histogram import Histogram
import cmsstyle as CMS
import pdb
from xsec import getCrossSection as gxsec
from xsec import json
from files_dicts import *
from files import *
from functions import *
import argparse

class Canvas_Class():
    def __init__(self, lumi='0.11'):
        if not isinstance(lumi, str):
            lumi = str(lumi)
        self.lumi = lumi[:4]
        self.set_common_settings()

    def set_common_settings(self):
        CMS.SetExtraText('Private work')
        CMS.SetLumi(self.lumi)
        CMS.SetEnergy('13.6')

    def create_ratio_canvas(self, var_name, inbin, endbin, label, y_max, logy=False):
        canv_name = label
        xlabel = self.get_fancy_label(var_name)
        
        canv = CMS.cmsDiCanvas(
            canv_name,
            inbin,
            endbin,
            1.1e-1,
            y_max * 10,
            0,
            2.5,
            xlabel,
            'Events',
            "Data/Pred.",
            square=CMS.kSquare,
            extraSpace=0.01,
            iPos=0,
        )
        if logy:
            canv.SetLogy(True)
        return canv

    def create_canvas(self, var_name, inbin, endbin, label, y_max, logy=True, ylabel='Events'):
        canv_name = label
        xlabel = self.get_fancy_label(var_name)
        if logy:
            y_max *= 10
        
        canv = CMS.cmsCanvas(
            canv_name,
            inbin,
            endbin,
            1.1e-3,
            y_max,
            xlabel,
            ylabel,
            square=CMS.kRectangular,  # CMS.kSquare,
            extraSpace=0.01,
            iPos=0,
        )
        if logy:
            canv.SetLogy(True)
        return canv

    def create_sig_canvas(self, inbin, endbin, y_max, y_min, y_label, log=True):
        canv_name = y_label
        if log:
            y_max *= 10
        else:
            y_min = 0

        canv = CMS.cmsCanvas(
            canv_name,
            inbin,
            endbin,
            y_min,
            y_max,
            "c#tau [cm]",
            y_label,
            square=CMS.kSquare,
            extraSpace=0.01,
            iPos=0,
        )
        if log:
            canv.SetLogy(True)
        canv.SetLogx(True)
        return canv

    def get_fancy_label(self, var_name):
        labels = {
            'hasVtx': 'Different vertex                    Same vertex   ',
            'iso': '#mu(Iso/p_{T})',
            'd0sig': 'd_{0, #sigma}(#mu^{+})',
            'invMass': 'm_{#mu#mu} [GeV]',
            'pt': 'p_{T}^{#mu} [GeV]',
            'd0err': '#sigma_{d_{0}}',
            'd0': 'd_{0}',
            'lxyerr': '#sigma_{Lxy}',
            'DeltaR': '#Delta R'
        }
        return labels.get(var_name, '')

