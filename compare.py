import sys
import numpy
from ROOT import *
from tqdm import tqdm

import tdrstyle

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

f_out = TFile.Open('DTDPGNtuple_10_3_3_ZMuSkim_2018D_Comparison.root', 'recreate')

DTTREE_data = TChain('dtNtupleProducer/DTTREE')
DTTREE_data.Add('DTDPGNtuple_10_3_3_ZMuSkim_2018D.root')

DTTREE_emul = TChain('dtNtupleProducer/DTTREE')
DTTREE_emul.Add('DTDPGNtuple_10_3_3_ZMuSkim_2018D_emulator_qual6.root')

print "Make ltTwinMuxOut 2D Comparison Histograms"
# branches of ltTwinMuxOut
#    nTrigs
#    wheel, sector, station, BX
#    quality, rpcBit, is2nd
#    phi, phiB, posLoc_x, dirLoc_phi
name_RPCbit = ['inclusive', 'RPCbit0', 'RPCbit1', 'RPCbit2']
nStation = 4 # 1 2 3 4
nWheel = 5 # -2 -1 0 1 2
nSector = 12 # 1 ~ 12
nBX = 9 # -4 ~ 4

name_Wheel = ['W-2', 'W-1', 'W0', 'W+1', 'W+2']
name_Sector = [
        'S1', 'S2', 'S3', 'S4', 'S5', 'S6',
        'S7', 'S8', 'S9', 'S10', 'S11', 'S12']
#name_Sector_RB3 = [
#        'Sector1-', 'Sector1+', 'Sector2-', 'Sector2+', 'Sector3-', 'Sector3+',
#        'Sector4-', 'Sector4+', 'Sector5-', 'Sector5+', 'Sector6-', 'Sector6+',
#        'Sector7-', 'Sector7+', 'Sector8-', 'Sector8+', 'Sector9-', 'Sector9+',
#        'Sector10-', 'Sector10+', 'Sector11-', 'Sector11+', 'Sector12-', 'Sector12+'
#        ]
#name_Sector_RB4 = [
#        'Sector1-', 'Sector1+', 'Sector2-', 'Sector2+', 'Sector3-', 'Sector3+',
#        'Sector4--', 'Sector4-', 'Sector4+', 'Sector4++', 'Sector5-', 'Sector5+',
#        'Sector6-', 'Sector6+', 'Sector7-', 'Sector7+', 'Sector8-', 'Sector8+',
#        'Sector9', 'Sector10-', 'Sector10+', 'Sector11', 'Sector12-', 'Sector12+'
#        ]
name_BX = ['BX-4', 'BX-3', 'BX-2', 'BX-1', 'BX0', 'BX1', 'BX2', 'BX3', 'BX4']

h_nRPCbitData = TH1D('h_nRPCbitData', 'RPC bit', 3, 0, 3)
h_nRPCbitData.GetXaxis().SetTitle('RPC bit')
h_nRPCbitData.GetXaxis().SetBinLabel(1, '0')
h_nRPCbitData.GetXaxis().SetBinLabel(2, '1')
h_nRPCbitData.GetXaxis().SetBinLabel(3, '2')
h_nRPCbitData.GetYaxis().SetTitle('Entries')
h_nRPCbitData.Sumw2()

h_nRPCbitEmul = TH1D('h_nRPCbitEmul', 'RPC bit', 3, 0, 3)
h_nRPCbitEmul.GetXaxis().SetTitle('RPC bit')
h_nRPCbitEmul.GetXaxis().SetBinLabel(1, '0')
h_nRPCbitEmul.GetXaxis().SetBinLabel(2, '1')
h_nRPCbitEmul.GetXaxis().SetBinLabel(3, '2')
h_nRPCbitEmul.GetYaxis().SetTitle('Entries')
h_nRPCbitEmul.Sumw2()

h_nSegmentData = TH1D('h_nSegmentData','Number of Segments',240,0,240)
h_nSegmentEmul = TH1D('h_nSegmentEmul','Number of Segments',240,0,240)
h_nSegmentData.GetYaxis().SetTitle('Number of Segments')
h_nSegmentEmul.GetYaxis().SetTitle('Number of Segments')
h_nSegmentData.Sumw2()
h_nSegmentEmul.Sumw2()
h_nSegmentData_RB = [[0] for i in range(nStation)]
h_nSegmentEmul_RB = [[0] for i in range(nStation)]

