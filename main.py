import os
import sys
import numpy
import glob
import time
from datetime import datetime
import multiprocessing as mp
import argparse
import subprocess

from ROOT import *

import compare as cp
import utils 

if __name__ == '__main__':
    start_time = time.time()

    parser = argparse.ArgumentParser(description="""
        Comparing TwinMuxOut between unpacked data and emulated one.
        Default outdir = ./output
        Default dataset = Run2018D/SingleMuon/RAW-RECO/ZMu-PromptReco-v2
    """)
    
    parser.add_argument('-t', '--test', required=False, type=utils.str2bool, default=False, help='Test')
    parser.add_argument('-i', '--input', required=False, type=str, 
            default='/data/users/seohyun/ntuple/TwinMux/SingleMuon/', 
            help='Set input location')
    parser.add_argument('-o', '--output', required=False, type=str, default='output', help='Set output location')
    args = parser.parse_args()
    outDir = args.output

    if not os.path.exists(outDir):
        os.makedirs(outDir)
    if not os.path.exists('./pdf'):
        os.makedirs('./pdf')

    list_dataDir = []
    list_emulDir = []
    for (path, dir, files) in os.walk(args.input):
        depth = path.count(os.path.sep) - args.input.count(os.path.sep)
        if depth < 2: continue
        if 'Emulator' in path:
            list_emulDir.append(path)
        else:
            list_dataDir.append(path)

    print list_dataDir
    print list_emulDir
    if args.test:
        tmp1 = list_dataDir[0]
        tmp2 = list_emulDir[0]
        tmp3 = 'DTDPGNtuple_10_3_3_ZMuSkim_2018D_53.root'
        cp.makeHist(cp.argParser(tmp1, tmp2, tmp3, outDir))
        
        quit() 
     
    list_input = []
    for index, item_dir in enumerate(list_dataDir):
        for item in os.listdir(item_dir):
            emulFile = item[:item.rfind('_')]+'_Emulator_'+item[:-5].split('_')[-1]+'.root' 
            if not os.path.exists(list_emulDir[index]+'/'+emulFile):
                print list_emulDir[index]+'/'+emulFile + "does not exist"
            list_input.append(item)
        pool = mp.Pool(processes=50)
        pool.map(cp.makeHist, [cp.argParser(item_dir, list_emulDir[index], item, outDir) for item in list_input])
        pool.close()
        pool.join()
    
    cmd = ['hadd', str(outDir)+'/DTDPGNtuple_10_3_3_ZMuSkim_2018D_Comparison.root'] + glob.glob(outDir+'/*')
    subprocess.call(cmd)
    
    cp.drawHist(outDir+'/DTDPGNtuple_10_3_3_ZMuSkim_2018D_Comparison.root', outDir)
    
    print "Total running time: %s" % (time.time() - start_time)
