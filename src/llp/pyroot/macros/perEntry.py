import ROOT as ROOT

def perEntry(
    entry   : ROOT.TTree,
    branch  : str
):
    return any(getattr(entry,branch))