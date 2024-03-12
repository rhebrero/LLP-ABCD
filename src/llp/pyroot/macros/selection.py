from llp.utils import load_macro
import ROOT
load_macro('selection')


def selectionMask(
        entry       : ROOT.TTree                ,  
        cut         : str                       ,
        branch      : str           = 'patmu'   ,
        per_muon    : bool          = True  
    ) -> 'ROOT.VecOps.RVecI':
    """
    Returns 0 and 1 for each muon, whether they pass the cut.
    The length of the vector is given through "{branch}_nMuons"
    """
    result = ROOT.selectionMask(entry,cut,getattr(entry,f'{branch}_nMuons')[0])
    
    if per_muon:
        return result
    else:
        return ROOT.VecOps.Any(result)

def selectionIdx(
        entry       : ROOT.TTree                ,  
        branch      : str           = 'patmu'   ,
        selection   : str           = None      ,
        cut         : str           = None  
    ) -> 'ROOT.VecOps.RVecI':
    """
    Returns the index of the muons that pass the selection.
        - if selecion is defined: Checks {branch}_{selection}.
        - if cut      is defined: Computes cut and returns the indexes of the muons that pass the cut.
    """
    if (cut is not None) & (selection is None):
        return ROOT.selectionIdxFromCut(entry,cut,getattr(entry,f'{branch}_nMuons')[0])
    elif (selection is not None) & (cut is None):
        return ROOT.selectionIdxFromMask(getattr(entry,f'{branch}_{selection}'))
    else:
        raise RuntimeError("Both \"branch\" and \"cut\" can't be set.")

def nPassing(
        entry       : ROOT.TTree            ,
        branch      : str                   ,
        selection   : str           = None  ,
        cut         : str           = None  
    ) -> int:
    
    if (cut is not None) & (selection is None):
        return ROOT.nPassing(entry,cut,getattr(entry,f'{branch}_nMuons')[0])
    elif (selection is not None) & (cut is None):
        return sum(getattr(entry,f'{branch}_{selection}'))
    else:
        raise RuntimeError("Both \"branch\" and \"cut\" can't be set.")