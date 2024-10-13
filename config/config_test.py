import yaml as ym
import pdb
import os
# Contruction of caracteristic dics I use in the scripts for each kind of file from the config files

def load_config(filename):
    with open(filename, 'r') as file:
        return ym.safe_load(file)
    
# dicts = load_config('files_dicts.yaml')
# paths = load_config('files_paths.yaml')

def get_config():
    
    config_path = os.path.join(os.path.dirname(__file__), 'files_paths.yaml')
    return load_config(config_path)


def get_dict(file_type, 
             kind, 
             all=False, 
             ctau_signal=None,
             mass_signal=None,
             mass_i=None, 
             mass_f=None
             ):
    
    """
    Given a process type returns the corresponding dictionary needed for the scripts

    Args:
        type: the file type (data, signal or background)

        kind: if bkg type specify the bkg process, if signal specify STop{Mass} or SMuon{Mass}, 
        if data specify which era (eg. data_eraB). Only included eraB (.11fb-1) at the moment tho 

        mass_i/f: if not "all", specify the mass range of bkg file or signal mass
    """

    if file_type not in ['data', 'signal', 'background']:
        raise ValueError('File type not valid for getting the dict')

    config = get_config()
    items = config[kind]

    if file_type == 'signal':
        if not ctau_signal or not mass_signal: 
            raise ValueError('Specify signal lifetime')
        if all: 
            raise ValueError('Selec just one signal file')
        
        path = f'{kind}ToMuGravitino_{mass_signal}_{ctau_signal}.root' if kind == 'SMuon' else f'{kind}ToMuB{mass_signal}_{ctau_signal}.root'

        if not all:

            return {
                'file':   config[f'Folder{kind}Signal'] + path,
                'mass':   mass_signal,
                'type':   file_type,
                'susy':   kind,
                'label':  f'{kind}_{mass_signal}_{ctau_signal}'
            }
            
            

    elif file_type == 'background':
        # should include an all_bkg option
        if all:
            return [
                {
                    'file':    config['BackgroundFolder'] + item['path'], 
                    'label':   item['name'],
                    'type':    file_type,  
                    'kind':    kind,  
                    'x_sec':   item['x_sec'], 
                    'events':  item['events']
                }
                for item in items 
            ]
            
        
        else: 
            if not mass_f or not mass_i: 
                raise ValueError('Specify mass range for bkg file')

            item = next((item for item in items if f'{mass_i}to{mass_f}' in item['name']), None)

            if not item: 
                raise ValueError('Invalid mass range')
            
            return {
                    'file':    config['BackgroundFolder'] + item['path'], 
                    'label':   item['name'],
                    'type':    file_type,  
                    'kind':    kind,  
                    'x_sec':   item['x_sec'], 
                    'events':  item['events']
                }
            
    elif file_type=='data':
        # pdb.set_trace()
        return {
            'file':      config['DataFolder'] + items['path'],
            'type':      file_type,  
            'kind':      kind,  
            'friend':    items['friend'],
            'data_lumi': items['lumi']
        }
        # Not "all" option for data at the moment

def GetGenSig(mass, ctau, all=True):
    conf = get_config()
    path = conf['FolderGenSmuonSig'] + conf['GenSmuonSig'][str(mass)][str(ctau)]

    if all:
        path_list = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and 'log' not in f]

    else:
        path_list = [path]

    return path_list

# pdb.set_trace()
def main():
    pdb.set_trace()
    try:
        result_dict = get_dict('background', 'DYto2Mu200k',  mass_i=50, mass_f = 120)
        pdb.set_trace()
        print(result_dict)

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
