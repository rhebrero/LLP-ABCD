import ROOT



data = [
    '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022B-ReReco-v2.root',
]
src_branches = {
            'evt_event'                 : ROOT.std.vector('int')(),
            'patmu_d0_pv'               : ROOT.std.vector('float')(),
            'patmu_idx'                 : ROOT.std.vector('int')(),
            'patmu_px'                  : ROOT.std.vector('double')(),
            'patmu_py'                  : ROOT.std.vector('double')(),
            'patmu_eta'                 : ROOT.std.vector('float')(),
            'patmu_phi'                 : ROOT.std.vector('float')(),
            'trig_hlt_path'             : ROOT.std.vector('string')(),
            'trig_hlt_idx'              : ROOT.std.vector('int')(),
            'patmu_nMatchedStations'    : ROOT.std.vector('int')(),
            'patmu_nTrackerLayers'      : ROOT.std.vector('int')(),
            'patmu_ptError'             : ROOT.std.vector('float')(),
            'patmu_d0sig_pv'            : ROOT.std.vector('float')(),
        }

tree = ROOT.TChain()
for data_file in data:
    tree.Add(data_file)

tree.SetBranchStatus('*',0)
for branch in src_branches.keys():
    tree.SetBranchStatus(branch,1)



target = ROOT.TFile('/nfs/cms/martialc/Displaced2024/llp/data/test.root','RECREATE')
tree.CloneTree(0)


