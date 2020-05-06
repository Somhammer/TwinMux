import os
import sys
import numpy

import math
from ROOT import *

import tdrstyle
import utils

def calculateEfficiency(args):#(emulDir, inFile, outDir):
    inputDir = args[0]
    inFile = args[1]
    outDir = args[2]
    multiProcess = args[3]
    print "Start "+str(inFile)
    if not os.path.exists(outDir+'/efficiency'):
        os.makedirs(outDir+'/efficiency')
    f_out = TFile.Open(outDir+'/efficiency/'+inFile, 'recreate')
    
    DTTREE = TChain('dtNtupleProducer/DTTREE')
    DTTREE.Add(inputDir+'/'+inFile)
    f_out.cd()
    
    h_SegVsTwinMux_dPhi = TH1D('h_SegVsTwinMux_dPhi', 'Segment vs TwinMux dPhi', 100, -2000.0, 2000.0)
    h_SegVsTwinMux_dPhi.GetXaxis().SetTitle('#Delta phi_{Seg,TwinMux}')
    h_SegVsTwinMux_dPhi.GetYaxis().SetTitle('Entries')
    h_SegVsTwinMux_dPhi.Sumw2()

    h_Efficiency = TH1D('h_Efficiency', 'The efficiency of trigger primitives', 2, 0, 2)
    h_Efficiency.GetXaxis().SetTitle("")
    h_Efficiency.GetXaxis().SetBinLabel(1,'inclusive')
    h_Efficiency.GetXaxis().SetBinLabel(2,'RPC only')
    h_Efficiency.GetXaxis().SetTitle("Efficiency")
    h_Efficiency.SetMaximum(1.2)
    h_Efficiency.SetMinimum(0.0)

    coneSize = 1600
    denoInclusive = 0 
    numeInclusive = 0
    denoRPConly = 0
    numeRPConly = 0
    for ievent in xrange(DTTREE.GetEntries()):
        if not multiProcess:
            utils.printProgress(ievent, DTTREE.GetEntries(), 'Progress: ', 'Complete', 1, 25)
        DTTREE.GetEntry(ievent)
        for iseg in range(DTTREE.seg_nSegments):
            if DTTREE.seg_phi_t0[iseg] > -6.0 or DTTREE.seg_phi_t0[iseg] < 6.0:
                isMatchWithRPCbit01 = False
                for itrig in range(DTTREE.ltTwinMuxOut_nTrigs):
                    # Match between DTSegment and TwinMuxOut
                    isSameDetector = False
                    isSameWheel = False
                    isSameStation = False
                    isSameSector = False
                    isBX0 = False

                    if DTTREE.seg_wheel[iseg] and DTTREE.ltTwinMuxOut_wheel[itrig]:
                        isSameWheel = True
                    if DTTREE.seg_sector[iseg] and DTTREE.ltTwinMuxOut_sector[itrig]:
                        isSameSector = True
                    if DTTREE.seg_station[iseg] and DTTREE.ltTwinMuxOut_station[itrig]:
                        isSameStation = True
                    if DTTREE.ltTwinMuxOut_BX[itrig] == 0:
                        isBX0 = True

                    if isSameWheel and isSameStation and isSameSector and isBX0:
                        deltaPhi = DTTREE.seg_posGlb_phi[iseg] - DTTREE.ltTwinMuxOut_phi[itrig]
                        h_SegVsTwinMux_dPhi.Fill(deltaPhi)
                    
                    if DTTREE.seg_station[iseg] <= 2:
                        denoInclusive += 1
                        if DTTREE.ltTwinMuxOut_rpcBit[itrig] < 2:
                            if abs(DTTREE.ltTwinMuxOut_phi[itrig]) < coneSize:
                                numeInclusive += 1
                                isMatchWithRPCbit01 = True
                
                if not isMatchWithRPCbit01:
                    denoRPConly += 1
                    for itrig in range(DTTREE.ltTwinMuxOut_nTrigs):
                        if abs(DTTREE.ltTwinMuxOut_phi[itrig]) < coneSize and DTTREE.ltTwinMuxOut_rpcBit[itrig] == 2:
                            numeRPConly += 1

    print "\nDeno(inclusive): "+str(denoInclusive)
    print "Nume(inclusive): "+str(numeInclusive)
    print "Deno(RPConly): "+str(denoRPConly)
    print "Nume(RPConly): "+str(numeRPConly)
    effInclusive = float(numeInclusive)/float(denoInclusive)
    effRPConly = float(numeRPConly)/float(denoRPConly)
    h_Efficiency.SetBinContent(1, effInclusive)
    h_Efficiency.SetBinContent(2, effRPConly)
    print "Efficiency(inclusive): "+str(effInclusive)
    print "Efficiency(RPC only): "+str(effRPConly)

    f_out.Write()
    f_out.Close()
