from llp.utils import load_macro
import ROOT
load_macro('selection')


def selectionMask(
        entry       : ROOT.TTree,  
        cut         : str,
        per_muon    : bool          = True
    ) -> 'ROOT.VecOps.RVecI':
    
    if per_muon:
        return ROOT.selectionMask(entry,cut)
    else:
        return ROOT.VecOps.Any()

def selectionIdx(
        entry       : ROOT.TTree            ,  
        branch      : str           = None  ,
        cut         : str           = None
    ) -> 'ROOT.VecOps.RVecI':
    
    if (cut is not None) & (branch is None):
        return ROOT.selectionIdxFromMask(entry,cut)
    elif (branch is not None) & (cut is None):
        return ROOT.selectionIdxFromBranch(getattr(entry,branch))
    else:
        raise RuntimeError("Both \"branch\" and \"cut\" can't be set.")

def nPassing(
        entry   : ROOT.TTree            ,
        branch  : str           = None  ,
        cut     : str           = None
    ) -> int:
    
    if (cut is not None) & (branch is None):
        return ROOT.nPassing(entry,cut)
    elif (branch is not None) & (cut is None):
        return ROOT.VecOps.Sum(getattr(entry,branch))
    else:
        raise RuntimeError("Both \"branch\" and \"cut\" can't be set.")