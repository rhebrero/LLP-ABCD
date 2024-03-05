import ROOT as ROOT

def perEntry(
    entry   : ROOT.TTree,
    branch  : str
):
    return ROOT.VecOps.Any(getattr(entry,branch))