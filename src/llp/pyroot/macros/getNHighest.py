from llp.utils import load_macro
import ROOT
load_macro('getNHighest')


def getNHighest(
        entry   : ROOT.TTree            ,
        branch  : str                   ,
        mu_type : str           = 'pat' ,
        n       : int           = 2     ,
        do_abs  : bool          = True
    ) -> int:
    return ROOT.getNHighest(
            getattr(entry, f'{mu_type}mu_{branch}'),
            getattr(entry, f'{mu_type}mu_idx'),
            n,
            do_abs
        )