iBin = 1;
for i in range(nStation):
    h_nSegmentData_RB[i] = TH1D('h_nSegmentData_RB'+str(i+1),'Number of Segments in RB'+str(i+1),60,0,60)
    h_nSegmentEmul_RB[i] = TH1D('h_nSegmentEmul_RB'+str(i+1),'Number of Segments in RB'+str(i+1),60,0,60)
    h_nSegmentData_RB[i].GetYaxis().SetTitle('Number of Segments')
    h_nSegmentEmul_RB[i].GetYaxis().SetTitle('Number of Segments')
    h_nSegmentData_RB[i].Sumw2()
    h_nSegmentEmul_RB[i].Sumw2()
    iBin2 = 1;
    for j in range(nWheel):
        for k in range(nSector):
            str_name = 'RB'+str(i+1)+'_'+name_Wheel[j]+'_'+name_Sector[k]
            str_name2 = name_Wheel[j]+'_'+name_Sector[k]
            h_nSegmentData.GetXaxis().SetBinLabel(iBin,str_name)
            h_nSegmentEmul.GetXaxis().SetBinLabel(iBin,str_name)
            h_nSegmentData_RB[i].GetXaxis().SetBinLabel(iBin2,str_name2)
            h_nSegmentEmul_RB[i].GetXaxis().SetBinLabel(iBin2,str_name2)
            iBin += 1
            iBin2 += 1

h_nSegmentPerChamberData = TH1D("h_nSegmentPerChamberData", "Number of Segments per Chamber", 5, 0, 5)
h_nSegmentPerChamberData.GetXaxis().SetTitle('nSegments/chamber')
h_nSegmentPerChamberData.GetXaxis().SetBinLabel(1,'0')
h_nSegmentPerChamberData.GetXaxis().SetBinLabel(2,'1')
h_nSegmentPerChamberData.GetXaxis().SetBinLabel(3,'2')
h_nSegmentPerChamberData.GetXaxis().SetBinLabel(4,'3')
h_nSegmentPerChamberData.GetXaxis().SetBinLabel(5,'4')
h_nSegmentPerChamberData.GetYaxis().SetTitle('Entries')
h_nSegmentPerChamberData.Sumw2()

h_nSegmentPerChamberEmul = TH1D("h_nSegmentPerChamberEmul", "Number of Segments per Chamber", 5, 0, 5)
h_nSegmentPerChamberEmul.GetXaxis().SetTitle('nSegments/chamber')
h_nSegmentPerChamberEmul.GetXaxis().SetBinLabel(1,'0')
h_nSegmentPerChamberEmul.GetXaxis().SetBinLabel(2,'1')
h_nSegmentPerChamberEmul.GetXaxis().SetBinLabel(3,'2')
h_nSegmentPerChamberEmul.GetXaxis().SetBinLabel(4,'3')
h_nSegmentPerChamberEmul.GetXaxis().SetBinLabel(5,'4')
h_nSegmentPerChamberEmul.GetYaxis().SetTitle('Entries')
h_nSegmentPerChamberEmul.Sumw2()

h2_ltTwinMuxOut_phi = [[0] for i in range(len(name_RPCbit))]
h2_ltTwinMuxOut_phiB = [[0] for i in range(len(name_RPCbit))]
h2_ltTwinMuxOut_posLoc_x = [[0] for i in range(len(name_RPCbit))]
h2_ltTwinMuxOut_dirLoc_phi = [[0] for i in range(len(name_RPCbit))]

