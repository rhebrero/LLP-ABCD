import pathlib, inspect
here = pathlib.Path(inspect.getfile(inspect.currentframe())).parent

def get_src():
    where_src = [i for i, part in enumerate(here.parts) if part == 'src']
    return pathlib.Path('').joinpath(*here.parts[:where_src[0]])

parent_directory = get_src()
data_directory   = parent_directory / pathlib.Path('data')
config_directory = parent_directory / pathlib.Path('cfg')
macros_directory = parent_directory / pathlib.Path('macros')

def is_valid(path):
    if isinstance(path,str):
        path = pathlib.Path(path)
    elif isinstance(path, pathlib.Path):
        pass
    else:
        raise TypeError(f"Type of path is not valid. Expected str or pathlib.Path, not {type(path)}")
    
    if path.exists():
        return True
    else:
        try:
            print(f'Trying to touch {path}')
            path.touch()
            path.unlink()
            return True
        except OSError:
            print(f"Can't touch {path}")
            return False
            

def check_root_file(path):
    path = pathlib.Path(path)
    if path.suffix == '.root': pass
    elif path.suffix == '': path = path.with_suffix('.root')
        
    if is_valid(data_directory / path):
        return data_directory / path
    elif is_valid(path):
        return path
    else:
        raise ValueError(f"Can't find .root file with name {path}!")







if __name__ == '__main__':
    print(get_src())