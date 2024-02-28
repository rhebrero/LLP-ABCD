import ROOT as rt
import llp.pyroot as pyrt
from llp.pyroot.macros import mu_nPrompt



t1 = pyrt.Tree(
    '/nfs/cms/martialc/Displaced2024/llp/data/t0.root',
    'SimpleNTupler/DDTree',
    debug = True,
    # nentries = 1000
    debug_step = 10000
)
print(t1.tree.Show())