for i in range(len(name_RPCbit)):
    h2_ltTwinMuxOut_phi[i] = TH2D(
            'h2_ltTwinMuxOut_phi_'+name_RPCbit[i],
            'h2_ltTwinMuxOut_phi_'+name_RPCbit[i],
            100, -2000.0, 2000.0, 100, -2000.0, 2000.0)
    h2_ltTwinMuxOut_phi[i].GetXaxis().SetTitle('Data.ltTwinMuxOut_phi')
    h2_ltTwinMuxOut_phi[i].GetYaxis().SetTitle('Emul.ltTwinMuxOut_phi')
    h2_ltTwinMuxOut_phi[i].Sumw2()

    h2_ltTwinMuxOut_phiB[i] = TH2D(
            'h2_ltTwinMuxOut_phiB_'+name_RPCbit[i],
            'h2_ltTwinMuxOut_phiB_'+name_RPCbit[i],
            100, -450.0, 450.0, 100, -450.0, 450.0)
    h2_ltTwinMuxOut_phiB[i].GetXaxis().SetTitle('Data.ltTwinMuxOut_phiB')
    h2_ltTwinMuxOut_phiB[i].GetYaxis().SetTitle('Emul.ltTwinMuxOut_phiB')
    h2_ltTwinMuxOut_phiB[i].Sumw2()

    h2_ltTwinMuxOut_posLoc_x[i] = TH2D(
            'h2_ltTwinMuxOut_posLoc_x_'+name_RPCbit[i],
            'h2_ltTwinMuxOut_posLoc_x_'+name_RPCbit[i],
            100, -350.0, 350.0, 100, -350.0, 350.0)
    h2_ltTwinMuxOut_posLoc_x[i].GetXaxis().SetTitle('Data.ltTwinMuxOut_posLoc_x')
    h2_ltTwinMuxOut_posLoc_x[i].GetYaxis().SetTitle('Emul.ltTwinMuxOut_posLoc_x')
    h2_ltTwinMuxOut_posLoc_x[i].Sumw2()

    h2_ltTwinMuxOut_dirLoc_phi[i] = TH2D(
            'h2_ltTwinMuxOut_dirLoc_phi_'+name_RPCbit[i],
            'h2_ltTwinMuxOut_dirLoc_phi_'+name_RPCbit[i],
            100, -90.0, 90.0, 100, -90.0, 90.0)
    h2_ltTwinMuxOut_dirLoc_phi[i].GetXaxis().SetTitle('Data.ltTwinMuxOut_dirLoc_phi')
    h2_ltTwinMuxOut_dirLoc_phi[i].GetYaxis().SetTitle('Emul.ltTwinMuxOut_dirLoc_phi')
    h2_ltTwinMuxOut_dirLoc_phi[i].Sumw2()

f_out.cd()

print "Compare data and emul event by event"

