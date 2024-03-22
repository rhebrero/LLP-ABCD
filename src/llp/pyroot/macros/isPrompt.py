from llp.utils import load_macro
import ROOT
load_macro('isPrompt')


def isPrompt(
        entry               : ROOT.TTree        ,
        branch              : str   = 'patmu'   ,
        d0sig               : float = 1.2       ,
        per_muon            : bool  = True      ,
    ) -> 'ROOT.VecOps.RVecI':
    
    return ROOT.isPrompt(
        getattr(entry, f'{branch}_d0_pv'    ),
        getattr(entry, f'{branch}_d0sig_pv' ),
        getattr(entry, f'{branch}_isGood'   ),
        d0sig
    )