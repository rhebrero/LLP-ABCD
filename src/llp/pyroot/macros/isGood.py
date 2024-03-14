from llp.utils import load_macro
import ROOT
load_macro('isGood')


def isGood(
        entry               : ROOT.TTree        ,
        branch              : str   = 'patmu'   ,
        nMatchedStations    : int   = 1         ,
        nTrackerLayers      : int   = 5         ,
        pt                  : float = 5         ,
        ptRelError          : float = 1         ,
        per_muon            : bool  = True      ,
    ) -> 'ROOT.VecOps.RVecI':
    
    return ROOT.isGood(
        getattr(entry,f'{branch}_nMatchedStations'),
        getattr(entry,f'{branch}_nTrackerLayers'),
        getattr(entry,f'{branch}_pt'),
        getattr(entry,f'{branch}_ptError'),
        nMatchedStations,
        nTrackerLayers,
        pt,
        ptRelError
    )