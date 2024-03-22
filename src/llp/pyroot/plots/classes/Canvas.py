import ROOT
import numpy as np
import pathlib
from typing import Iterable, Generator
from llp.pyroot.classes import Tree
from llp.pyroot.plots.classes.Plot import Plot
import llp.pyroot.utils.io as io
import pathlib


class Canvas(ROOT.TCanvas):
    _active_canvas      : 'int'                         = 0
    
    _fig_formats        : 'tuple[str]'                  = (".png", ".pdf", ".tex", ".C")
    def __init__(
        self,
        *args,
        logy = False,
        logx = False,
        **kwargs   
    ):
        Canvas._active_canvas     += 1
        
        # Inicializamos atributos
        self._plots              : 'dict[int,dict[str,Plot]]'    = {0 : {}}
        self._color_palette      : 'None | list[int]'            = None
        self._color_generators   : 'dict[int, Generator[int]]'   = {0 : None}
        self._logx = logx
        self._logy = logy
        
        if len(args) == 0:
            self._alias = f'c{self._active_canvas}'
        else:
            self._alias = args[0]
        
        super().__init__(self.alias,*args[1:],**kwargs)
        
        
        if logy: self.SetLogy()
        if logx: self.SetLogx()
        
        
        
        
    def subplots(self, nrows, ncols, xpad = 0.01, ypad =0.01):
        self.Divide(ncols,nrows,xpad,ypad,0)
    
    @property
    def active_canvas(self):
        return self._active_canvas
    
    @property
    def alias(self):
        return self._alias
    
    @property
    def plots(self):
        return self._plots
    
    def make_plot(self,cls : Plot,*args,subplot=0,**kwargs) -> Plot:
        plot = cls(*args,**kwargs)
        self.add_plot(plot,subplot)
        return plot
    
    def add_plot(self,plot : Plot, subplot=0,do_draw=True):
        plot_info = {
            'plot'  : plot,
            'color' : self.get_next_color(subplot),
            'order' : len(self.plots[subplot]),
            'style' : plot.plot_style
            
        }
        
        if plot_info['order'] > 0: plot_info['style'] += ' SAMES'
                
        
        #Añadimos
        self.plots[subplot][plot.alias] = plot_info
        if do_draw: self.draw_plot(plot,subplot)
        
        
        
    def draw_plot(self, plot : Plot,subplot=0):
        plot_info = self.get_plot(plot.alias,subplot)
        color = plot_info['color']
        style = plot_info['style']
        order = plot_info['order']
        
        #Pintamos
        plot.draw_in(self,subplot,color = color, style = style, order = order)
        plot.draw()
        
    def draw(self):
        self.Clear()
        for subplot, plots in self.plots.items():
            [self.draw_plot(plot['plot'],subplot) for alias, plot in plots.items()]
    
    
    
    @property
    def plot_order(self):
        return self._plot_order
    @property
    def color_palette(self):
        return self._color_palette
    @color_palette.setter
    def color_palette(self,color_palette):
        self._color_palette = color_palette
        
        # Actualizamos el color de todas las gŕaficas en el orden en el que fueron añadidas
        for subplot, plots in self.plots.items():
            self._color_generators[subplot] = self.color_generator()
            
            # Cambiar color y volver a pintar
            self.cd(subplot)
            for alias in self.plot_order[subplot]:
                plots[alias].set_color(self.get_next_color(subplot))
                
                # Actualizar canvas y pads (TODO: No sé si sería mejor fuera del bucle)
                ROOT.gPad.Update()
                self.Update()
            
        self.cd()        
    
    
    @property
    def color_generators(self):
        return self._color_generators
    
    def color_generator(self):
        color_index = 1
        if self.color_palette is None:
            while True:
                yield color_index
                color_index += 1
        else:
            for color_index in self.color_palette:
                yield self.color_palette[color_index-1]

    def get_next_color(self,subplot=0):
        self.check_color_generator(subplot)
        return next(self.color_generators[subplot])
    
    def check_color_generator(self,subplot):
        if self.color_generators[subplot] is None:
            self._color_generators[subplot] = self.color_generator()
        return
    
    @property
    def fig_formats(self):
        return self._fig_formats
    
    def save_to(self,path):
        # self.draw()
        if isinstance(path,str):
            path = pathlib.Path(path)
        elif isinstance(path,pathlib.Path):
            pass
        else:
            raise TypeError(f'path type is incorrect: only str and pathlib.Path are allowed and an object of type {type(path)} was provided.')
        
        
        for format in self.fig_formats:
            self.SaveAs(str(path.with_suffix(format)))
    
    def get_subplots(self,subplot):
        return self.plots.get(subplot,{})
    
    def get_plot(self,alias,subplot=0):
        return self.plots[subplot][alias]