for i in xrange(DTTREE_data.GetEntries()):
    printProgress(i, DTTREE_data.GetEntries(), 'Progress: ', 'Complete', 1, 25)
    
    DTTREE_data.GetEntry(i)
    DTTREE_emul.GetEntry(i)
    if DTTREE_data.event_eventNumber != DTTREE_emul.event_eventNumber:
        print "Entry: "+str(i)+" They are not same event number"
        continue
    
    nSegmentData  = [[[[0 for i in range(nBX)] for j in range(nSector)] for k in range(nWheel)] for l in range(nStation)]
    nSegmentEmul  = [[[[0 for i in range(nBX)] for j in range(nSector)] for k in range(nWheel)] for l in range(nStation)]
   
    # Debug
    #if len(DTTREE_data.ltTwinMuxOut_rpcBit) > 0:
    #    tmp = ""
    #    for i in range(DTTREE_data.ltTwinMuxOut_rpcBit.size()):
    #        tmp += " "+str(DTTREE_data.ltTwinMuxOut_rpcBit[i])
    #    print "rpcBit Size: " + str(DTTREE_data.ltTwinMuxOut_rpcBit.size())+" Value: "+tmp

    #if DTTREE_data.ltTwinMuxOut_sector.size() > 0:
    #    str_station = ""
    #    str_wheel = ""
    #    str_sector = ""
    #    str_BX = ""
    #    for i in range(DTTREE_data.ltTwinMuxOut_sector.size()):
    #        str_station += " "+str(DTTREE_data.ltTwinMuxOut_station[i])
    #        str_wheel += " "+str(DTTREE_data.ltTwinMuxOut_wheel[i])
    #        str_sector += " "+str(DTTREE_data.ltTwinMuxOut_sector[i])
    #        str_BX += " "+str(DTTREE_data.ltTwinMuxOut_BX[i])
    #    print str(DTTREE_data.event_eventNumber)
    #    print "  Staton size:"+str(DTTREE_data.ltTwinMuxOut_station.size())+" value:"+str_station
    #    print "  Wheel  size:"+str(DTTREE_data.ltTwinMuxOut_wheel.size())+" value:"+str_wheel
    #    print "  Sector size:"+str(DTTREE_data.ltTwinMuxOut_sector.size())+" value:"+str_sector
    #    print "  BX     size:"+str(DTTREE_data.ltTwinMuxOut_BX.size())+" value:"+str_BX

    #if len(DTTREE_data.ltTwinMuxOut_station) > 0 and len(DTTREE_data.ltTwinMuxOut_wheel) > 0 and len(DTTREE_data.ltTwinMuxOut_sector) > 0 and len(DTTREE_data.ltTwinMuxOut_BX) > 0:
    #    print "Station:"+str(DTTREE_data.ltTwinMuxOut_station.size())+" Wheel:"+str(DTTREE_data.ltTwinMuxOut_wheel.size())+\
    #            " Sector:"+str(DTTREE_data.ltTwinMuxOut_sector.size())+" BX:"+str(DTTREE_data.ltTwinMuxOut_BX.size())
        #print "Station:"+str(DTTREE_data.ltTwinMuxOut_station[0])+" Wheel:"+str(DTTREE_data.ltTwinMuxOut_wheel[0])+\
        #        " Sector:"+str(DTTREE_data.ltTwinMuxOut_sector[0])+" BX:"+str(DTTREE_data.ltTwinMuxOut_BX[0])
    #if len(DTTREE_data.ltTwinMuxOut_station) > 1 and len(DTTREE_data.ltTwinMuxOut_wheel) > 1 and len(DTTREE_data.ltTwinMuxOut_sector) > 1 and len(DTTREE_data.ltTwinMuxOut_BX) > 1:
    #    print "Station[1]:"+str(DTTREE_data.ltTwinMuxOut_station[1])+" Wheel[1]:"+str(DTTREE_data.ltTwinMuxOut_wheel[1])+\
    #            " Sector[1]:"+str(DTTREE_data.ltTwinMuxOut_sector[1])+" BX[1]:"+str(DTTREE_data.ltTwinMuxOut_BX[1])
    #else:
    #    print "Empty info"
    for i in range(DTTREE_data.ltTwinMuxOut_station.size()):
        same_rpcBit = False
        same_is2nd = False
        same_station = False
        same_wheel = False
        same_sector = False
        same_BX = False
        for j in range(DTTREE_emul.ltTwinMuxOut_station.size()):
            if DTTREE_data.ltTwinMuxOut_rpcBit[i] == DTTREE_emul.ltTwinMuxOut_rpcBit[j]:
                same_rpcBit = True
            if DTTREE_data.ltTwinMuxOut_is2nd[i] == DTTREE_emul.ltTwinMuxOut_is2nd[j]:
                same_is2nd = True
            if DTTREE_data.ltTwinMuxOut_station[i] == DTTREE_emul.ltTwinMuxOut_station[j]:
                same_station = True
            if DTTREE_data.ltTwinMuxOut_wheel[i] == DTTREE_emul.ltTwinMuxOut_wheel[j]:
                same_wheel = True
            if DTTREE_data.ltTwinMuxOut_sector[i] == DTTREE_emul.ltTwinMuxOut_sector[j]:
                same_sector = True
            if DTTREE_data.ltTwinMuxOut_BX[i] == DTTREE_emul.ltTwinMuxOut_BX[j]:
                same_BX = True

            if same_rpcBit and same_is2nd and same_station and same_wheel and same_sector and same_BX:
                h2_ltTwinMuxOut_phi[0].Fill(DTTREE_data.ltTwinMuxOut_phi[i], DTTREE_emul.ltTwinMuxOut_phi[j])
                h2_ltTwinMuxOut_phiB[0].Fill(DTTREE_data.ltTwinMuxOut_phiB[i], DTTREE_emul.ltTwinMuxOut_phiB[j])
                h2_ltTwinMuxOut_posLoc_x[0].Fill(DTTREE_data.ltTwinMuxOut_posLoc_x[i], DTTREE_emul.ltTwinMuxOut_posLoc_x[j])
                h2_ltTwinMuxOut_dirLoc_phi[0].Fill(DTTREE_data.ltTwinMuxOut_dirLoc_phi[i], DTTREE_emul.ltTwinMuxOut_dirLoc_phi[j])
                if DTTREE_data.ltTwinMuxOut_rpcBit[i] == 0:
                    h2_ltTwinMuxOut_phi[1].Fill(DTTREE_data.ltTwinMuxOut_phi[i], DTTREE_emul.ltTwinMuxOut_phi[j])
                    h2_ltTwinMuxOut_phiB[1].Fill(DTTREE_data.ltTwinMuxOut_phiB[i], DTTREE_emul.ltTwinMuxOut_phiB[j])
                    h2_ltTwinMuxOut_posLoc_x[1].Fill(DTTREE_data.ltTwinMuxOut_posLoc_x[i], DTTREE_emul.ltTwinMuxOut_posLoc_x[j])
                    h2_ltTwinMuxOut_dirLoc_phi[1].Fill(DTTREE_data.ltTwinMuxOut_dirLoc_phi[i], DTTREE_emul.ltTwinMuxOut_dirLoc_phi[j])
                elif DTTREE_data.ltTwinMuxOut_rpcBit[i] == 1:
                    h2_ltTwinMuxOut_phi[2].Fill(DTTREE_data.ltTwinMuxOut_phi[i], DTTREE_emul.ltTwinMuxOut_phi[j])
                    h2_ltTwinMuxOut_phiB[2].Fill(DTTREE_data.ltTwinMuxOut_phiB[i], DTTREE_emul.ltTwinMuxOut_phiB[j])
                    h2_ltTwinMuxOut_posLoc_x[2].Fill(DTTREE_data.ltTwinMuxOut_posLoc_x[i], DTTREE_emul.ltTwinMuxOut_posLoc_x[j])
                    h2_ltTwinMuxOut_dirLoc_phi[2].Fill(DTTREE_data.ltTwinMuxOut_dirLoc_phi[i], DTTREE_emul.ltTwinMuxOut_dirLoc_phi[j])
                elif DTTREE_data.ltTwinMuxOut_rpcBit[i] == 2:
                    h2_ltTwinMuxOut_phi[3].Fill(DTTREE_data.ltTwinMuxOut_phi[i], DTTREE_emul.ltTwinMuxOut_phi[j])
                    h2_ltTwinMuxOut_phiB[3].Fill(DTTREE_data.ltTwinMuxOut_phiB[i], DTTREE_emul.ltTwinMuxOut_phiB[j])
                    h2_ltTwinMuxOut_posLoc_x[3].Fill(DTTREE_data.ltTwinMuxOut_posLoc_x[i], DTTREE_emul.ltTwinMuxOut_posLoc_x[j])
                    h2_ltTwinMuxOut_dirLoc_phi[3].Fill(DTTREE_data.ltTwinMuxOut_dirLoc_phi[i], DTTREE_emul.ltTwinMuxOut_dirLoc_phi[j])

    #nSegment[nStation][nWheel][nSector][nBX]
    for i in range(DTTREE_data.ltTwinMuxOut_nTrigs):
        iStation_idx = DTTREE_data.ltTwinMuxOut_station[i] - 1
        iWheel_idx = DTTREE_data.ltTwinMuxOut_wheel[i] + 2
        iSector_idx = DTTREE_data.ltTwinMuxOut_sector[i] - 1
        iBX_idx = DTTREE_data.ltTwinMuxOut_BX[i] + 4
        nSegmentData[iStation_idx][iWheel_idx][iSector_idx][iBX_idx] += 1
        h_nRPCbitData.Fill(DTTREE_data.ltTwinMuxOut_rpcBit[i])

    for i in range(DTTREE_emul.ltTwinMuxOut_nTrigs):
        iStation_idx = DTTREE_emul.ltTwinMuxOut_station[i] - 1
        iWheel_idx = DTTREE_emul.ltTwinMuxOut_wheel[i] + 2
        iSector_idx = DTTREE_emul.ltTwinMuxOut_sector[i] - 1
        iBX_idx = DTTREE_emul.ltTwinMuxOut_BX[i] + 4
        nSegmentEmul[iStation_idx][iWheel_idx][iSector_idx][iBX_idx] += 1
        h_nRPCbitEmul.Fill(DTTREE_emul.ltTwinMuxOut_rpcBit[i])

    # Debug
    #check = numpy.array(nSegmentData)
    #tmp = numpy.where(check != 0)
    #if tmp[0].size > 0:
    #    for i in range(tmp[0].size):
    #        print("Index: "+str(tmp[0][i])+" "+str(tmp[1][i])+" "+str(tmp[2][i])+" "+str(tmp[3][i]))
    #        print("Value: "+str(nSegmentData[tmp[0][i]][tmp[1][i]][tmp[2][i]][tmp[3][i]]))

    binNum = 0
    for i in range(nStation):
        binNum2 = 0
        for j in range(nWheel):
            for k in range(nSector):
                tmp1 = 0.0
                tmp2 = 0.0
                for l in range(nBX):
                    tmp1 += nSegmentData[i][j][k][l]
                    tmp2 += nSegmentEmul[i][j][k][l]
                    h_nSegmentPerChamberData.Fill(nSegmentData[i][j][k][l])
                    h_nSegmentPerChamberEmul.Fill(nSegmentEmul[i][j][k][l])
                h_nSegmentData.Fill(binNum, tmp1)
                h_nSegmentEmul.Fill(binNum, tmp2)
                h_nSegmentData_RB[i].Fill(binNum2, tmp1)
                h_nSegmentEmul_RB[i].Fill(binNum2, tmp2)
                binNum += 1
                binNum2 += 1
    
