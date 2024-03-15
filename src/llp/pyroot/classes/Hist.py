import ROOT as rt
import numpy as np
import pathlib
from collections.abc import Iterable
from llp.pyroot.classes import Tree
import pathlib

class Hist(object):
    fig_formats = [".png", ".pdf", ".tex", ".C"]
    plot_type = {
            'data'      :   'HIST',
            'signal'    :   'SAMES'
        }
    
    def __init__(
        self,
        branch,
        prefix = '',
        suffix = '',
        nbins = 100,
        range = None,
        norm = False,
        logy = False,
        selection = None
    ):
        self.color_palette = None
        self.color_generator = None
        self.branch = branch
        
        self.trees = {}
        
        
        
        self.histograms = {}
        self.filters = []
        self.colors ={}
        
        self.canvas = rt.TCanvas('canvas')
        self.legend = rt.TLegend(0.15, 0.7, 0.35, 0.85)
        if logy: self.canvas.SetLogy()
        
        self.nbins = nbins
        self.range = range
        self.norm = norm
        
        if not selection:   self.selection = '1'
        else:               self.selection = selection
        
        pass
        
    
    
    def add_hist(
            self,
            title           : str                               ,
            file_path       : str                               ,
            tree_path       : str                               ,
            freinds_path    : str                   = []        ,
            selection       : str                   = None      ,
            kind            : str                   = 'data'    ,
            weight          : float                 = None      ,
            ylabel          : str                   = 'Events'  ,
            plot_type       : str                   = 'data'    ,
        ):
        
        if isinstance(file_path, (str, pathlib.Path)):
            file_list = [str(file_path)]
        elif isinstance(file_path, Iterable):
            file_list = [str(file) for file in file_path]
        else:
            raise ValueError(f'file_path must be path or list of paths, {type(file_path)} given instead')
        
        tree = rt.TChain(tree_path)
        [tree.Add(file) for file in file_list]
        
        hist_id = f'h{str(len(self.histograms))}' # h0, h1, h2...
        
        self.trees      [hist_id] = tree
        self.colors     [hist_id] = color = self.get_color()
        
        if not self.range:
            self.histograms [hist_id] = hist  = rt.TH1D(
                                                    hist_id,
                                                    title,
                                                    self.nbins
                                                )
        else:
            self.histograms [hist_id] = hist  = rt.TH1D(
                                                    hist_id,
                                                    title,
                                                    self.nbins,
                                                    *np.double(self.range)
                                                )
                            
        
        print(f'Filtros: {selection}')
        if selection:
            tree.Draw(
                f'{self.branch} >> {hist_id}',
                '('+') && ('.join([selection,self.selection])+')',
                'goff' #TODO: Preguntarle a Alberto por qué hace esto.
            )
        else:
            tree.Draw(
                f'{self.branch} >> {hist_id}',
                '('+') && ('.join(['1',self.selection])+')',
                'goff' #TODO: Preguntarle a Alberto por qué hace esto.
            )
        
        scale = 1
        if weight: scale *= weight
        if self.norm & (hist.Integral() > 0): scale /= hist.Integral()
        hist.Scale(scale)
        
        if len(self.histograms) > 1:
            hist.Draw('SAMES')
        else:
            hist.Draw(self.plot_type[plot_type])
            
            
        hist.SetLineColor(color)
        
        if weight: ylabel += ' scaled'
        elif self.norm: ylabel += ' norm.'
        
        if len(self.histograms) == 1:
            hist.GetXaxis().SetTitle(self.branch)
            hist.GetYaxis().SetTitle(ylabel)
        
        rt.gPad.Update()
        stats = hist.FindObject('stats')
        
        stats.SetTextColor(color)
        stats.SetX1NDC(0.80-0.2*len(self.histograms))
        stats.SetX2NDC(0.99-0.2*len(self.histograms))
        
        self.canvas = self.canvas.DrawClone()
        
        return 

    def add_data(self,*args,**kwargs):
        self.add_hist(*args,plot_type = 'data', **kwargs)
    
    def add_signal(self,*args,**kwargs):
        self.add_hist(*args,plot_type = 'signal', **kwargs)
    
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
    file_hist = [
        '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_BC__000_1e5.root',
        '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_BC__1e5_2e5.root',
        '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_BC__2e5_3e5.root',
        '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_BC__3e5_4e5.root',
    ]
    signal = '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/StopToMuB_v05/StopToMuB_500_1.root'
    
    h = Hist('dimPL_mass',range = (0,300), nbins=100, logy = True, norm = True)
    h.add_data('DiMuon data',
        file_hist,
        'SimpleNTupler/DDTree'
    )
    h.add_signal('Stop 500 GeV 1 mm',
        signal,
        'SimpleMiniNTupler/DDTree',
        weight = 0.03
    )
    h.save_to('/nfs/cms/martialc/Displaced2024/llp/sandbox/figs/test')