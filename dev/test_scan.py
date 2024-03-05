import ROOT as rt
import numpy as np
file = rt.TFile.Open('/nfs/cms/martialc/Displaced2024/llp/data/DoMuons_1PM.root')
tree = file.Get('SimpleNTupler/DDTree')

tree.Scan('*')