h_nSegmentPerChamberData2 = h_nSegmentPerChamberData.Clone()
h_nSegmentPerChamberData2.SetName(h_nSegmentPerChamberData.GetName()+'_exceptSeg0')
h_nSegmentPerChamberData2.SetBinContent(1,0)

h_nSegmentPerChamberEmul2 = h_nSegmentPerChamberEmul.Clone()
h_nSegmentPerChamberEmul2.SetName(h_nSegmentPerChamberEmul.GetName()+'_exceptSeg0')
h_nSegmentPerChamberEmul2.SetBinContent(1,0)

f_out.Write()

tdrstyle.setTDRStyle()
wp = tdrstyle.tdrWorkProgress()

c = TCanvas('c','c',600,600)
leg = TLegend(0.52,0.78,0.88,0.92)
leg.SetTextSize(0.03)
leg.SetTextFont(42)

leg.SetHeader('Run2018D SingleMu Run 321475')
leg.AddEntry(h_nRPCbitData, 'Unpacked', 'l')
leg.AddEntry(h_nRPCbitEmul, 'Emulator', 'l')

h_nRPCbitData.SetLineWidth(2)
h_nRPCbitEmul.SetLineWidth(2)
h_nRPCbitEmul.SetLineColor(kRed)
h_nRPCbitData.SetMaximum(h_nRPCbitEmul.GetMaximum()*1.5)
#h_nRPCbitData.GetYaxis().SetTitleSize(0.055)
h_nRPCbitData.GetYaxis().SetLabelSize(0.038)
#h_nRPCbitData.GetXaxis().SetTitleSize(0.055)
h_nRPCbitData.GetXaxis().SetLabelSize(0.055)
h_nRPCbitData.Draw('hist')
h_nRPCbitEmul.Draw('hist same')
leg.Draw('same')
wp.Draw('same')
c.Print('h_nRPCbitComp.pdf','pdf')
leg.Clear()
c.Clear()

