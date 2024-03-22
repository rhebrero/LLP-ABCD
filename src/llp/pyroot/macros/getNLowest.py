from llp.utils import load_macro
import ROOT
load_macro('getNLowest')


def getNLowest(
        entry       : ROOT.TTree            ,
        branch      : str           = None  ,
        selection   : str           = None  ,
        idx         : str           = None  ,       
        n           : int           = 2     ,
        do_abs      : bool          = True  ,
    ) -> int:
    try:
        if (branch is not None) & (selection is None) & (idx is None):
            return ROOT.getNLowest(
                    getattr(entry, branch),
                    n,
                    do_abs
                )
            
        elif (branch is not None) & (selection is not None) & (idx is None):
            return ROOT.getNLowest_fromIdx(
                    getattr(entry, branch),
                    getattr(entry, selection),
                    n,
                    do_abs
                )
        elif (branch is None) & (selection is None) & (idx is not None):
            return ROOT.getNLowest_fromBranch(
                    getattr(entry, idx),
                    n
                )
    except Exception as e:
        if (branch is not None) & (selection is None) & (idx is None):
            print(
                    getattr(entry, branch),
                    n,
                    do_abs
                )
            
        elif (branch is not None) & (selection is not None) & (idx is None):
            print(
                    getattr(entry, branch),
                    getattr(entry, selection),
                    n,
                    do_abs
                )
        elif (branch is None) & (selection is None) & (idx is not None):
            print(
                    getattr(entry, idx),
                    n
                )
        raise e