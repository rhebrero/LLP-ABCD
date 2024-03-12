def confirmation(msg):
    yes = 'yes'
    no = 'no'
    
    while True:
        user_input = input(f'\n{msg}\t')
        
        if user_input in [yes.lower(),yes.upper(),yes[0].upper(),yes[0].lower(),'']:
            return True
        elif user_input in [no.lower(),no.upper(),no[0].upper(),no[0].lower()]:
            return False
        else:
            print('Value was not recognized. Use yes(y) or no(n).')
            continue