from llp.utils import load_macro
import ROOT
load_macro('getNHighest')


def getNHighest(
        entry       : ROOT.TTree            ,
        branch      : str                   ,
        selection   : str           = None  ,
        n           : int           = 2     ,
        do_abs      : bool          = True  ,
    ) -> int:
    if selection is None:
        return ROOT.getNHighest(
                getattr(entry, branch),
                n,
                do_abs
            )
    else:
        return ROOT.getNHighest_fromIdx(
                getattr(entry, branch),
                getattr(entry, idx),
                n,
                do_abs
            )