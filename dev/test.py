# print(' || '.join(['(patmu_d0_pv[{i}] > 1 && patmu_px[{i}])'.format(i = i) for i in range(10)]))



# def test(x,*args,**kwargs):
#     print(x)
#     print('args:\t',args,type(args))
#     print('kwargs:\t',kwargs,type(kwargs))
    
# test(*range(10),**{'a': 1, 'b': 2, 'c': 3})


import ROOT as rt
import numpy as np
file = rt.TFile.Open('/nfs/cms/martialc/Displaced2024/llp/data/test_nPrompt_1e3.root')
tree = file.Get('SimpleNTupler/DDTree')
from llp.utils.macros import load_macro



cut_string = 'abs(patmu_d0_pv) < 0.1'



def format_cut(cut,N):
    return '(' + ' || '.join(['(' + cut.format(i=i) + ')' for i in range(N)]) + ')'


new_branches = dict(
    patmu_pt         = dict(value = rt.VecOps.RVec('float') ((0))),
    passing_idx      = dict(value = rt.VecOps.RVec('int')   ((0))),
    patmu_mu1_pt_idx = dict(value = rt.VecOps.RVec('int')   ((0))),
    patmu_mu2_pt_idx = dict(value = rt.VecOps.RVec('int')   ((0))),
    patmu_mu1_d0_idx = dict(value = rt.VecOps.RVec('int')   ((0))),
    patmu_mu2_d0_idx = dict(value = rt.VecOps.RVec('int')   ((0))),
)

for branch_name, branch_dict in new_branches.items():
    tree.Branch(branch_name, branch_dict['value'])

muType = 'pat'
debug = True
debug_step = 10000
# tree.SetAlias('patmu_pt','sqrt(patmu_px**2+patmu_py**2)')

load_macro('selectionCut')
load_macro('getNHighest')
load_macro('pt')


print(f'Corte: {cut_string}')
for i in range(tree.GetEntries()):
    tree.GetEntry(i)
    # N = len(getattr(tree,f'{muType}mu_idx'))
    # print(format_cut(cut_string,N))

    passing_idx = rt.selectionCut(cut_string,tree)
    new_branches['passing_idx']['value'] = passing_idx
    new_branches['patmu_pt']['value'] = rt.pt(tree.patmu_px,tree.patmu_py)
    
    
    get2Highest_d0 = rt.getNHighest(tree.patmu_d0_pv, passing_idx, 2, True)
    new_branches['patmu_mu1_d0_idx']['value'] = get2Highest_d0[0]
    new_branches['patmu_mu2_d0_idx']['value'] = get2Highest_d0[1]
    
    get2Highest_pt = rt.getNHighest(tree.patmu_pt, passing_idx, 2, False)
    new_branches['patmu_mu1_pt_idx']['value'] = get2Highest_pt[0]
    new_branches['patmu_mu2_pt_idx']['value'] = get2Highest_pt[1]

    if not i % debug_step & len(passing_idx) >= 2 & debug:
        passing_d0 = [tree.patmu_d0_pv[i] for i in passing_idx]
        passing_pt = [tree.patmu_pt[i] for i in passing_idx]
        print(
            "\n"
            "==========================================\n"
            f"EventNr {i}\n"
            "==========================================\n"
            f" All muons: {tree.patmu_idx}\n"
            f" Passing muons: {passing_idx}\n"
            "---------------------------------------------\n"
            f'All mu: {[f"{d0:.5f}" for d0 in tree.patmu_d0_pv]}\n'
            f'Passing mu: {[f"{d0:.5f}" for d0 in passing_d0]}\n'
            f"   1st highest d0: {get2Highest_d0[0]} {tree.patmu_d0_pv[get2Highest_d0[0]]:.5f}\n"
            f"   2nd highest d0: {get2Highest_d0[1]} {tree.patmu_d0_pv[get2Highest_d0[1]]:.5f}\n"
            "---------------------------------------------\n"
            f'All mu: {[f"{pt:.5f}" for pt in tree.patmu_pt]}\n'
            f'Passing mu: {[f"{d0:.5f}" for d0 in passing_pt]}\n'
            f"   1st highest pt: {get2Highest_pt[0]} {tree.patmu_pt[get2Highest_pt[0]]:.5f}\n"
            f"   2nd highest pt: {get2Highest_pt[1]} {tree.patmu_pt[get2Highest_pt[1]]:.5f}\n"
        )
        
        # print(type(get2Highest_d0))
    # formula = rt.TTreeFormula('selection',cut_string,tree)
    # value[0] = rt.selectionCut(formula)

    
