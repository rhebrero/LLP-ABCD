from networkx import effective_size
import ROOT as rt
import numpy as np
import pathlib
from collections.abc import Iterable
from llp.pyroot.classes import Tree
from llp.pyroot.plots.classes.Plot import Plot
import llp.pyroot.utils.io as io
import llp.pyroot.utils.logic as logic

import pathlib
import json
from pprint import pprint

# Para que no muestre errores en ttreeformula
rt.RooMsgService.instance().setGlobalKillBelow(rt.RooFit.ERROR)

class Histogram(Plot):
    
    _default_alias  = 'h'
    _default_title  = 'Histogram'
    # _default_style  = 'hist'

    
    _cut_dict       = {}
    def __init__(self,
            file_path                   ,
            tree_path                   ,
            branch                      ,
            alias       = None          ,
            range       = None          ,
            nbins       = 100           ,
            friend_path = None          ,
            plot_style  = 'hist'        ,
            trigger     = {}            ,
            cut         = []            ,
            logx        = False         ,
            logy        = False         ,
            norm        = False         ,
            weight      = 1             ,
            title       = None          ,
            color       = 1             ,
        ):
        
        if not title: title = ' '.join([self._default_title,branch])
        super().__init__(
            alias       = alias                 ,
            plot_style  = plot_style            ,
            logx        = logx                  ,
            logy        = logy                  ,
            color       = color                 ,
            title       = self._default_title   ,
        )
        
        # inicializamos atributos
        self._hist          = None
        self._bins          = None
        self._nbins         = nbins
        self._trig_eff      = {}
        
        # Cargamos los datos
        self.tree    = io.get_tree(file_path,tree_path)
        if isinstance(friend_path,(str,Iterable)):
            self.friend  = io.get_tree(friend_path,tree_path)
            self.tree.AddFriend(self.friend)

        # Debe ir antes de xrange
        self.branch         = branch
        self.cut_dict       = cut
        self._cut_eff       = None
        self.trig_dict      = trigger
        self._trig_eff      = None
        
        # Asignamos los límites
        self._xlabel        = branch
        self._xrange        = range
        self._weight        = weight
        
        # Calculamos el histograma
        self.calc_hist()
        
        # print(json.dumps(self.trig_eff_study(),indent=4))
        # print(json.dumps(self.cut_eff_study(),indent=4))
        
        
        return
    
    @property
    def title(self):
        return self._title
    
    def calc_hist(self):
        self.canvas.cd()
        if not self.range:
            # WARNING: Esto no se puede hacer por un bug en ROOT y no quiero programar un macro
            # con un bucle en todas las entradas.
            # Hay que hacer esto porque TTree.GetMaximum/TTree.GetMinimum no funcionan
            # aux_alias = f'{self.alias}_aux'
            # aux_hist = rt.TH1D(
            #                     aux_alias,
            #                     'Ancillary Hist',
            #                     self.nbins,
            #                 )
            # self.tree.Draw()
            # self._xrange = [aux_hist.GetBinLowEdge(), aux_hist.GetBinLowEdge() + self.nbins*aux_hist.GetBinWidth()]
            raise NotImplementedError('"range" must be given as an argument to the class constructor')
        
        self._hist = hist = rt.TH1D(
                            self.alias,
                            self.title,
                            self.nbins,
                            self.bins
                        )
        
        # Rellenamos el histograma activo.
        rt.gROOT.ProcessLine("gErrorIgnoreLevel = 6001;")
        self.tree.Draw(
            f'{self.branch} >> {self.alias}',
            self.selection,
            'goff'
        )
                
        hist.GetXaxis().SetTitle(self.branch)
        hist.GetYaxis().SetTitle(self.ylabel)
        
        self.draw()
        
        
    
    @property
    def nbins(self):
        return self._nbins
    @property
    def xrange(self):
        return self._xrange
    @property
    def bins(self):
        if self._bins is None: self._bins = self.calc_bins()
        return self._bins
    
    @property
    def selection(self):
        return logic.join_and([self.cuts,self.trigger])
    
    @property
    def trigger(self):
        if len (self.trig_dict) > 0:
            trig = logic.join_and([
                logic.join_or(logic.trigger_parser(trig_lvl,trig_paths))
                for trig_lvl, trig_paths in self.trig_dict.items()
            ])
            if len(self.trig_dict) == 1:
                return trig[1:-1]
            else:
                return trig
        else:
            return '1'
    
    @property
    def cuts(self):
        if len (self.cut_dict) > 0:
            return logic.join_and(self.cut_dict.values())
        else:
            return '1'
        
    
    @property
    def trig_dict(self):
        return self._trig_dict
    @trig_dict.setter
    def trig_dict(self,value):
        if isinstance(value, dict):
            self._trig_dict = value
        else:
            raise ValueError('"trig_dict" must be a dict.')
    @property
    def cut_dict(self):
        return self._cut_dict
    @cut_dict.setter
    def cut_dict(self,value):
        if isinstance(value, dict):
            self._cut_dict = value
        elif isinstance(value,Iterable):
            self._cut_dict = {cut : cut for cut in value}
        elif isinstance(value,str):
            self._cut_dict = {value : value}
        else:
            raise ValueError('"trig_dict" must be a dict or Iterable.')
        
        
    def calc_bins(self):
        if self.range:
            if self.logx:
                bins = np.logspace(*np.log10(self.range),self.nbins+1,base=10)
            else:
                bins = np.linspace(*self.range,self.nbins+1)
            return bins.astype(np.double)
        else:
            return None
    
    @property
    def range(self):
        return self.xrange

    @property
    def weight(self):
        return self._weight

    @property
    def hist(self):
        return self._hist
    @hist.deleter
    def hist(self):
        del self._hist
    @property
    def plot_style(self):
        return self._plot_style
    
    def set_xlabel(self,label):
        self._xlabel = label
        self.hist.GetXaxis().SetTitle(label)
        self.pad.Update()
        
    def set_ylabel(self,label):
        self._ylabel = label
        self.hist.GetYaxis().SetTitle(label)
        self.pad.Update()

    
    
    def draw(self):
        pad = self.canvas.cd()
        pad.Clear()
        pad.Draw()
        self.hist.Draw(self.plot_style)
        pad.Update()
        Histogram.set_color(self.hist, self.color)
        Histogram.set_scale(self.hist, self.weight)
        Histogram.set_stats(self.hist,eff=self.efficiency)
        
        self.update()
        self._is_drawn = True
    
    @staticmethod
    def set_color(hist,color):
        hist.SetLineColor(color)
        stats = hist.FindObject('stats')
        # Esto falla por alguna razón
        stats.SetTextColor(color)
    
    @staticmethod
    def set_scale(hist,weight):
        hist.Scale(weight)
    
    @staticmethod
    def set_stats(hist,order=0,eff=0):
        stats = hist.FindObject('stats')
        stats.SetX1NDC(0.80-0.2*(order))
        stats.SetX2NDC(0.99-0.2*(order))
        stats.AddText(f'{"Efficiency":<10s}{eff*100:>6.2f}%')
        stats.DrawClone()      
    
    def draw_in(self,canvas,subplot=0,color=1,style='hist',weight=1,order=1):
        if self.hist:
            if not self._is_drawn: self.draw()
            
            pad = canvas.cd(subplot)
            pad.Draw()
            new_hist = self.hist.DrawClone(style)
            new_hist.Draw(style)
            pad.Update()
            Histogram.set_color(new_hist,color)
            Histogram.set_scale(new_hist,weight)
            Histogram.set_stats(new_hist,order=order,eff=self.efficiency)
            pad.Update()
            canvas.Update()
            canvas.Modified()
        else:
            print(f'WARNING: {self.alias} histogram has not been computed yet and thus will not be drawn in {canvas.alias}')
    



    def __delete__(self):
        print(f'{self.alias} está siendo eliminado...')
        self.canvas.Close()
        del self._hist


    
    def trig_eff_study(self):
        if not self._trig_eff:
            eff = {}
            if len(self.trig_dict) > 0:
                eff['global'] = self.get_eff(self.trigger)
                for trig_lvl, trig_paths in self.trig_dict.items():
                    eff[trig_lvl] = {}
                    eff[trig_lvl]['global'] = self.get_eff(logic.join_or(logic.trigger_parser(trig_lvl,trig_paths)))
                    for trig_path in trig_paths:
                        trig = logic.trigger_parser(trig_lvl,trig_path)
                        eff[trig_lvl][trig_path] = self.get_eff(trig)
            self._trig_eff = eff
        return self.trig_eff
    
    def cut_eff_study(self):
        if not self._cut_eff:
            eff = {}
            if len(self.cut_dict) > 0:
                eff['global'] = self.efficiency
                for alias, cut in self.cut_dict.items():
                    eff[alias] = self.get_eff(logic.join_and([self.trigger,cut]))

            self._cut_eff = eff
        return self.cut_eff
    
    @property
    def cut_eff(self):
        if not self._cut_eff: self.cut_eff_study()
        return self._cut_eff
    
    @property
    def trig_eff(self):
        if not self._trig_eff: self.trig_eff_study()
        return self._trig_eff
    
    def get_eff(self,selection):
        hist = rt.TH1D(
                    'h_aux',
                    self.title,
                    self.nbins,
                    self.bins
                )
        rt.gROOT.ProcessLine("gErrorIgnoreLevel = 6001;")
        self.tree.Draw(
            f'{self.branch} >> h_aux',
            selection,
            'goff'
        )
        eff = hist.Integral()/self.nentries
        del hist
        
        return eff
            
    @property
    def nentries(self):
        return self.tree.GetEntries()

    
    
    def eff_study(self,trigger = True, cut = True):
        eff_report = '\n'.join([
                '\n',
                '=================================================',
               f'EFFICIENCIES FOR:\t{self.title} ({self.alias})',
                '================================================='

        ])
        if trigger:
            trig_eff = self.trig_eff
            eff_report += '\n'.join([
                '\n',
                '-------------------------------------------------',
                'TRIGGER ({eff:6>3.2f} %)'.format(eff=trig_eff['global']*100),
                '-------------------------------------------------',
            ]) + '\n'
                        
            for trig_lvl, trig_paths in trig_eff.items():
                if trig_lvl == 'global': continue
                eff_report += '{trig_lvl} ({eff:6>3.2f} %)\n\n'.format(
                    trig_lvl = trig_lvl,
                    eff = trig_paths['global']*100
                )
                trig_template = ' - {trigger:<' + '{max_len}'.format(
                    max_len = max([len(path) for path in trig_paths.keys()])
                ) + 's}\t:  {eff:>6.2f} %\n'
                
                for trig_path, eff in trig_paths.items():
                    if trig_path == 'global': continue
                    eff_report += trig_template.format(
                        trigger = trig_path,
                        eff     = eff*100
                    )
                eff_report += '\n'
        if cut:
            cut_eff = self.cut_eff
            eff_report += '\n'.join([
                '\n',
                '-------------------------------------------------',
                'TRIGGER + SELECTION ({eff:6>3.2f} %)'.format(eff=cut_eff['global']*100),
                '-------------------------------------------------',
            ]) + '\n'
            
            cut_template = ' - {alias:<' + '{max_len}'.format(
                    max_len = max([len(path) for path in cut_eff.keys()])
                ) + 's}\t:  {eff:>6.2f} %\n'
                  
            for alias, eff in cut_eff.items():
                if alias == 'global': continue
                
                
                eff_report += cut_template.format(
                    alias = alias,
                    eff     = eff*100
                )
                eff_report += '\n'
            
        eff_report += '\n'.join([
                '-------------------------------------------------',
                'TOTAL ({eff:6>3.2f} %)'.format(eff=self.efficiency*100),
                '-------------------------------------------------',
            ])
        
        print(eff_report)
        return eff_report
                
    @property
    def efficiency(self):
        if self.hist:
            return self.hist.Integral()/self.nentries



