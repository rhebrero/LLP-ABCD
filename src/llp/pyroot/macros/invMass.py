from llp.utils import load_macro
import ROOT
load_macro('invMass')


def invMass_MuMu(
        entry       : ROOT.TTree           ,
        mu_idx1     : str                  ,
        mu_idx2     : str                  ,
        branch      : str         = 'patmu',
    ) -> 'ROOT.VecOps.RVecF':
    
    return ROOT.invMass_fromIdx(
            getattr(entry,mu_idx1)[0],
            getattr(entry,mu_idx2)[0],
            getattr(entry, f'{branch}_pt'),
            getattr(entry, f'{branch}_eta'),
            getattr(entry, f'{branch}_phi'),
        )