import ROOT as rt
import numpy as np
file = rt.TFile.Open('/nfs/cms/martialc/Displaced2024/llp/data/DiMuons_1PM.root')
tree = file.Get('SimpleNTupler/DDTree')


canvas = rt.TCanvas('c')
canvas.SetLogy()
hist = rt.TH1D('h','patmu_mu1_pt hist',100,0,5000)
tree.Draw('patmu_mu1_pt >> h')
print(hist.Integral())
hist.Draw('SAMES',)

# hist.GetXaxis().SetRangeUser(0,100)
canvas.Draw()
canvas.SaveAs('/nfs/cms/martialc/Displaced2024/llp/sandbox/figs/test.pdf')