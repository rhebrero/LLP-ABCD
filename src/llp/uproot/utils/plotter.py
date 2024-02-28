import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
from collections.abc import Iterable
from fractions import Fraction
from typing import List

def plot_hist_mpl(
        data : pd.Series,
        bins=100,
        range = None,
        histtype='step',
        do_clip = True,
        label = None,
        ax : plt.Axes = None,
        **kwargs
    ):
    if ax is None: fig, ax = plt.subplots(1,1)
    else:
        fig = ax.figure
    
    if range is None: range = [data.min(skipna=True),data.max(skipna=True)]
    elif range[0] is None: range[0] = data.min(skipna=True)
    elif range[1] is None: range[1] = data.max(skipna=True)
    
    
    try:
        assert range[0] < range[1]
    except AssertionError:
        raise RuntimeError(f'No hay ninguna entrada en el rango seleccionado para {data.name}.')
        
    if isinstance(range, Iterable):
        try:
            assert len(range) == 2
        except AssertionError:
            raise ValueError(f'La variable "range" no tiene la longitud correcta. Esperaba 2 elementos y tiene {len(range)}')    
        
    if do_clip: data = np.clip(data,*range)
    
    weights = np.ones_like(data)
    if kwargs['density']: weights = weights/data.count()
    
    hist = ax.hist(
        data,
        bins = bins,
        range = range,
        histtype = histtype,
        label = label,
        weights = weights
    )
    
    # ax.set_xlim(*range)

    if 'angular' in kwargs.keys():
        if kwargs['angular']:
            ax.set_xticks(np.linspace(0,np.pi,len(ax.get_xticks())))
            ax.get_xaxis().set_major_formatter(lambda x, pos: radian_formatter(x))
            ax.format_coord = lambda x,y: f'x = {x/np.pi:.4f}pi, y = {y:.4f}'

    
    if 'log' in kwargs.keys():
        if kwargs['log']: ax.set_yscale('log')
        
    return fig, ax, hist
    
    
    
    
def plot_hist(*args, library='mpl', **kwargs):
    libraries = dict(
        mpl = plot_hist_mpl
    )
    
    if library in libraries:
        return libraries[library](*args,**kwargs)
    else:
        raise ValueError(f'La librería seleccionada no es válida, escoge una de entre: {libraries}.')


def radian_formatter(value):
    # print(label.get_text())
    # value = float(label.get_text())
    if value == 0:
        return str(0)
    else:
        fract = Fraction(value/np.pi).limit_denominator(20)
        if fract.numerator == 1:
            num = ''
        else:
            num = str(fract.numerator)
        if fract.denominator == 1:
            return f'${num}' + r'\pi$'
        else:
            den = str(fract.denominator)
            return r'$\frac{' + f'{num}' + r'\pi}{' + f'{den}'+ r'}$'
        

def plot_significance(*args, library='mpl', **kwargs):
    libraries = dict(
        mpl = plot_significance_mpl
    )
    
    if library in libraries:
        return libraries[library](*args,**kwargs)
    else:
        raise ValueError(f'La librería seleccionada no es válida, escoge una de entre: {libraries}.')

def plot_significance_mpl(data_num, data_den, bins, ax=None):
    if ax is None: fig, ax = plt.subplots(1,1)
    else:
        fig = ax.figure
    
    sig = data_num/data_den
    dsig = sig*np.sqrt(1/data_num+1/data_den)
    
    bin_mid = (bins[1:]+bins[:-1])/2
    bin_width = bins[1]-bins[0]
    
    loglim = np.ceil(np.abs([np.log10(sig[np.isfinite(sig)].min()),np.log10(sig[np.isfinite(sig)].max())]).max()) # Máximo exponente de 10 redondeado hacia arriba
    
    if not np.isfinite(loglim): loglim = 3
        
    
    ax.set_ylim(np.power(10,-loglim),np.power(10,loglim))
    
    ax.axhline(1,linestyle='dashed',color='k')
    
    plot = ax.errorbar(
        bin_mid,
        sig,
        # xerr = bin_width,
        yerr = dsig,
        elinewidth=1,
        capsize=1.5,
        fmt='_',
        linestyle = 'none',
        # lolims=(sig-dsig) < ax.get_ylim()[0],
        # uplims=(sig+dsig) > ax.get_ylim()[1],
        color = 'k'
    )
    
    
    ax.set_yscale('log')
    return fig, ax, plot


def plot_hist_stacked(*args,library='mpl',**kwargs):
    libraries = dict(
        mpl = plot_hist_stacked_mpl
    )
    
    if library in libraries:
        return libraries[library](*args,**kwargs)
    else:
        raise ValueError(f'La librería seleccionada no es válida, escoge una de entre: {libraries}.')

def plot_hist_stacked_mpl(
        data : List[pd.Series],
        bins=100,
        range = None,
        histtype='stepfilled',
        do_clip = True,
        label = None,
        ax : plt.Axes = None,
        **kwargs
    ):
    if ax is None: fig, ax = plt.subplots(1,1)
    else:
        fig = ax.figure
    
    glob_min = min([data_i.min(skipna=True) for data_i in data])
    glob_max = max([data_i.max(skipna=True) for data_i in data])
    
    if range is None: range = [glob_min,glob_max]
    elif range[0] is None: range[0] = glob_min
    elif range[1] is None: range[1] = glob_max
    
    
    
    try:
        assert range[0] < range[1]
    except AssertionError:
        raise RuntimeError(f'No hay ninguna entrada en el rango seleccionado para los datos.')
        
    if isinstance(range, Iterable):
        try:
            assert len(range) == 2
        except AssertionError:
            raise ValueError(f'La variable "range" no tiene la longitud correcta. Esperaba 2 elementos y tiene {len(range)}')    
        
    if do_clip: data = [np.clip(data_i,*range) for data_i in data]
    
    weights = [np.ones_like(data_i) for data_i in data]
    if kwargs['density']: weights = weights/sum([data_i.count() for data_i in data])
    
    hist = ax.hist(
        data,
        bins = bins,
        range = range,
        histtype = histtype,
        label = label,
        weights = weights,
        stacked=True
    )
    
    # ax.set_xlim(*range)

    if 'angular' in kwargs.keys():
        if kwargs['angular']:
            ax.set_xticks(np.linspace(0,np.pi,len(ax.get_xticks())))
            ax.get_xaxis().set_major_formatter(lambda x, pos: radian_formatter(x))
            ax.format_coord = lambda x,y: f'x = {x/np.pi:.4f}pi, y = {y:.4f}'

    
    if 'log' in kwargs.keys():
        if kwargs['log']: ax.set_yscale('log')
    
    
    return fig, ax, hist
