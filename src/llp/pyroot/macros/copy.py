from llp.utils import load_macro
import ROOT
load_macro('copy')

def copyFloat(
        entry       : ROOT.TTree    ,
        branch      : str           ,
    ) -> float:
    return ROOT.copyFloat(
        getattr(entry, branch),
    )

def copyInt(
        entry       : ROOT.TTree    ,
        branch      : str           ,
    ) -> int:
    return ROOT.copyInt(
        getattr(entry, branch),
    )

def copyVFloat(
        entry       : ROOT.TTree    ,
        branch      : str           ,
    ) -> float:
    return ROOT.copyVFloat(
        getattr(entry, branch),
    )

def copyVInt(
        entry       : ROOT.TTree    ,
        branch      : str           ,
    ) -> int:
    return ROOT.copyVInt(
        getattr(entry, branch),
    )