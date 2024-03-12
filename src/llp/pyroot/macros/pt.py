from llp.utils import load_macro
import ROOT
load_macro('pt')


def pt(
        entry   : ROOT.TTree           ,
        branch  : str           = 'patmu'
    ) -> 'ROOT.VecOps.RVecF':
    """
    Returns the pt value calculated using branches "{branch}_px" and "{branch}_py".
    """
    return ROOT.pt(
            getattr(entry, f'{branch}_px'),
            getattr(entry, f'{branch}_py'),
        )
