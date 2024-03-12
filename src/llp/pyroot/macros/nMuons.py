from llp.utils import load_macro
import ROOT
load_macro('nMuons')


def nMuons(
        entry   : ROOT.TTree            ,
        branch  : str           = 'patmu'
    ) -> int:
    """
    Returns the length of "{branch}_idx", 'patmu_idx' by default.
    """
    return ROOT.nMuons(getattr(entry, f'{branch}_idx'))