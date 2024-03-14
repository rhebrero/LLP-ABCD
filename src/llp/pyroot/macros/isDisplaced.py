from llp.utils import load_macro
import ROOT
load_macro('isDisplaced')


def isDisplaced(
        entry               : ROOT.TTree        ,
        branch              : str   = 'patmu'   ,
        d0                  : float = 0.1       ,
        d0sig               : float = 6         ,
        per_muon            : bool  = True      ,
    ) -> 'ROOT.VecOps.RVecI':
    
    return ROOT.isDisplaced(
        getattr(entry, f'{branch}_d0_pv'    ),
        getattr(entry, f'{branch}_d0sig_pv' ),
        d0,
        d0sig
    )