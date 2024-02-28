import ROOT as rt
import numpy as np
import pathlib
from collections.abc import Iterable
from llp.pyroot.classes import Tree

class Hist(object):
    fig_formats = [".png", ".pdf", ".tex", ".C"]
    plot_type = {
            'data'  :   'hist',
            'sim'   :   'SAMES'
        }
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
        pass
    
    
    
    def add_tree(
            self,
            tree : Tree,
            label = None,
            kind = 'data'
        ):
        if not label: label = tree.alias
        
        self.trees      [label] = tree
        self.colors     [label] = color = self.get_color()
        self.histograms [label] = hist  = rt.TH1D(
                                                label,
                                                f'{self.branch} hist',
                                                self.nbins
                                            )
            
        
    
    def process_trees(self):
        for label, tree in self.trees.items():
            if self.range is None:
                pass
            else:
                self.histograms[label] = hist = rt.TH1D(label, f'{self.branch} hist', self.nbins, *np.double(self.range))

        pass
    
    
    def add_data(
            self,
            file_path,
            tree_path,
            label = None,
            filters = [],
            kind = 'data'
        ):
                
        
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
