import os
import sys
import numpy
import glob
import time
from datetime import datetime
import multiprocessing as mp
import argparse
import subprocess

from tqdm import tqdm
from ROOT import *

import compare as cp
import efficiency as ef
import utils 

if __name__ == '__main__':
    start_time = time.time()
    gROOT.ProcessLine("gErrorIgnoreLevel = kFatal;")

    parser = argparse.ArgumentParser(description="""
        Comparing TwinMuxOut between unpacked data and emulated one.
        Default outdir = ./output
        Default dataset = Run2018D/SingleMuon/RAW-RECO/ZMu-PromptReco-v2
    """)
 
    parser.add_argument('-i', '--input', required=False, type=str, 
            default='/data/users/seohyun/ntuple/TwinMux/SingleMuon/', 
            help='Set input location')
    parser.add_argument('-o', '--output', required=False, type=str, default='output', help='Set output location')
    parser.add_argument('-f', '--full', required=False, type=utils.str2bool, default=False, help='Run full 2018D dataset')
    parser.add_argument('-c', '--compare', required=False, type=utils.str2bool, default=False, help='Compare unpacked data and emulator')
    parser.add_argument('-e', '--efficiency', required=False, type=utils.str2bool, default=False, help='Calculate RPC efficiency')

    args = parser.parse_args()
    if args.compare == False and args.efficiency == False:
        print "Run full analysis"
        args.compare = True
        args.efficiency = True
    
    outDir = args.output

    if not os.path.exists(outDir):
        os.makedirs(outDir)
    if not os.path.exists(outDir+'/pdf'):
        os.makedirs(outDir+'/pdf')

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

    if args.full:
        list_data= []
        list_emul = []
        for index, item_dir in enumerate(list_dataDir):
            if index > 1: continue
            print item_dir
            for item in os.listdir(item_dir):
                emulFile = item[:item.rfind('_')]+'_Emulator_'+item[:-5].split('_')[-1]+'.root' 
                if not os.path.exists(list_emulDir[index]+'/'+emulFile):
                    print list_emulDir[index]+'/'+emulFile + "does not exist"
                list_data.append(item)
                list_emul.append(emulFile)
           
            if args.compare:
                pool = mp.Pool(processes=50)
                with tqdm(total=len(list_data)) as pbar:
                    for _ in pool.imap_unordered(cp.compareDataEmul, [utils.argParser(item_dir, list_emulDir[index], item, outDir, True) for item in list_data]):
                        pbar.update()
                pool.close()
                pool.join()
            # NEED TO FIX
            if args.efficiency:
                pool = mp.Pool(processes=50)
                with tqdm(total=len(list_emul)) as pbar:
                    for _ in pool.imap_unordered(ef.calculateEfficiency, [utils.argParser(list_emulDir[index], item, outDir, True) for item in list_emul]):
                        pbar.update()
                pool.close()
                pool.join()
       
        if args.compare:
            cmd = ['hadd', str(outDir)+'/DTDPGNtuple_10_3_3_ZMuSkim_2018D_Comparison.root'] + glob.glob(outDir+'/comparison/*')
            subprocess.call(cmd)
        if args.efficiency:
            cmd = ['hadd', str(outDir)+'/DTDPGNtuple_10_3_3_ZMuSkim_2018D_Efficiency.root'] + glob.glob(outDir+'/efficiency/*')
            subprocess.call(cmd)
    else:
        if args.compare:
            cp.compareDataEmul(utils.argParser('./', './', 'DTDPGNtuple_10_3_3_ZMuSkim_2018D.root', outDir, False))
        if args.efficiency:
            ef.calculateEfficiency(utils.argParser('./', 'DTDPGNtuple_10_3_3_ZMuSkim_2018D_Emulator.root',outDir, False))
        
    if args.compare:
        cp.drawHist(outDir+'/DTDPGNtuple_10_3_3_ZMuSkim_2018D_Comparison.root', outDir+'/pdf')
    
    if args.efficiency and args.full:
        f_eff = TFile.Open(str(outDir)+'/DTDPGNtuple_10_3_3_ZMuSkim_2018D_Efficiency.root')
        h_eff = f_eff.Get('h_Efficiency')
        effInclusive = float(h_eff.GetBinContent(2))/float(h_eff.GetBinContent(1))
        effRPConly = float(h_eff.GetBinContent(4))/float(h_eff.GetBinContent(3))
        print '\n==== Inclusive ===='
        print 'Nume: '+str(h_eff.GetBinContent(2))+', Deno: '+str(h_eff.GetBinContent(1))+\
                ', Efficiency: '+str(effInclusive)
        print '==== RPC only ===='
        print 'Nume: '+str(h_eff.GetBinContent(4))+', Deno: '+str(h_eff.GetBinContent(3))+\
                ', Efficiency: '+str(effRPConly)
    
    print "Total running time: %s" % (time.time() - start_time)
