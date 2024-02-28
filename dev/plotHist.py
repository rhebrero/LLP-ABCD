import ROOT as rt
import numpy as np
import pathlib
from collections.abc import Iterable

for macro in pathlib.Path('/nfs/cms/martialc/Displaced2024/llp/sandbox/pyroot/macros').glob('**/*.C'):
    if rt.gROOT.LoadMacro(str(macro)):
        raise OSError(f'Unable to load: {macro}')


class Histogram(object):
    fig_formats = [".png", ".pdf", ".tex", ".C"]
    def __init__(
        self,
        branch,
        nbins = 100,
        range = None,
        norm = False,
        logy = False
    ):
        self.color_palette = None
        self.color_generator = None
        self.branch = branch
        
        self.histograms = {}
        self.filters = []
        self.colors ={}
        
        self.canvas = rt.TCanvas('canvas')
        self.legend = rt.TLegend(0.15, 0.7, 0.35, 0.85)
        if logy: self.canvas.SetLogy()
        
        self.nbins = nbins
        self.range = range
        self.norm = norm
        pass
    
    def add_data(
            self,
            file_path,
            tree_path,
            label = None,
            filters = [],
            kind = 'data'
        ):
        
        plot_type = {
            'data' : 'hist'
        }
        
        
        if label is None: label = f'h{len(self.histograms)}'
        
        # Preguntarle a Alberto por esto
        if len(self.histograms) == 0: plot_label = 'hist'       # Quieres que los datos salgan así
        else: plot_label = 'SAMES'                              # Y el MC salga así
                

        self.colors[label] = color = self.get_color()
        
        
        if isinstance(file_path, (str, pathlib.Path)):
            files = [file_path]
        elif isinstance(file_path, Iterable):
            files = file_path
        
        if isinstance(filters, bool):
            if filters:
                filters = self.filters
            else:
                filters = []
        elif isinstance(filters,list):
            pass
        
        # Rellenamos el histograma
        tree = rt.TChain(tree_path)
        for i, file_path in enumerate(files):
            tree.Add(file_path)

        tree.SetAlias('isTest','test(patmu_d0_pv)')
        tree.SetAlias('isVTest','Vtest(patmu_d0_pv)')
        # tree.Scan('test')
        # Vformula = rt.TTreeFormula("Vtest", "Vtest(patmu_d0_pv)", tree)
        # tree.Scan('Vtest')
        
        
        if self.range is None:
            self.histograms[label] = hist = rt.TH1D(label, f'{self.branch} hist', self.nbins)
        
        else:
            self.histograms[label] = hist = rt.TH1D(label, f'{self.branch} hist', self.nbins, *np.double(self.range))
        print(f'Filtros: {" && ".join(filters)}')
        tree.Draw(
            f'{self.branch} >> {label}',
            ' && '.join(filters),
            'goff' #TODO: Preguntarle a Alberto por qué hace esto.
        )
        
        
        if self.norm & (hist.Integral() > 0):
            hist.Scale(1 / hist.GetEntries())
            
        hist.Draw(plot_label)
        hist.SetLineColor(color)
        hist.GetXaxis().SetTitle(self.branch)
        ylabel = 'Events'
        if self.norm: ylabel += ' norm.' 
        hist.GetYaxis().SetTitle(ylabel)
        
        rt.gPad.Update()
        stats = hist.FindObject('stats')
        stats.SetTextColor(color)
        stats.SetX1NDC(0.80-0.2*len(self.histograms))
        stats.SetX2NDC(0.99-0.2*len(self.histograms))
        
        
        self.canvas = self.canvas.DrawClone()
        
        return 

    def data_plot_type(self):
        plot_type = ''
    
    
    def plot_hist(self):
        self.canvas.Draw()
    

    def save_to(self,path):
        if isinstance(path,str):
            path = pathlib.Path(path)
        elif isinstance(path,pathlib.Path):
            pass
        else:
            raise TypeError(f'path type is incorrect: only str and pathlib.Path are allowed and an object of type {type(path)} was provided.')
        
        
        for format in self.fig_formats:
            self.canvas.SaveAs(str(path.with_suffix(format)))
    
        
    def set_color_generator(self):
        color_index = 1
        if self.color_palette is None:
            while True:
                yield color_index
                color_index += 1
        else:
            for color_index in self.color_palette:
                yield self.color_palette[color_index-1]

    def get_color(self):
        if not self.color_generator:
            self.color_generator = self.set_color_generator()
        return next(self.color_generator)
    
if __name__ == '__main__':
    
    files = [
        '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022B-ReReco-v2.root',
        # '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022C-ReReco-v2.root'
    ]
    
    branch = 'dim_mass'
    range = (0,200)
    bins = 200
    
    hist = Histogram(
        branch,
        nbins=bins,
        range = range,
        norm=False,
        logy=True
    )
    
    data_triggers = [
        'trig_hlt_path=="HLT_DoubleL2Mu23NoVtx_2Cha_v2"', # Para Era B
        'trig_hlt_path=="HLT_DoubleL2Mu23NoVtx_2Cha_v3"'  # para Era C
    ]
    triggers = '('+'||'.join(data_triggers)+')'
    data_filters = [
        # triggers,
        # 'patmu_idx == 0',
        # '(dimu_mass < 80 || dimu_mass > 110)',
        # 'patmu_asdasd > 10',
        'isVTest'
        
    ]
    
    
    hist.add_data(files,'SimpleNTupler/DDTree',filters = data_filters)
    
    # hist.add_data(files[0],'SimpleNTupler/DDTree',filters = [triggers])
    # hist.add_data(files[1],'SimpleNTupler/DDTree',filters = [triggers])
    
    
    fig_dir = pathlib.Path('/nfs/cms/martialc/Displaced2024/llp/sandbox/pyroot/figs')
    fig_name = pathlib.Path(f'data__{branch}__{"_".join(map(str,range))}')
    
    hist.save_to(fig_dir / fig_name)