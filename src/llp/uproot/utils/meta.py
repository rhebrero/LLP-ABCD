import pathlib

parent = pathlib.Path('/nfs/cms/martialc/Displaced2024/llp')

#======================================================================================
filter_default  = pathlib.Path('cfg/filters')
data_default    = pathlib.Path('cfg/data')

#======================================================================================

defaults = dict(
    filter  = pathlib.Path('cfg/filters'),
    data    = pathlib.Path('cfg/data')
)

defaults = {key : parent.joinpath(path) for key, path in defaults.items()}

if __name__ == '__main__':
    print(parent)
    print(defaults)