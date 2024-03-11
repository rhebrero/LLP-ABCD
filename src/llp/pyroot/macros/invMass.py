from llp.utils import load_macro
import ROOT
load_macro('invMass')


def invMass_MuMu(
        entry       : ROOT.TTree           ,
        mu_idx1     : str                  ,
        mu_idx2     : str                  ,
        mu_type     : str           = 'pat'
    ) -> 'ROOT.VecOps.RVecF':
    
    return ROOT.invMass_fromIdx(
            getattr(entry,mu_idx1)[0],
            getattr(entry,mu_idx2)[0],
            getattr(entry, f'{mu_type}mu_pt'),
            getattr(entry, f'{mu_type}mu_eta'),
            getattr(entry, f'{mu_type}mu_phi'),
        )