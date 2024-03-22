import ROOT as rt
import numpy as np
import pathlib
from collections.abc import Iterable
from llp.pyroot.classes import Tree
import llp.pyroot.utils.io as io

import pathlib

class Hist(object):
    fig_formats = [".png", ".pdf", ".tex", ".C"]
    active_canvas = 0
    def __init__(
        self,
        prefix      = '',
        suffix      = '',
        nbins       = 100,
        range       = None,
        norm        = False,
        logy        = False,
        logx        = False,
        selection   = None,
        alias                               = None,
        canvas      : rt.TCanvas            = None,
        subplot                             = 0

    ):
        if not canvas:
            Hist.active_canvas     += 1
            if not alias:
                self._alias = f'c{self.active_canvas}'
            else:
                self._alias = alias
            self.canvas = rt.TCanvas(self.alias)
        else:
            self.canvas = canvas
        
        self.color_palette      = None
        self.color_generator    = None
        
        self.trees = {}
        self.subplot = subplot
        self.effs = {}
        
        self.histograms = {}
        self.filters = []
        self.colors ={}
        
        
        self.legend = rt.TLegend(0.15, 0.7, 0.35, 0.85)
        self.logx = logx
        self.logy = logy
        
        if logy: self.canvas.SetLogy()
        if logx: self.canvas.SetLogx()
        
        self.nbins = nbins
        self.range = range
        self.norm = norm
        
        self.ymax = 0
        self.ymin = 0.8
        
        if not selection:   self.selection = '1'
        else:               self.selection = selection
        
        pass
    
    @property
    def alias(self):
        return self._alias
    
    def subplots():
        pass
    
    @staticmethod
    def get_tree(file_path,tree_path):
        if isinstance(file_path, (str, pathlib.Path)):
            file_list = [str(file_path)]
        elif isinstance(file_path, Iterable):
            file_list = [str(file) for file in file_path]
        else:
            raise ValueError(f'file_path must be path or list of paths, {type(file_path)} given instead')
        
        tree = rt.TChain(tree_path)
        [tree.Add(file) for file in file_list]
        return tree
    
    def subplots(self, nrows, ncols, xpad = 0.01, ypad =0.01):
        self.canvas.Divide(ncols,nrows,xpad,ypad)
    
    
    def add_hist(
            self,
            branch,
            title           : str                               ,
            file_path       : str                               ,
            tree_path       : str                               ,
            friend_path     : str                   = []        ,
            selection       : str                   = None      ,
            kind            : str                   = 'data'    ,
            weight          : float                 = None      ,
            ylabel          : str                   = 'Events'  ,
            plot_type       : str                   = 'hist'    ,
            subplot         : int                   = 0         ,
            alias           : str                   = None
        ):
        
        self.canvas.cd(self.subplot)
        
        tree    = Hist.get_tree(file_path,tree_path)
        friend  = Hist.get_tree(friend_path,tree_path)
        tree.AddFriend(friend)
        if not alias:
            hist_id = f'h{str(len(self.histograms))}' # h0, h1, h2...
        else:
            hist_id = alias
        
        self.trees      [hist_id] = tree
        self.colors     [hist_id] = color = self.get_color()
        
        if not self.range:
            self.histograms [hist_id] = hist  = rt.TH1D(
                                                    hist_id,
                                                    title,
                                                    self.nbins
                                                )
        elif self.logx:
            xbins = np.logspace(*np.log10(self.range),self.nbins+1,base=10)
            
            self.histograms [hist_id] = hist  = rt.TH1D(
                                                    hist_id,
                                                    title,
                                                    self.nbins,
                                                    xbins.astype(np.double)
                                                )
        else:
            self.histograms [hist_id] = hist  = rt.TH1D(
                                                    hist_id,
                                                    title,
                                                    self.nbins,
                                                    *np.double(self.range)
                                                )
                            
        # scale = 1
        # if weight: scale *= weight
        print(f'\n\nINFO: {title}')
        if selection is None:
            print(f'  Filtros:\t {self.selection}')
            tree.Draw(
                f'{branch} >> {hist_id}',
                f'{self.selection}',
                'goff' #TODO: Preguntarle a Alberto por qué hace esto.
            )
        else:
            
            print('  Filtros:\t('+') && ('.join([selection,self.selection])+')')
            tree.Draw(
                f'{branch} >> {hist_id}',
                '('+') && ('.join([selection,self.selection])+')',
                'goff' #TODO: Preguntarle a Alberto por qué hace esto.
            )
            
        print(f'  Integral:\t{hist.Integral()}')
        print(f'  NEntries:\t{tree.GetEntries()}')
        print(f'  Eff.:    \t{hist.Integral()/tree.GetEntries()*100:6<3.2f}%')
        
        scale = 1
        if weight: scale *= weight
        if self.norm & (hist.Integral() > 0): scale /= hist.Integral()
        hist.Scale(scale)
        
        hist.Draw(plot_type)
            
        self.effs[alias] = hist.Integral()/tree.GetEntries()
        hist.SetLineColor(color)
        
        if weight: ylabel += ' scaled'
        elif self.norm: ylabel += ' norm.'
        
        if len(self.histograms) == 1:
            hist.GetXaxis().SetTitle(branch)
            hist.GetYaxis().SetTitle(ylabel)
        
        rt.gPad.Update()
        
        stats = hist.FindObject('stats')
        
        hist.SetTitle(title)
        stats.SetTextColor(color)
        stats.SetX1NDC(0.80-0.2*len(self.histograms))
        stats.SetX2NDC(0.99-0.2*len(self.histograms))
        
        self.ymax = max(hist.GetMaximum(),self.ymax)
        self.ymin = min(scale,self.ymin)
        self.update_ylims()

        self.canvas.Update()
        self.canvas = self.canvas.DrawClone()
        
        return 

    def update_ylims(self):
        for hist in self.histograms.values():
            # ymin = np.power(10,np.floor(np.log10(self.ymin)-1))*0.8
            ymin = 0.8
            # ymax = np.power(10,np.ceil(np.log10(self.ymax)+1))*1.2
            ymax = 1e6
            hist.GetYaxis().SetRangeUser(ymin,ymax)
    
    def add_data(self,*args,**kwargs):
        self.add_hist(*args,plot_type = 'HIST', **kwargs)
    
    def add_signal(self,*args,**kwargs):
        self.add_hist(*args,plot_type = 'SAMES', **kwargs)
    
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























# if __name__ == '__main__':
#     file_hist = [
#         '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_BC__000_1e5.root',
#         '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_BC__1e5_2e5.root',
#         '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_BC__2e5_3e5.root',
#         '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_BC__3e5_4e5.root',
#     ]
#     signal = '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/StopToMuB_v05/StopToMuB_500_1.root'
    
#     h = Hist('dimPL_mass',range = (0,300), nbins=100, logy = True, norm = True)
#     h.add_data('DiMuon data',
#         file_hist,
#         'SimpleNTupler/DDTree'
#     )
#     h.add_signal('Stop 500 GeV 1 mm',
#         signal,
#         'SimpleMiniNTupler/DDTree',
#         weight = 0.03
#     )
#     h.save_to('/nfs/cms/martialc/Displaced2024/llp/sandbox/figs/test')
    

