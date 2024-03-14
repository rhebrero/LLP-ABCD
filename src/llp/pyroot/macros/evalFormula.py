from llp.utils import load_macro
import ROOT
load_macro('evalFormula')

def evalFormula(
        formula     : ROOT.TTreeFormula         ,
    ) -> 'ROOT.VecOps.RVecI':
    """
    Returns 0 and 1 for each muon, whether they pass the cut.
    The length of the vector is given through "{branch}_nMuons"
    """
    return ROOT.evalFormula(formula)
