import os
import sys
import numpy

import math
from ROOT import *

import tdrstyle
import utils

def calEfficiency():#(emulDir, inFile, outDir):
    #print "Start "+str(inFile)
    #if not os.path.exists(outDir+'/efficiency'):
    #    os.makdirs(outDir+'/efficiency')
    #f_out = TFile.Open(outDir+'/efficiency/'+inFile[:-5]+'_efficiency.root', 'recreate')
    
    #emulFile = inFile[:inFile.rfind('_')]+'_Emulator_'+inFile[:-5].split('_')[-1]+'.root'
    #DTTREE_emul = TChain('dtNtupleProducer/DTTREE')
    #DTTREE_emul.Add(emulDir+'/'+emulFile)
    f_out = TFile.Open("Effciency.root","recreate")
    DTTREE_emul = TChain('dtNtupleProducer/DTTREE')
    DTTREE_emul.Add("DTDPGNtuple_10_3_3_ZMuSkim_2018D_emulator.root")
    f_out.cd()
    
    h_SegVsTwinMux_dPhi = TH1D('h_SegVsTwinMux_dPhi', 'Segment vs TwinMux dPhi', 100, -2000.0, 2000.0)
    h_SegVsTwinMux_dPhi.GetXaxis().SetTitle('#Delta phi_{Seg,TwinMux}')
    h_SegVsTwinMux_dPhi.GetYaxis().SetTitle('Entries')
    h_SegVsTwinMux_dPhi.Sumw2()

    coneSize = 1600
    deno = 0 
    nume = 0
    for iEvt in xrange(DTTREE_emul.GetEntries()):
        DTTREE_emul.GetEntry(iEvt)
        for iSeg in range(DTTREE_emul.seg_nSegments):
            if DTTREE_emul.seg_phi_t0[iSeg] > -6.0 or DTTREE_emul.seg_phi_t0[iSeg] < 6.0:
                for iTrig in range(DTTREE_emul.ltTwinMuxOut_nTrigs):
                    same_wheel = False
                    same_station = False
                    same_sector = False
                    isBX0 = False

                    if DTTREE_emul.seg_wheel[iSeg] and DTTREE_emul.ltTwinMuxOut_wheel[iTrig]:
                        same_wheel = True
                    if DTTREE_emul.seg_sector[iSeg] and DTTREE_emul.ltTwinMuxOut_sector[iTrig]:
                        same_sector = True
                    if DTTREE_emul.seg_station[iSeg] and DTTREE_emul.ltTwinMuxOut_station[iTrig]:
                        same_station = True
                    if DTTREE_emul.ltTwinMuxOut_BX[iTrig] == 0:
                        isBX0 = True

                    if same_wheel and same_station and same_sector and isBX0:
                        deltaPhi = DTTREE_emul.seg_posGlb_phi[iSeg] - DTTREE_emul.ltTwinMuxOut_phi[iTrig]
                        h_SegVsTwinMux_dPhi.Fill(deltaPhi)
                    
                    if DTTREE_emul.seg_station[iSeg] <= 2:
                        deno += 1
                        if DTTREE_emul.ltTwinMuxOut_rpcBit[iTrig] < 2 and abs(DTTREE_emul.ltTwinMuxOut_phi[iTrig]) < coneSize:
                            nume += 1

    print "Deno: "+str(deno)
    print "Nume: "+str(nume)
    eff = float(nume)/float(deno)
    print "Efficiency: "+str(eff)

    f_out.Write()
    f_out.Close()

calEfficiency()
