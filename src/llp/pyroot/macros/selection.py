from llp.utils import load_macro
import ROOT
load_macro('selection')


def selectionMask(
        entry       : ROOT.TTree            ,  
        cut         : str                   ,
        n_muons      : str                   ,
        per_muon    : bool          = True  
    ) -> 'ROOT.VecOps.RVecI':
    result = ROOT.selectionMask(entry,cut,getattr(entry,n_muons)[0])
    
    if per_muon:
        return result
    else:
        return ROOT.VecOps.Any(result)

def selectionIdx(
        entry       : ROOT.TTree            ,  
        n_muons      : str                   ,
        branch      : str           = None  ,
        cut         : str           = None  
    ) -> 'ROOT.VecOps.RVecI':
    
    if (cut is not None) & (branch is None):
        return ROOT.selectionIdxFromCut(entry,cut,getattr(entry,n_muons)[0])
    elif (branch is not None) & (cut is None):
        return ROOT.selectionIdxFromMask(getattr(entry,branch))
    else:
        raise RuntimeError("Both \"branch\" and \"cut\" can't be set.")

def nPassing(
        entry   : ROOT.TTree            ,
        n_muons  : str                   ,
        branch  : str           = None  ,
        cut     : str           = None  
    ) -> int:
    
    if (cut is not None) & (branch is None):
        return ROOT.nPassing(entry,cut,getattr(entry,n_muons)[0])
    elif (branch is not None) & (cut is None):
        return sum(getattr(entry,branch))  
    else:
        raise RuntimeError("Both \"branch\" and \"cut\" can't be set.")