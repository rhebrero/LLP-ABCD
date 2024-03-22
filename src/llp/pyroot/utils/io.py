from llp.utils.paths import is_valid
from collections.abc import Iterable
import pathlib
import ROOT

def get_tree(
        file_path : 'str | pathlib.Path | Iterable[str] | Iterable[pathlib.Path]',
        tree_path : 'str'
    ) -> ROOT.TChain:
    
    if isinstance(file_path, (str, pathlib.Path)):
        if is_valid(str(file_path)):
            file_list = [str(file_path)]
        else:
            raise IOError(f'The path {file_path} does not exist!')
        
    elif isinstance(file_path, Iterable):
        file_list = []
        for file in file_path:
            if is_valid(file):
                file_list.append(str(file))
            else:
                print(f'WARNING: the path {file} does not exist and so will be omitted!')
                continue
        if len(file_list) == 0: raise IOError('None of the given paths exist!')
        
    else:
        raise ValueError(f'file_path must be path or list of paths, {type(file_path)} given instead')
    
    tree = ROOT.TChain(tree_path)
    [tree.Add(file) for file in file_list]
    return tree