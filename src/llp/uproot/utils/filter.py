import functools
import yaml
import numpy as np
import pandas as pd
import pathlib

from llp.utils.meta import defaults
from llp.utils.parser import str2float
from llp.utils.misc import filter_lookup

available_filters = {}



def Filter(
        filter_name = 'Filter'):
    def decorator(func):
        #do something before function call
        
        @functools.wraps(func)
        def wrapper(branch,*args,**kwargs):
            
            #do something and function call
            
            return func(branch, *args,**kwargs)

        # "wrapper" va a hacer las veces de la función
        
        available_filters[filter_name] = wrapper # añadimos la función al diccionario de filtros disponibles
        return wrapper
    
    return decorator


def calc_filters(tree, path):
    # Carga un filtro/filtros definidos en un archivo YAML y crea
    # un dataset booleano para seleccionar los datos.
    
    path = filter_lookup(path)
    
    with open(path,'r') as file:
        filters_cfg = yaml.safe_load(file)
    
    filters = {}
    
    for alias, filter_cfg in filters_cfg.items():
        # print(alias,filter_cfg)
        filter_type = filter_cfg['type']
        
        if filter_type not in available_filters.keys():
            print(f'WARNING: Filter type {filter_type} is not available for filter {alias}.')
            continue
        filters[alias] = calc_filter(tree,filter_cfg)

    return pd.DataFrame(filters)
    
    
def apply_filters(tree, path):
    filters = calc_filters(tree,path)
    return filters.product(axis='columns').astype(bool)




            




def calc_filter(tree, filter_cfg):
    filter_type = filter_cfg['type']
    filter_f = available_filters[filter_type]
    
    filter_args = [str2float(arg) for arg in filter_cfg['args']]
    filter_kwargs = {key : str2float(arg) for key, arg in filter_cfg['kwargs'].items()}

    branch = tree.arrays(filter_cfg['branch'],library='pd')
    
    return filter_f(branch,*filter_args,**filter_kwargs).astype(bool)

    
    
    
#---------------------------------------
# Definimos los filtros
#---------------------------------------
    

@Filter(filter_name = 'OppositeSigned')
def opposite_signed(branch):
    return branch.iloc[:,0]*branch.iloc[:,1] == -1

@Filter(filter_name = 'SameSigned')
def same_signed(branch):
    return branch.iloc[:,0]*branch.iloc[:,1] == 1


@Filter(filter_name = 'MinMax')
def minmax(branch : pd.Series, min, max):
    mask = branch.iloc[:,0].copy(deep=False).astype(bool)
    mask.values.fill(True)
    if min is not None:
        mask = mask & (min <= branch.iloc[:,0])
    if max is not None:
        mask = mask & (branch.iloc[:,0] <= max)
    return mask



if __name__ == '__main__':
    from llp.utils.rootIO import read_tree
    print(available_filters.keys())
    
    tree = read_tree(
        '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022B-ReReco-v2.root',
        tree = 'SimpleNTupler/DDTree'
    )
    
    print(apply_filters(
        tree,
        '/nfs/cms/martialc/Displaced2024/llp/src/llp/filters/test.yml'
    ))
