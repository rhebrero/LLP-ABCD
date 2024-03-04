import ROOT as rt
import numpy as np
file = rt.TFile.Open('/nfs/cms/martialc/Displaced2024/llp/data/test_1e2.root')
tree = file.Get('SimpleNTupler/DDTree')

tree.Scan('*')