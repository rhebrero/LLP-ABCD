from llp.utils import load_macro
import ROOT
load_macro('getNElement')

def getNElement(
        entry       : ROOT.TTree    ,
        branch      : str           ,
        n           : int           ,
    ) -> int:
        return ROOT.getNElement(
            getattr(entry, branch),
            n
        )