import ROOT as rt
import numpy as np
file = rt.TFile.Open('/nfs/cms/martialc/Displaced2024/llp/data/test_nPrompt_1e3.root')
tree = file.Get('SimpleNTupler/DDTree')

tree.Scan('*')