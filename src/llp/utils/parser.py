def str2float(value):
    from numpy import pi, inf
    
    if isinstance(value, str):
        if 'pi' in value:
            if len(value.split('pi')[0]) > 0 and '*' not in value:
                value = value.replace('pi','*pi')
        elif 'inf' in value:
            from numpy import inf
        elif 'None' == value:
            return None
        value = eval(value)
        
    return float(value)