leg.SetHeader('Run2018D SingleMu Run 321475')
leg.AddEntry(h_nSegmentPerChamberData, 'Unpacked', 'l')
leg.AddEntry(h_nSegmentPerChamberEmul, 'Emulator', 'l')

h_nSegmentPerChamberData.SetLineWidth(2)
h_nSegmentPerChamberEmul.SetLineWidth(2)
h_nSegmentPerChamberEmul.SetLineColor(kRed)
h_nSegmentPerChamberData.SetMaximum(h_nSegmentPerChamberEmul.GetMaximum()*1.5)
h_nSegmentPerChamberData.GetYaxis().SetLabelSize(0.038)
h_nSegmentPerChamberData.GetXaxis().SetLabelSize(0.055)
h_nSegmentPerChamberData.Draw('hist')
h_nSegmentPerChamberEmul.Draw('hist same')
leg.Draw('same')
wp.Draw('same')
c.Print('h_nSegmentPerChamberComp.pdf','pdf')
leg.Clear()
c.Clear()

leg.SetHeader('Run2018D SingleMu Run 321475')
leg.AddEntry(h_nSegmentPerChamberData2, 'Unpacked', 'l')
leg.AddEntry(h_nSegmentPerChamberEmul2, 'Emulator', 'l')

h_nSegmentPerChamberData2.SetLineWidth(2)
h_nSegmentPerChamberEmul2.SetLineWidth(2)
h_nSegmentPerChamberEmul2.SetLineColor(kRed)
h_nSegmentPerChamberData2.SetMaximum(h_nSegmentPerChamberEmul2.GetMaximum()*1.5)
h_nSegmentPerChamberData2.GetYaxis().SetLabelSize(0.038)
h_nSegmentPerChamberData2.GetXaxis().SetLabelSize(0.055)
h_nSegmentPerChamberData2.Draw('hist')
h_nSegmentPerChamberEmul2.Draw('hist same')
leg.Draw('same')
wp.Draw('same')
c.Print('h_nSegmentPerChamberComp_except0.pdf','pdf')
leg.Clear()
c.Clear()