if __name__ == '__main__':
    from llp.pyroot.plots.classes.Canvas import Canvas
    c = Canvas('test_canvas',
        logy = True
    )
    # print(c.alias)
    
    data_triggers = [
        'HLT_DoubleL2Mu23NoVtx_2Cha_v2',                    # Para Era B
        'HLT_DoubleL2Mu23NoVtx_2Cha_v3',                    # para Era C
        'HLT_DoubleL2Mu10NoVtx_2Cha_VetoL3Mu0DxyMax1cm_v1', # From aescalante@github/work/DDM/SimpleTTree/plots_example.py
        'HLT_DoubleL3Mu16_10NoVtx_DxyMin0p01cm_v1'          # From aescalante@github/work/DDM/SimpleTTree/plots_example.py
    ]
    
    cut_dict = {
        'OS'    :   '(dimPP_mu1_idx >= 0) && (dimPP_mu2_idx >= 0) && (patmu_charge[dimPP_mu1_idx] != patmu_charge[dimPP_mu2_idx])',
    }
    
    
    
    h1 = c.make_plot(Histogram,
        '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_BC__000_1e5.root',
        'SimpleNTupler/DDTree',
        'dimPP_mass',
        range = (0,200),
        logy = True,
        alias = 'h1',
        trigger = dict(trig_hlt_path = data_triggers),
        cut     = cut_dict
    )
    # c.add_plot(h1)
    h2 = Histogram(
        '/pnfs/ciemat.es/data/cms/store/user/martialc/displacedLeptons/202403_March24/DiMuons_NPND_BC/DiMuons_NPND_BC__1e5_2e5.root',
        'SimpleNTupler/DDTree',
        'dimPP_mass',
        logy = True,
        range = (0,200),
        alias = 'h2',
        trigger = dict(trig_hlt_path = data_triggers),
        cut     = cut_dict
        
    )
    c.add_plot(h2)
    
    h1.eff_study()
    h2.eff_study()
    
    c.save_to('/nfs/cms/martialc/Displaced2024/llp/sandbox/Hist/current')
    h1.save_to('/nfs/cms/martialc/Displaced2024/llp/sandbox/Hist/current_1')
    h2.save_to('/nfs/cms/martialc/Displaced2024/llp/sandbox/Hist/current_2')
    h2.canvas.Close()
    h1.canvas.Close()
    c.Close()
