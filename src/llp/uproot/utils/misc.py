import pathlib

from llp.utils.meta import defaults

def cfg_lookup(path, default = None):
    path = pathlib.Path(path)
    if path.exists():
        return path
    
    elif (default is not None) & (path.suffix in ['','.yaml','.yml']):
        # Si no se encuentra, buscar en la carpeta por defecto si se ha definido.
        cfg_list = list(default.glob('*.yml'))
        for cfg_i in cfg_list:
            if path.stem == cfg_i.stem:
                print(cfg_i)
                return cfg_i
    else:
        raise NameError(f'El archivo de configuración no existe en {path}.')

def filter_lookup(path):
    return cfg_lookup(path, default=defaults['filter'])

def data_lookup(path):
    return cfg_lookup(path, default=defaults['data'])