for i in range(nStation):
    label = TPaveText()
    label.SetX1NDC(0.21)
    label.SetX2NDC(0.40)
    label.SetY1NDC(0.82)
    label.SetY2NDC(0.92)
    label.AddText('Station: RB'+str(i+1))
    label.SetTextFont(42)
    label.SetFillStyle(0)
    label.SetBorderSize(0)
    label.SetTextSize(0.04)

    leg.SetHeader('Run2018D SingleMu Run 321475')
    leg.AddEntry(h_nSegmentData_RB[i], 'Unpacked', 'l')
    leg.AddEntry(h_nSegmentEmul_RB[i], 'Emulator', 'l')

    #h_nSegmentData_RB[i].SetLineWidth(2)
    #h_nSegmentEmul_RB[i].SetLineWidth(2)
    h_nSegmentEmul_RB[i].SetLineColor(kRed)
    h_nSegmentData_RB[i].SetMaximum(h_nSegmentEmul_RB[i].GetMaximum()*1.5)
    h_nSegmentData_RB[i].GetYaxis().SetLabelSize(0.038)
    h_nSegmentData_RB[i].GetXaxis().SetLabelSize(0.025)
    h_nSegmentData_RB[i].Draw('hist')
    h_nSegmentEmul_RB[i].Draw('hist same')
    leg.Draw('same')
    wp.Draw('same')
    label.Draw('same')
    c.Print('h_nSegmentComp_RB'+str(i+1)+'.pdf','pdf')
    leg.Clear()
    c.Clear()

