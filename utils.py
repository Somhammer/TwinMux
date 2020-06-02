import sys
from tqdm import tqdm

def printProgress(iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
    nEvent = str(iteration) + '/' + str(total)
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100*(iteration/float(total)))
    filledLength = int(round(barLength * iteration/float(total)))
    bar = '#'*filledLength + '-'*(barLength-filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s %s' % (prefix, bar, percent, '%', suffix, nEvent)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1', 'True'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0', 'False'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected')

def argParser(*args):
    arglist = [item for item in args]
    return arglist

def setChamberName():
    global nStation
    global nWheel
    global nSector
    global nBX
    global name_RPCbit
    global name_Wheel
    global name_Sector
    global name_BX

    nStation = 4 # 1 2 3 4
    nWheel = 5 # -2 -1 0 1 2
    nSector = 12 # 1 ~ 12
    nBX = 9 # -4 ~  4 
    name_RPCbit = ['inclusive', 'RPCbit0', 'RPCbit1', 'RPCbit2']
    name_Wheel = ['W-2', 'W-1', 'W0', 'W+1', 'W+2']
    name_Sector = [
        'S1', 'S2', 'S3', 'S4', 'S5', 'S6',
        'S7', 'S8', 'S9', 'S10', 'S11', 'S12']# We does not focus out and in in sector.
    name_BX = ['BX-4', 'BX-3', 'BX-2', 'BX-1', 'BX0', 'BX1', 'BX2', 'BX3', 'BX4']


