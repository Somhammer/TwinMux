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

    h_Efficiency = TH1D('h_Efficiency', 'The efficiency of trigger primitives', 4, 0, 4)
    h_Efficiency.GetXaxis().SetTitle("")
    h_Efficiency.GetXaxis().SetBinLabel(1,'Deno(inclusive)')
    h_Efficiency.GetXaxis().SetBinLabel(2,'Nume(inclusive)')
    h_Efficiency.GetXaxis().SetBinLabel(3,'Deno(RPC only)')
    h_Efficiency.GetXaxis().SetBinLabel(4,'Nume(RPC only)')

    coneSize = 1600
    for ievent in xrange(DTTREE.GetEntries()):
        if not multiProcess:
            utils.printProgress(ievent, DTTREE.GetEntries(), 'Progress: ', 'Complete', 1, 25)
        DTTREE.GetEntry(ievent)
        for iseg in range(DTTREE.seg_nSegments):
            if DTTREE.seg_phi_t0[iseg] <= -6.0 or DTTREE.seg_phi_t0[iseg] >= 6.0: continue
            isMatchWithRPCbit01 = False
            for itrig in range(DTTREE.ltTwinMuxOut_nTrigs):
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
                if isSameWheel and isSameStation and isSameSector:
                    isSameDetector = True
                
                if isSameDetector and isBX0:
                    deltaPhi = DTTREE.seg_posGlb_phi[iseg] - DTTREE.ltTwinMuxOut_phi[itrig]
                    h_SegVsTwinMux_dPhi.Fill(deltaPhi)
                
                if DTTREE.seg_station[iseg] <= 2 and isSameDetector and isBX0:
                    h_Efficiency.Fill(0,1)
                    if DTTREE.ltTwinMuxOut_rpcBit[itrig] < 2:
                        h_Efficiency.Fill(1,1)
                        isMatchWithRPCbit01 = True
            
            if not isMatchWithRPCbit01 and DTTREE.seg_station[iseg] <= 2:
                h_Efficiency.Fill(2,1)
                for itrig in range(DTTREE.ltTwinMuxOut_nTrigs):
                    isSameWheel = False
                    isSameStation = False
                    isSameSector = False
                    if DTTREE.seg_wheel[iseg] and DTTREE.ltTwinMuxOut_wheel[itrig]:
                        isSameWheel = True
                    if DTTREE.seg_sector[iseg] and DTTREE.ltTwinMuxOut_sector[itrig]:
                        isSameSector = True
                    if DTTREE.seg_station[iseg] and DTTREE.ltTwinMuxOut_station[itrig]:
                        isSameStation = True

                    if isSameWheel and isSameSector and isSameStation:
                        h_Efficiency.Fill(3,1)
                        break
                
    if not multiProcess:
        effInclusive = float(h_Efficiency.GetBinContent(2))/float(h_Efficiency.GetBinContent(1))
        effRPConly = float(h_Efficiency.GetBinContent(1))/float(h_Efficiency.GetBinContent(3))
        print '\n==== Inclusive ===='
        print 'Nume: '+str(h_Efficiency.GetBinContent(2))+', Deno: '+str(h_Efficiency.GetBinContent(1))+', Efficiency: '+str(effInclusive)
        print '==== RPC only ===='
        print 'Nume: '+str(h_Efficiency.GetBinContent(4))+', Deno: '+str(h_Efficiency.GetBinContent(3))+', Efficiency: '+str(effRPConly)

    f_out.Write()
    f_out.Close()
