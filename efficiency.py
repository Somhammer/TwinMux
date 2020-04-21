import os
import sys
import numpy

import math
from ROOT import *

import tdrstyle
import utils 

def calEfficiency():#(emulDir, inFile, outDir):
    global cone = 1.6
    #print "Start "+str(inFile)
    #f_out = TFile.Open(outDir+'/Efficiency_'+inFile, 'recreate')
    
    #emulFile = inFile[:inFile.rfind('_')]+'_Emulator_'+inFile[:-5].split('_')[-1]+'.root'
    #DTTREE_emul = TChain('dtNtupleProducer/DTTREE')
    #DTTREE_emul.Add(emulDir+'/'+emulFile)
    f_out = TFile.Open("Effciency.root","recreate")
    DTTREE_emul = TChain('dtNtupleProducer/DTTREE')
    DTTREE_emul.Add("DTDPGNtuple_10_3_3_ZMuSkim_2018D_emulator.root")
    f_out.cd()
    
    h_SegVsTwinMux_dPhi = TH1D('h_SegVsTwinMux_dPhi', 'Segment vs TwinMux dPhi', 40, 0.0, 4.0)
    h_SegVsTwinMux_dPhi.GetXaxis().SetTitle('|#Delta phi_{Seg,TwinMux}|')
    h_SegVsTwinMux_dPhi.GetYaxis().SetTitle('Entries')
    h_SegVsTwinMux_dPhi.Sumw2()

    for iEvt in xrange(DTTREE_emul.GetEntries()):
        DTTREE_emul.GetEntry(iEvt)
        for iSeg in range(DTTREE_emul.seg_nSegments):
            if DTTREE_emul.seg_phi_t0[iSeg] < -12.5 or DTTREE_emul.seg_phi_t0[iSeg] > 12.5:
                continue
            
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
                    phin = (DTTREE_emul.seg_sector[iSeg]-1) * math.pi/6
                    phicenter = DTTREE_emul.seg_dirGlb_phi[iSeg]
                    dirLoc = TVector3(DTTREE_emul.seg_dirLoc_x[iSeg], DTTREE_emul.seg_dirLoc_y[iSeg], DTTREE_emul.seg_dirLoc_z[iSeg])
                    r = dirLoc.Perp()
                    x = DTTREE_emul.seg_posLoc_x[iSeg]
                    segPhi = math.atan((x + r * math.sin(phicenter - phin))/(r * math.cos(phicenter - phin)))
                    deltaPhi = abs(segPhi - DTTREE_emul.ltTwinMuxOut_phi[iTrig] % math.pi)
                    h_SegVsTwinMux_dPhi.Fill(deltaPhi)

    f_out.Write()
    f_out.Close()

calEfficiency()
