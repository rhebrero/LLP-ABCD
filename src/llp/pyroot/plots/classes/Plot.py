import ROOT as rt
import numpy as np
import pathlib
from collections.abc import Iterable
from llp.pyroot.classes import Tree
import llp.pyroot.utils.io as io
import pathlib

class Plot(object):
    _orphan_hist    = 0
    _default_alias  = 'p'
    
    def __init__(self,
            *args                       ,
            alias       = None          ,
            plot_style  = 'p'  ,
            logx        = False         ,
            logy        = False         ,
            title       = None          ,
            color       = 1             ,
            **kwargs
        ):
        
        # inicializamos atributos
        self._color          = color
        self._title          = 'Plot'
        self._src_canvas     = None
        self._target_canvas  = {}
        self._alias          = 'p'
        self._has_default_alias  = True
        self._xrange = [0,1]
        self._yrange = [0,1]
        self._logx   = False
        self._logy   = False
        self._xlabel = 'Variable'
        self._ylabel = 'Events'
        self._plot_style = 'p'
        self._is_drawn = False
        
        

        
        
        from llp.pyroot.plots.classes.Canvas import Canvas
        # TCanvas initialization # Verificado
        self._src_canvas    = Canvas(logx=logx,logy=logy)
        self.alias          = alias
        
        if title: self._title = title
        self._plot_style = plot_style
        
        self._src_canvas.add_plot(self,do_draw=False)
        return

    @property
    def title(self):
        self._title
    @property
    def pad(self):
        return self.canvas.cd()
    @property
    def plot_style(self):
        return self._plot_style
        
    @property
    def default_alias(self):
        return self._default_alias
        
    def get_default_alias(self,canvas,subplot=0):
        plots = canvas.get_subplots(subplot).values()
        n_default = sum([(plot.has_default_alias) & (plot.__class__.__name__ == self.__class__.__name__) for plot in plots])
        alias = f'{self.default_alias}{n_default + 1}' # This will be the n+1 default plot
        
        
        if subplot > 0:
            alias = '_'.join([canvas.alias,subplot,alias])
        else:
            alias = '_'.join([canvas.alias,alias])
            
        return alias
        
    @property
    def alias(self):
        if not self._alias: self.alias = self._alias
        return self._alias
    @alias.setter
    def alias(self,alias):
        if not alias:
            self._alias = self.get_default_alias(self.canvas)
        else:
            self._alias = alias
            self._has_default_alias = False

    @property
    def color(self):
        return self._color
    @property
    def hist(self):
        self._hist
    
    
    
    @property
    def has_default_alias(self):
        return self._has_default_alias
    
    def set_color(self,color):
        self._color = color
        return
    
    @property
    def canvas(self):
        return self._src_canvas

    @property
    def src(self):
        return self._src_canvas

    
    @property
    def xrange(self):
        return self._xrange
    @property
    def yrange(self):
        return self._yrange
    @property
    def xmin(self):
        return self.xrange[0]
    @property
    def xmax(self):
        return self.xrange[1]
    @property
    def ymin(self):
        return self.yrange[0]
    @property
    def ymax(self):
        return self.yrange[1]
    @property
    def logx(self):
        return self.canvas._logx
    @property
    def logy(self):
        return self.canvas._logy
    @property
    def xlabel(self):
        return self._xlabel
    @property
    def ylabel(self):
        return self._ylabel
    
    
    def add_to_canvas(self,canvas,subplot=0):
        
        if not self.get_canvas(canvas):
            self._target_canvas[canvas] = []
        
        self.get_canvas(canvas).append(subplot)
        canvas.add_plot(self,subplot)

            
    def get_canvas(self,alias) -> list:
        return self._target_canvas.get(alias,None)
    
      
    def __str__(self):
        string = f'{self.__class__.__name__}({self.alias}) @ {self.canvas.alias}'

        return string
                
    def __repr__(self):
        return str(self)
    
    def draw(self):
        self._is_drawn = True
        return
    
    @property
    def pad(self):
        if self.canvas: return self.canvas.cd()
        else: return None
    @property
    def target_canvas(self):
        return self._target_canvas
    def update(self):
        pad = self.canvas.cd()
        pad.Update()
        self.canvas.Update()
        # if self._canvas_target
    
    @classmethod
    def from_canvas(cls,*args,**kwargs):
        return cls(*args, **kwargs)

    def save_to(self,path):
        self.canvas.save_to(path)