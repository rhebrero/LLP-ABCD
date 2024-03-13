from llp.utils import load_macro
import ROOT
load_macro('sortBy')


def sortBy(
        entry       : ROOT.TTree            ,
        branch      : str                   ,
        selection   : str           = None  ,
        cut         : str           = None  ,
        do_abs      : bool          = True  ,
    ) -> int:
    if (cut is None) & (selection is None):
        return ROOT.sortBy(
                getattr(entry, branch),
                do_abs
            )
    elif (cut is None) & (selection is not None):
        return ROOT.sortBy_fromMask(
                getattr(entry, branch),
                getattr(entry,selection),
                do_abs
            )
    elif (cut is not None) & (selection is None):
        return ROOT.sortBy_fromCut(
                entry,
                cut,
                getattr(entry, branch),
                do_abs
            )
    else:
        raise ValueError("'selection' and 'cut' can't be set at the same time.")