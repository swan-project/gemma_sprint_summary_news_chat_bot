def set_config(mode):
    global ENV_MODE
    if mode == 'develop':
        ENV_MODE = 'develop'   
    elif mode == 'product':
        ENV_MODE = 'product'
    else:
        raise ValueError('Invalid mode')
    

def getENVMode():
    return ENV_MODE