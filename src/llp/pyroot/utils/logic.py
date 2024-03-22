from typing import Iterable
def join_and(cutstring_list):
    return '(' + ') && ('.join(cutstring_list) + ')'

def join_or(cutstring_list):
    return '(' + ') || ('.join(cutstring_list) + ')'

def trigger_parser(trig_lvl,trig_path):
    if isinstance(trig_path, str):
        return f'{trig_lvl} == "{trig_path}"'
    elif isinstance(trig_path,Iterable):
        return [f'{trig_lvl} == "{trig_path}"' for trig_path in trig_path]
    else:
        raise TypeError(f'trig_path type {type(trig_path)} is not str or Iterable.')