import ROOT as rt
import numpy as np
from llp.utils.macros import load_macro
from llp.pyroot import Hist
import numpy as np

file_hist = '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_BC.root',

signal_d0 = 10
signal_100 = f'/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/StopToMuB_v05/StopToMuB_100_{signal_d0}.root'
signal_500 = f'/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/StopToMuB_v05/StopToMuB_500_{signal_d0}.root'

h = Hist('patmu_pt[patmu_mu1_d0_pv_idx]',
    range       = (0,100)        ,
    nbins       = 200            ,
    logy        = True          ,
    # norm        = True          ,
    selection   = 'patmu_isGood && (patmu_nGood > 1) && (patmu_nDisplaced > 1) && (patmu_mu1_d0_pv_idx >= 0) && (patmu_mu1L_d0_pv_idx >= 0)'
)
h.add_data('DiMuon data',
    file_hist,
    'SimpleNTupler/DDTree',
    selection = '((dimPL_mass < 70) || (dimPL_mass > 110))'
)
h.add_signal(f'Stop 100 GeV {signal_d0} mm',
    signal_100,
    'SimpleMiniNTupler/DDTree',
)
h.add_signal(f'Stop 500 GeV {signal_d0} mm',
    signal_500,
    'SimpleMiniNTupler/DDTree',
)
h.save_to('/nfs/cms/martialc/Displaced2024/llp/sandbox/figs/current')
