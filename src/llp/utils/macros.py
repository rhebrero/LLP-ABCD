def load_macros():
    load_macro('*')

def load_macro(macro_name = '*'):
    import pathlib, inspect
    import ROOT as rt
    from llp.utils.paths import macros_directory
    for macro in macros_directory.glob(f'**/{macro_name}.C'):
        if rt.gROOT.LoadMacro(str(macro)):
            raise OSError(f'Unable to load: {macro}')
    return True