from llp.utils import load_macro
import ROOT
load_macro('mu_nPrompt')


def mu_nPrompt(
        entry   : ROOT.TTree            ,
        d0_cut  : float         = 0.1   ,
        mu_type : str           = 'pat'
    ) -> int:
    return ROOT.mu_nPrompt(
            getattr(entry, f'{mu_type}mu_d0_pv'),
            d0_cut
        )