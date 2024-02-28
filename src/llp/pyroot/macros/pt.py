from llp.utils import load_macro
import ROOT
load_macro('pt')


def pt(
        entry   : ROOT.TTree           ,
        mu_type : str           = 'pat'
    ) -> 'ROOT.VecOps.RVecF':
    return ROOT.pt(
            getattr(entry, f'{mu_type}mu_px'),
            getattr(entry, f'{mu_type}mu_py'),
        )
