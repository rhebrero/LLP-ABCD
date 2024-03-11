from llp.utils import load_macro
import ROOT
load_macro('getNHighest')


def getNHighest(
        entry   : ROOT.TTree            ,
        branch  : str                   ,
        mu_type : str           = 'pat' ,
        mu_idx  : str           = None  ,
        n       : int           = 2     ,
        do_abs  : bool          = True  ,
    ) -> int:
    if mu_idx is None:
        return ROOT.getNHighest(
                getattr(entry, f'{mu_type}mu_{branch}'),
                n,
                do_abs
            )
    else:
        return ROOT.getNHighest_fromIdx(
                getattr(entry, f'{mu_type}mu_{branch}'),
                getattr(entry, mu_idx),
                n,
                do_abs
            )