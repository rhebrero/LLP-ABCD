from llp.utils import load_macro
import ROOT
load_macro('getNHighest')


def getNHighest(
        entry       : ROOT.TTree            ,
        branch      : str           = None  ,
        selection   : str           = None  ,
        idx         : str           = None  ,       
        n           : int           = 2     ,
        do_abs      : bool          = True  ,
    ) -> int:
    if (branch is not None) & (selection is None) & (idx is None):
        return ROOT.getNHighest(
                getattr(entry, branch),
                n,
                do_abs
            )
    elif (branch is not None) & (selection is not None) & (idx is None):
        return ROOT.getNHighest_fromIdx(
                getattr(entry, branch),
                getattr(entry, selection),
                n,
                do_abs
            )
    elif (branch is None) & (selection is None) & (idx is not None):
        return ROOT.getNHighest_fromBranch(
                getattr(entry, idx),
                n
            )