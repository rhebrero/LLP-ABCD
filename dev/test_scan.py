import ROOT as rt
import numpy as np
file = rt.TFile.Open('/pnfs/ciemat.es/data/cms/store/user/escalant/displacedLeptons/StopToMuB_v05/StopToMuB_500_10.root')
tree = file.Get('SimpleMiniNTupler/DDTree')
# 215
value = rt.std.vector('string')()
tree.SetBranchAddress('trig_hlt_idx',value)

tree.GetEntry(215)
print(value)