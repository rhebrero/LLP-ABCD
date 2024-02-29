from llp.utils import load_macro
import ROOT
load_macro('nMuons')


def nMuons(
        entry   : ROOT.TTree            ,
        mu_type : str           = 'pat'
    ) -> int:
    return ROOT.nMuons(getattr(entry, f'{mu_type}mu_idx'))