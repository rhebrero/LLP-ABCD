from llp.utils import load_macro
import ROOT
load_macro('selectionMask')


def selectionMask(
        selection   : str           ,
        entry       : ROOT.TTree           
    ) -> 'ROOT.VecOps.RVecI':
    return ROOT.pt(
            selection,
            entry,
        )
