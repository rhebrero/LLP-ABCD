import ROOT as rt
import numpy as np
from llp.utils.macros import load_macro
from llp.pyroot import Hist
import numpy as np

file_hist = [
    '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_BC__000_1e5.root',
    '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_BC__1e5_2e5.root',
    '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_BC__2e5_3e5.root',
    '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_BC__3e5_4e5.root',
]
signal = '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/StopToMuB_v05/StopToMuB_500_1.root'

h = Hist('dimPL_mass',range = (0,300), nbins=100, logy = True, norm = True)
h.add_data('DiMuon data',
    file_hist,
    'SimpleNTupler/DDTree'
)
h.add_signal('Stop 500 GeV 1 mm',
    signal,
    'SimpleMiniNTupler/DDTree',
    weight = 0.03
)
h.save_to('/nfs/cms/martialc/Displaced2024/llp/sandbox/figs/current')
h.save_to('/nfs/cms/martialc/Displaced2024/llp/sandbox/figs/test')