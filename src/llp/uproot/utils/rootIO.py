import uproot
import pathlib
from collections.abc import Iterable
from typing import Dict
import pandas as pd
import yaml
import dask.dataframe as dd
import dask.array as da

from llp.utils.misc import data_lookup


def read_root(
        path,    #: str | pathlib.Path    , 
        branch  : str                   = [],
        tree    : str                   = None,
        library : str                   = 'pd'
    ):# -> pd.DataFrame | pd.Series
    
    if isinstance(path, str):
        branch_list = [branch]
    elif isinstance(branch, Iterable):
        branch_list = branch
    else:
        raise TypeError('No se ha reconocido el tipo de "branch".')
    
    path = data_lookup(path)
    
    try:
        assert isinstance(path,pathlib.Path)
    except AssertionError:
        path = pathlib.Path(path)

    if path.suffix in ['.yml','.yaml']:
        data_list = read_data_cfg(path).path.to_list()
    
    elif path.suffix == '.root':
        data_list = [path]
    
    else:
        raise ValueError('El tipo de archivo no se puede identificar')
        
    if isinstance(branch, str):
        branch_list = [branch]
    elif isinstance(branch, Iterable):
        branch_list = branch
    else:
        raise TypeError('No se ha reconocido el tipo de "branch".')
    
    
    # return read_tree(path, tree = tree).arrays(branch_list, library=library)
    if library == 'dask':
        ddict : Dict[str, da.Array] = uproot.dask(
            [':'.join([data,tree]) for data in data_list],
            filter_name = branch_list,
            step_size=10000,
            open_files=True,
            library='np'
        )
        # for key, val in ddict.items():
        #     print(key,val)
        
        cols = list(ddict.keys())
        darray = da.stack(ddict.values()).transpose()
        ddf : dd.DataFrame = dd.from_dask_array(darray,cols)
        return ddf

    else:
        return uproot.concatenate(
                [':'.join([data,tree]) for data in data_list],
                filter_name = branch_list,
                library=library
            )




def read_data_cfg(
        path,    #: str | pathlib.Path    ,
        astype = 'pd'
    ):
    path = data_lookup(path)
    
    with open(path,'r') as file:
        configs = yaml.safe_load(file)
    
    paths = {}
    for alias, cfg in configs.items():
        try:
            assert alias not in paths.keys()
        except AssertionError:
            raise ValueError(f'Hay dos configuraciones con el mismo alias: "{alias}".')
        
        if cfg['type'] == 'root':
            paths[alias] = cfg
            
        elif cfg['type'] == 'join':
            for sub_cfg in cfg['path']:
                paths.update(read_data_cfg(sub_cfg,astype='dict'))
                
        else:
            raise TypeError(f'No se ha reconocido el typo de la configuración "{alias}"')
    if astype == 'dict':
        return paths
    elif astype == 'pd':
        return pd.DataFrame(paths).transpose()
    else:
        raise ValueError(f'No se reconoce el valor introducido para "astype": {astype}')
    

def time_read_branch_from_cfg(cfg, tree, branch,**kwargs):
    t_i = time.time()
    df = read_root(cfg,tree = tree, branch = branch,**kwargs)
    t_f = time.time()
    print(f'\tLa lectura ha tardado {t_f-t_i:.1f}s para {cfg}')
    return df



if __name__ == '__main__':
    import time
    print(read_data_cfg('test'))
    df = time_read_branch_from_cfg(
        'test.yml',
        branch = 'dim_mass',
        tree = 'SimpleNTupler/DDTree',
        library = 'pd'
    )
    print(df)