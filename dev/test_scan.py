import ROOT as rt
import numpy as np
file = rt.TFile.Open('/nfs/cms/martialc/Displaced2024/llp/data/test.root')
tree = file.Get('SimpleNTupler/DDTree')
# tree.SetBranchStatus('*',1)
tree.Scan('*')