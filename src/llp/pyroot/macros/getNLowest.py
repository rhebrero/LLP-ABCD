from llp.utils import load_macro
import ROOT
load_macro('getNLowest')


def getNLowest(
        entry   : ROOT.TTree            ,
        branch  : str                   ,
        mu_type : str           = 'pat' ,
        mu_idx  : str           = None  ,
        n       : int           = 2     ,
        do_abs  : bool          = True  ,
    ) -> int:
    if mu_idx is None:
        return ROOT.getNLowest(
                getattr(entry, f'{mu_type}mu_{branch}'),
                n,
                do_abs
            )
    else:
        return ROOT.getNLowest_fromIdx(
                getattr(entry, f'{mu_type}mu_{branch}'),
                getattr(entry, mu_idx),
                n,
                do_abs
            )