for i in range(len(name_RPCbit)):
    h_ltTwinMuxOut_phi_offdig = h2_ltTwinMuxOut_phi[i].ProjectionX()
    print "x-axis: 50 bin : "+str(h_ltTwinMuxOut_phi_offdig.GetBinContent(50))
    for iBin in range(1,h_ltTwinMuxOut_phi_offdig.GetNbinsX()+1):
        if h2_ltTwinMuxOut_phi[i].GetBinContent(50, iBin) != 0.0:
            print str(iBin)+" : "+str(h2_ltTwinMuxOut_phi[i].GetBinContent(50, iBin))

    for iBin in range(1,h_ltTwinMuxOut_phi_offdig.GetNbinsX()+1):
        tmp = h2_ltTwinMuxOut_phi[i].GetBinContent(iBin, iBin)
        tmp2 = h_ltTwinMuxOut_phi_offdig.GetBinContent(iBin)
        if tmp2 != 0 :
            value = ((tmp2 - tmp) / tmp2) * 100
            if i == 0:
                print str(iBin)+" : proj: "+str(tmp2)+" diag: "+str(tmp)+" value: "+str(value)
        else:
            value = 0
        h_ltTwinMuxOut_phi_offdig.SetBinContent(iBin, value)
    
    h_ltTwinMuxOut_phi_offdig.GetYaxis().SetTitleFont(42)
    h_ltTwinMuxOut_phi_offdig.GetYaxis().SetTitle('Off diagonal(%)')
    h_ltTwinMuxOut_phi_offdig.GetYaxis().SetTitleSize(0.038)
    h_ltTwinMuxOut_phi_offdig.GetYaxis().SetLabelSize(0.038)
    h_ltTwinMuxOut_phi_offdig.GetXaxis().SetTitle('ltTwinMuxOut phi')
    h_ltTwinMuxOut_phi_offdig.GetXaxis().SetLabelSize(0.025)

    h_ltTwinMuxOut_phi_offdig.Draw('hist')
    wp.Draw('same')
    c.Print('h_ltTwinMuxOut_phi_offdig_'+name_RPCbit[i]+'.pdf', 'pdf')
    c.Clear()

    h_ltTwinMuxOut_phiB_offdig = h2_ltTwinMuxOut_phiB[i].ProjectionX()
    for iBin in range(1,h_ltTwinMuxOut_phiB_offdig.GetNbinsX()+1):
        tmp = h2_ltTwinMuxOut_phiB[i].GetBinContent(iBin, iBin)
        tmp2 = h_ltTwinMuxOut_phiB_offdig.GetBinContent(iBin)
        if tmp2 != 0 :
            value = ((tmp2 - tmp) / tmp2) * 100
        else:
            value = 0
        h_ltTwinMuxOut_phiB_offdig.SetBinContent(iBin, value)
    
    h_ltTwinMuxOut_phiB_offdig.GetYaxis().SetTitleFont(42)
    h_ltTwinMuxOut_phiB_offdig.GetYaxis().SetTitle('Off diagonal(%)')
    h_ltTwinMuxOut_phiB_offdig.GetYaxis().SetTitleSize(0.038)
    h_ltTwinMuxOut_phiB_offdig.GetYaxis().SetLabelSize(0.038)
    h_ltTwinMuxOut_phiB_offdig.GetXaxis().SetTitle('ltTwinMuxOut phi')
    h_ltTwinMuxOut_phiB_offdig.GetXaxis().SetLabelSize(0.025)

    h_ltTwinMuxOut_phiB_offdig.Draw('hist')
    wp.Draw('same')
    c.Print('h_ltTwinMuxOut_phiB_offdig_'+name_RPCbit[i]+'.pdf', 'pdf')
    c.Clear()

    h_ltTwinMuxOut_posLoc_x_offdig = h2_ltTwinMuxOut_posLoc_x[i].ProjectionX()
    for iBin in range(1,h_ltTwinMuxOut_posLoc_x_offdig.GetNbinsX()+1):
        tmp = h2_ltTwinMuxOut_posLoc_x[i].GetBinContent(iBin, iBin)
        tmp2 = h_ltTwinMuxOut_posLoc_x_offdig.GetBinContent(iBin)
        if tmp2 != 0 :
            value = ((tmp2 - tmp) / tmp2) * 100
        else:
            value = 0
        h_ltTwinMuxOut_posLoc_x_offdig.SetBinContent(iBin, value)
    
    h_ltTwinMuxOut_posLoc_x_offdig.GetYaxis().SetTitleFont(42)
    h_ltTwinMuxOut_posLoc_x_offdig.GetYaxis().SetTitle('Off diagonal(%)')
    h_ltTwinMuxOut_posLoc_x_offdig.GetYaxis().SetTitleSize(0.038)
    h_ltTwinMuxOut_posLoc_x_offdig.GetYaxis().SetLabelSize(0.038)
    h_ltTwinMuxOut_posLoc_x_offdig.GetXaxis().SetTitle('ltTwinMuxOut posLoc_x')
    h_ltTwinMuxOut_posLoc_x_offdig.GetXaxis().SetLabelSize(0.025)

    h_ltTwinMuxOut_posLoc_x_offdig.Draw('hist')
    wp.Draw('same')
    c.Print('h_ltTwinMuxOut_posLoc_x_offdig_'+name_RPCbit[i]+'.pdf', 'pdf')
    c.Clear()

    h_ltTwinMuxOut_dirLoc_phi_offdig = h2_ltTwinMuxOut_dirLoc_phi[i].ProjectionX()
    for iBin in range(1,h_ltTwinMuxOut_dirLoc_phi_offdig.GetNbinsX()+1):
        tmp = h2_ltTwinMuxOut_dirLoc_phi[i].GetBinContent(iBin, iBin)
        tmp2 = h_ltTwinMuxOut_dirLoc_phi_offdig.GetBinContent(iBin)
        if tmp2 != 0 :
            value = ((tmp2 - tmp) / tmp2) * 100
        else:
            value = 0
        h_ltTwinMuxOut_dirLoc_phi_offdig.SetBinContent(iBin, value)
    
    h_ltTwinMuxOut_dirLoc_phi_offdig.GetYaxis().SetTitleFont(42)
    h_ltTwinMuxOut_dirLoc_phi_offdig.GetYaxis().SetTitle('Off diagonal(%)')
    h_ltTwinMuxOut_dirLoc_phi_offdig.GetYaxis().SetTitleSize(0.038)
    h_ltTwinMuxOut_dirLoc_phi_offdig.GetYaxis().SetLabelSize(0.038)
    h_ltTwinMuxOut_dirLoc_phi_offdig.GetXaxis().SetTitle('ltTwinMuxOut dirLoc_phi')
    h_ltTwinMuxOut_dirLoc_phi_offdig.GetXaxis().SetLabelSize(0.025)

    gPad.SetRightMargin(0.12)

    h_ltTwinMuxOut_dirLoc_phi_offdig.Draw('hist')
    wp.Draw('same')
    c.Print('h_ltTwinMuxOut_dirLoc_phi_offdig_'+name_RPCbit[i]+'.pdf', 'pdf')
    c.Clear()

    h2_ltTwinMuxOut_phi[i].Draw('colz')
    c.Print('h2_ltTwinMuxOut_phi_'+name_RPCbit[i]+'.pdf', 'pdf')
    c.Clear()

    h2_ltTwinMuxOut_phiB[i].Draw('colz')
    c.Print('h2_ltTwinMuxOut_phiB_'+name_RPCbit[i]+'.pdf', 'pdf')
    c.Clear()

    h2_ltTwinMuxOut_posLoc_x[i].Draw('colz')
    c.Print('h2_ltTwinMuxOut_posLoc_x_'+name_RPCbit[i]+'.pdf', 'pdf')
    c.Clear()

    h2_ltTwinMuxOut_dirLoc_phi[i].Draw('colz')
    c.Print('h2_ltTwinMuxOut_dirLoc_phi_'+name_RPCbit[i]+'.pdf', 'pdf')
    c.Clear()

f_out.Close()
