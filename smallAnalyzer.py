import sys,os
import numpy
import ROOT as r
from rootGarbageCollection import *
import profile, cProfile
import optparse

r.gROOT.SetBatch(True)

def main() :
    r.gROOT.SetBatch(True)

    parser = optparse.OptionParser(description="Switch debug info")
    parser.add_option('-d', '--debug',                  action="store_true", default=False,  dest="debug")
    parser.add_option('-o', '--outFile', type='string', action="store",      default="/tmp/sturdy/hpdInformation", dest="outFileName")
    parser.add_option('-j', '--jobName', type='string', action="store",      default="HTMHT", dest="jobName")
    parser.add_option('-f', '--fileList',type='string', action="store",      default="", dest="fileList")
    parser.add_option('-l', '--fileLow', type='int',    action="store",      default=0,       dest="fileLow")
    parser.add_option('-u', '--fileHigh',type='int',    action="store",      default=100,     dest="fileHigh")
    options, args = parser.parse_args()

    listOfFiles = options.fileList.split(',')
    if options.debug:
        print options.fileList
        print listOfFiles
    ##old method##badFiles = [4,5,7,
    ##old method##            29,
    ##old method##            30,32,39,
    ##old method##            40,42,44,46,47,
    ##old method##            55,56,57,58,59,
    ##old method##            60,64,66,69,
    ##old method##            71,79,
    ##old method##            80,81,88,
    ##old method##            90,91,92,94,98,99]
    ##old method##chain = r.TChain("ExportTree/HcalNoiseTree")
    ##old method##if options.debug:
    ##old method##    chain.Add("HTMHT_NoiseTree_9.root")
    ##old method##else:
    ##old method##    for file in range(options.fileLow,options.fileHigh):
    ##old method##        if file not in badFiles:
    ##old method##            chain.Add("root://eoscms//eos/cms/store/caf/user/chenyi/HcalNoiseTree/V00-03-12142/537p6/FT_P_V42D/HBHEYesHFNoHONo/000003/HTMHT/NoiseTree_%d.root"%(file))
    # new method #
    chain = r.TChain("ExportTree/HcalNoiseTree")
    if options.debug:
        chain.Add("HTMHT_NoiseTree_9.root")
    else:
        for subFile in listOfFiles:
            chain.Add("root://eoscms//eos/cms/store/caf/user/chenyi/HcalNoiseTree/V00-03-12142/537p6/FT_P_V42D/HBHEYesHFNoHONo/000003/%s/%s"%(options.jobName,subFile))
    entries = chain.GetEntriesFast()
    
    # Make plot of individual channel occupancy as a function of #Vtx
    # Measure this slope as a function of iEta
    # Make plot of individual channel occupancy as a function of #Vtx, combining stats from all barrel channels,
    # and all endcap channels
    # make these plots as a function of the threshold on individual channel contributions (1.5/3/5 GeV)
    # have to add up these values to get the individual HPD occupancies
    # HPD is constructed from consecutive values in iEta and iPhi
    # HPD occupancy as a function of #Vtx
    # energy = numpy.array('d',[])
    # depth  = numpy.array('d',[])
    # iEta   = numpy.array('d',[])
    # iPhi   = numpy.array('d',[])
    
    # for jentry in xrange( entries ):
    #    # get the next tree in the chain
    #    ientry = chain.LoadTree(jentry)
    #    if ientry < 0:
    #        break
    hpdNames = [
        "HBP01_1","HBP01_2","HBP01_3","HBP01_4",
        "HBP02_1","HBP02_2","HBP02_3","HBP02_4",
        "HBP03_1","HBP03_2","HBP03_3","HBP03_4",
        "HBP04_1","HBP04_2","HBP04_3","HBP04_4",
        "HBP05_1","HBP05_2","HBP05_3","HBP05_4",
        "HBP06_1","HBP06_2","HBP06_3","HBP06_4",
        "HBP07_1","HBP07_2","HBP07_3","HBP07_4",
        "HBP08_1","HBP08_2","HBP08_3","HBP08_4",
        "HBP09_1","HBP09_2","HBP09_3","HBP09_4",
        "HBP10_1","HBP10_2","HBP10_3","HBP10_4",
        "HBP11_1","HBP11_2","HBP11_3","HBP11_4",
        "HBP12_1","HBP12_2","HBP12_3","HBP12_4",
        "HBP13_1","HBP13_2","HBP13_3","HBP13_4",
        "HBP14_1","HBP14_2","HBP14_3","HBP14_4",
        "HBP15_1","HBP15_2","HBP15_3","HBP15_4",
        "HBP16_1","HBP16_2","HBP16_3","HBP16_4",
        "HBM01_1","HBM01_2","HBM01_3","HBM01_4",
        "HBM02_1","HBM02_2","HBM02_3","HBM02_4",
        "HBM03_1","HBM03_2","HBM03_3","HBM03_4",
        "HBM04_1","HBM04_2","HBM04_3","HBM04_4",
        "HBM05_1","HBM05_2","HBM05_3","HBM05_4",
        "HBM06_1","HBM06_2","HBM06_3","HBM06_4",
        "HBM07_1","HBM07_2","HBM07_3","HBM07_4",
        "HBM08_1","HBM08_2","HBM08_3","HBM08_4",
        "HBM09_1","HBM09_2","HBM09_3","HBM09_4",
        "HBM10_1","HBM10_2","HBM10_3","HBM10_4",
        "HBM11_1","HBM11_2","HBM11_3","HBM11_4",
        "HBM12_1","HBM12_2","HBM12_3","HBM12_4",
        "HBM13_1","HBM13_2","HBM13_3","HBM13_4",
        "HBM14_1","HBM14_2","HBM14_3","HBM14_4",
        "HBM15_1","HBM15_2","HBM15_3","HBM15_4",
        "HBM16_1","HBM16_2","HBM16_3","HBM16_4",
        
        "HEP01_1","HEP01_2","HEP01_3","HEP01_4",
        "HEP02_1","HEP02_2","HEP02_3","HEP02_4",
        "HEP03_1","HEP03_2","HEP03_3","HEP03_4",
        "HEP04_1","HEP04_2","HEP04_3","HEP04_4",
        "HEP05_1","HEP05_2","HEP05_3","HEP05_4",
        "HEP06_1","HEP06_2","HEP06_3","HEP06_4",
        "HEP07_1","HEP07_2","HEP07_3","HEP07_4",
        "HEP08_1","HEP08_2","HEP08_3","HEP08_4",
        "HEP09_1","HEP09_2","HEP09_3","HEP09_4",
        "HEP10_1","HEP10_2","HEP10_3","HEP10_4",
        "HEP11_1","HEP11_2","HEP11_3","HEP11_4",
        "HEP12_1","HEP12_2","HEP12_3","HEP12_4",
        "HEP13_1","HEP13_2","HEP13_3","HEP13_4",
        "HEP14_1","HEP14_2","HEP14_3","HEP14_4",
        "HEP15_1","HEP15_2","HEP15_3","HEP15_4",
        "HEP16_1","HEP16_2","HEP16_3","HEP16_4",
        "HEM01_1","HEM01_2","HEM01_3","HEM01_4",
        "HEM02_1","HEM02_2","HEM02_3","HEM02_4",
        "HEM03_1","HEM03_2","HEM03_3","HEM03_4",
        "HEM04_1","HEM04_2","HEM04_3","HEM04_4",
        "HEM05_1","HEM05_2","HEM05_3","HEM05_4",
        "HEM06_1","HEM06_2","HEM06_3","HEM06_4",
        "HEM07_1","HEM07_2","HEM07_3","HEM07_4",
        "HEM08_1","HEM08_2","HEM08_3","HEM08_4",
        "HEM09_1","HEM09_2","HEM09_3","HEM09_4",
        "HEM10_1","HEM10_2","HEM10_3","HEM10_4",
        "HEM11_1","HEM11_2","HEM11_3","HEM11_4",
        "HEM12_1","HEM12_2","HEM12_3","HEM12_4",
        "HEM13_1","HEM13_2","HEM13_3","HEM13_4",
        "HEM14_1","HEM14_2","HEM14_3","HEM14_4",
        "HEM15_1","HEM15_2","HEM15_3","HEM15_4",
        "HEM16_1","HEM16_2","HEM16_3","HEM16_4",
        ]

    # #testing##hpdHits = {}
    # #testing##for i in range(18):
    # #testing##    print"HBM%02d"%(i+1)
    # #testing##    print"HBP%02d"%(i+1)
    # #testing##    hpdHits["HBM%2d"%(i+1)] = {}
    # #testing##    hpdHits["HBP%2d"%(i+1)] = {}
    # #testing##    for j in range(4):
    # #testing##        hpdHits["HBM%2d"%(i+1)]["HPD%d"%(j+1)] = []
    # #testing##        hpdHits["HBP%2d"%(i+1)]["HPD%d"%(j+1)] = []
    # #testing##
    # #testing###dPhi = 1
    # #testing###if abs(iEta) > 20:
    # #testing###    dPhi = 2
    # #testing####iEta 16 to 20 has dPhi 1
    # #testing####iEta 21 to 28 has dPhi 2, alternating between hpds
    # #testing####iEta 29 has dPhi 2, on every HPD, alternating depths
    # #testing#### 22,24,26,28 on HPD 1,4
    # #testing#### 21,23,25,27 on HPD 2,3
    # #testing#### (iPhi+71) mod 71
    # #testing##for ip in range(72):
    # #testing##    myIPhi = ip+1
    # #testing##    print myIPhi, (myIPhi/2)%2, ((((myIPhi+1)%72)%4)+1), (myIPhi+71)%72
    # #testing##
    # #testing##for ie in range(-30,29):
    # #testing##    myIEta = ie+1
    # #testing##    for ip in range(72):
    # #testing##        myIPhi = ip+1
    # #testing##        map_channel_to_hpd(myIEta,myIPhi,1)
    # #testing##        map_channel_to_hpd(myIEta,myIPhi,2)
    # #testing##        map_channel_to_hpd(myIEta,myIPhi,3)
    # #testing##        #print myIEta,myIPhi, (myIPhi+1)%72, ((((myIPhi+1)%72)%4)+1), map_channel_to_hpd(myIEta,myIPhi,1)
    # #as HPD index increases, iPhi decreases, starts with {71,72,1,2}
    # #HB/EM increases, starting from 71
    # #HB/EP increases, starting from 71
    # #HBP01 71,72,1,2
    # #HPB02 3,4,5,6
    # ##def __construct_hpd_occupancy__
    # ##
    # ##
    
    outFile = r.TFile("%s_%s_v2.root"%(options.jobName,
                                       options.outFileName
                                       ),
                      "RECREATE")
    hpdInfo = setup_hpd_histograms(outFile)
    #print hpdInfo
    decade  = 0
    century = 0
    tsw = r.TStopwatch()
    tenpcount = 1
    onepcount = 1
    
    
    nentries = chain.GetEntries()
    print "chain nentries %d"%(nentries)
    sys.stdout.flush()
    i = 0
    
    for event in chain:
        # ==============print number of events done == == == == == == == =
        if ( i==0):
            tsw.Start()
        # print('.', end='')
            sys.stdout.write('.')
            sys.stdout.flush()
        if ((i*10)/nentries == tenpcount ) :
            tsw.Stop()
            time = tsw.RealTime()
            tsw.Start(r.kFALSE)
            finTime = 0.
            frac = (i*1.0)/(nentries*1.0)
            if (frac>0):
                finTime = time / frac - time
                finMin = finTime / 60.
                sys.stdout.write("%d%% done.  "%(tenpcount*10))
                # sys.stdout.write("t=7.2f"%(time))
                sys.stdout.write("t="+str(time))
                sys.stdout.write(" projected finish=%7d s("%(finTime))
                sys.stdout.write("%2.2f min).   "%(finMin))
                sys.stdout.write("\n")
                sys.stdout.flush()
                tenpcount = tenpcount + 1
                
        elif ( (i*100)/nentries == onepcount ) :
            # print('.', end='')
            sys.stdout.write('.')
            sys.stdout.flush()
            onepcount = onepcount + 1

        #if i > 10000:
        #    break
        i = i + 1

        # # Do the analysis part
        hpdInfo = reset_hpd_counters(hpdInfo)
        
        hpdHits = event.HPDHits
        energy = numpy.array(event.Energy)
        depth  = numpy.array(event.Depth)
        iEta   = numpy.array(event.IEta)
        iPhi   = numpy.array(event.IPhi)
        nVtx   = event.NumberOfGoodPrimaryVertices
        # print energy,depth,iEta,iPhi
        # print energy[0],depth[0],iEta[0],iPhi[0]
        for idx,enVal in enumerate(energy):
            # if idx < 10:
            #    print nVtx,idx,enVal,energy[idx],depth[idx],iEta[idx],iPhi[idx]
            
            if depth[idx] == 0 or iEta[idx] == 0 or iPhi[idx] == 0:
                continue
            
            thisHPDIndex =  map_channel_to_hpd(iEta[idx],iPhi[idx],depth[idx])

            absEta = abs(iEta[idx])
            theDepth = depth[idx]
            isBarrel = False
            if absEta < 16:
                isBarrel = True
            elif absEta == 16 and theDepth < 3:
                isBarrel = True
            plus = False
            minus = False
            if iEta[idx] > 0:
                plus  = True
                minus = False
            if iEta[idx] < 0:
                plus  = False
                minus = True
            if enVal > 0:
                
                if options.debug and absEta == 28:
                    print nVtx,idx,enVal,energy[idx],iEta[idx],iPhi[idx],depth[idx],thisHPDIndex
                    
                hpdInfo[thisHPDIndex]["hits"] = hpdInfo[thisHPDIndex]["hits"] + 1
                hpdInfo["rechitoccupancy"]["overall"]["rechits"] = hpdInfo["rechitoccupancy"]["overall"]["rechits"] + 1
                if plus:
                    hpdInfo["rechitenergy"]["rechits_energy_ieta%dp_d%d"%(absEta,theDepth)]  .Fill(enVal)
                    hpdInfo["rechitoccupancy"]["etahists"]["rechits_ieta%dp_d%d"%(absEta,theDepth)] = hpdInfo["rechitoccupancy"]["etahists"]["rechits_ieta%dp_d%d"%(absEta,theDepth)] + 1
                    if isBarrel:
                        hpdInfo["rechitoccupancy"][0]["rechits"] = hpdInfo["rechitoccupancy"][0]["rechits"] + 1
                    else:
                        hpdInfo["rechitoccupancy"][2]["rechits"] = hpdInfo["rechitoccupancy"][2]["rechits"] + 1
                elif minus:
                    hpdInfo["rechitenergy"]["rechits_energy_ieta%dm_d%d"%(absEta,theDepth)]  .Fill(enVal)
                    hpdInfo["rechitoccupancy"]["etahists"]["rechits_ieta%dm_d%d"%(absEta,theDepth)] = hpdInfo["rechitoccupancy"]["etahists"]["rechits_ieta%dm_d%d"%(absEta,theDepth)] + 1
                    if isBarrel:
                        hpdInfo["rechitoccupancy"][1]["rechits"] = hpdInfo["rechitoccupancy"][1]["rechits"] + 1
                    else:
                        hpdInfo["rechitoccupancy"][3]["rechits"] = hpdInfo["rechitoccupancy"][3]["rechits"] + 1
                #if isBarrel:
                #    hpdInfo["rechitoccupancy"]["Barrel"]["rechits"] = hpdInfo["rechitoccupancy"]["Barrel"]["rechits"] + 1
                #else:
                #    hpdInfo["rechitoccupancy"]["Endcap"]["rechits"] = hpdInfo["rechitoccupancy"]["Endcap"]["rechits"] + 1

                if enVal < 1.5:
                    hpdInfo[thisHPDIndex]["hitsto15"] = hpdInfo[thisHPDIndex]["hitsto15"] + 1
                    hpdInfo["rechitoccupancy"]["overall"]["rechitsto15"] = hpdInfo["rechitoccupancy"]["overall"]["rechitsto15"] + 1
                    if plus:
                        hpdInfo["rechitenergy"]["rechitsto15_energy_ieta%dp_d%d"%(absEta,theDepth)].Fill(enVal)
                        hpdInfo["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dp_d%d"%(absEta,theDepth)] = hpdInfo["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dp_d%d"%(absEta,theDepth)] + 1
                        if isBarrel:
                            hpdInfo["rechitoccupancy"][0]["rechitsto15"] = hpdInfo["rechitoccupancy"][0]["rechitsto15"] + 1
                        else:
                            hpdInfo["rechitoccupancy"][2]["rechitsto15"] = hpdInfo["rechitoccupancy"][2]["rechitsto15"] + 1
                    elif minus:
                        hpdInfo["rechitenergy"]["rechitsto15_energy_ieta%dm_d%d"%(absEta,theDepth)].Fill(enVal)
                        hpdInfo["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dm_d%d"%(absEta,theDepth)] = hpdInfo["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dm_d%d"%(absEta,theDepth)] + 1
                        if isBarrel:
                            hpdInfo["rechitoccupancy"][1]["rechitsto15"] = hpdInfo["rechitoccupancy"][1]["rechitsto15"] + 1
                        else:
                            hpdInfo["rechitoccupancy"][3]["rechitsto15"] = hpdInfo["rechitoccupancy"][3]["rechitsto15"] + 1
                    # if isBarrel:
                    #     hpdInfo["rechitoccupancy"]["Barrel"]["rechitsto15"] = hpdInfo["rechitoccupancy"]["Barrel"]["rechitsto15"] + 1
                    # else:
                    #     hpdInfo["rechitoccupancy"]["Endcap"]["rechitsto15"] = hpdInfo["rechitoccupancy"]["Endcap"]["rechitsto15"] + 1
                elif enVal > 1.5:
                    hpdInfo[thisHPDIndex]["hits15"] = hpdInfo[thisHPDIndex]["hits15"] + 1
                    hpdInfo["rechitoccupancy"]["overall"]["rechits15"] = hpdInfo["rechitoccupancy"]["overall"]["rechits15"] + 1
                    if plus:
                        hpdInfo["rechitenergy"]["rechits15_energy_ieta%dp_d%d"%(absEta,theDepth)].Fill(enVal)
                        hpdInfo["rechitoccupancy"]["etahists"]["rechits15_ieta%dp_d%d"%(absEta,theDepth)] = hpdInfo["rechitoccupancy"]["etahists"]["rechits15_ieta%dp_d%d"%(absEta,theDepth)] + 1
                        if isBarrel:
                            hpdInfo["rechitoccupancy"][0]["rechits15"] = hpdInfo["rechitoccupancy"][0]["rechits15"] + 1
                        else:
                            hpdInfo["rechitoccupancy"][2]["rechits15"] = hpdInfo["rechitoccupancy"][2]["rechits15"] + 1
                    elif minus:
                        hpdInfo["rechitenergy"]["rechits15_energy_ieta%dm_d%d"%(absEta,theDepth)].Fill(enVal)
                        hpdInfo["rechitoccupancy"]["etahists"]["rechits15_ieta%dm_d%d"%(absEta,theDepth)] = hpdInfo["rechitoccupancy"]["etahists"]["rechits15_ieta%dm_d%d"%(absEta,theDepth)] + 1
                        if isBarrel:
                            hpdInfo["rechitoccupancy"][1]["rechits15"] = hpdInfo["rechitoccupancy"][1]["rechits15"] + 1
                        else:
                            hpdInfo["rechitoccupancy"][3]["rechits15"] = hpdInfo["rechitoccupancy"][3]["rechits15"] + 1
                    # if isBarrel:
                    #     hpdInfo["rechitoccupancy"]["Barrel"]["rechits15"] = hpdInfo["rechitoccupancy"]["Barrel"]["rechits15"] + 1
                    # else:
                    #     hpdInfo["rechitoccupancy"]["Endcap"]["rechits15"] = hpdInfo["rechitoccupancy"]["Endcap"]["rechits15"] + 1
                    if enVal < 3.0:
                        hpdInfo[thisHPDIndex]["hits15to30"] = hpdInfo[thisHPDIndex]["hits15to30"] + 1
                        hpdInfo["rechitoccupancy"]["overall"]["rechits15to30"] = hpdInfo["rechitoccupancy"]["overall"]["rechits15to30"] + 1
                        if plus:
                            hpdInfo["rechitenergy"]["rechits15to30_energy_ieta%dp_d%d"%(absEta,theDepth)].Fill(enVal)
                            hpdInfo["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dp_d%d"%(absEta,theDepth)] = hpdInfo["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dp_d%d"%(absEta,theDepth)] + 1
                            if isBarrel:
                                hpdInfo["rechitoccupancy"][0]["rechits15to30"] = hpdInfo["rechitoccupancy"][0]["rechits15to30"] + 1
                            else:
                                hpdInfo["rechitoccupancy"][2]["rechits15to30"] = hpdInfo["rechitoccupancy"][2]["rechits15to30"] + 1
                        elif minus:
                            hpdInfo["rechitenergy"]["rechits15to30_energy_ieta%dm_d%d"%(absEta,theDepth)].Fill(enVal)
                            hpdInfo["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dm_d%d"%(absEta,theDepth)] = hpdInfo["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dm_d%d"%(absEta,theDepth)] + 1
                            if isBarrel:
                                hpdInfo["rechitoccupancy"][1]["rechits15to30"] = hpdInfo["rechitoccupancy"][1]["rechits15to30"] + 1
                            else:
                                hpdInfo["rechitoccupancy"][3]["rechits15to30"] = hpdInfo["rechitoccupancy"][3]["rechits15to30"] + 1
                        # if isBarrel:
                        #     hpdInfo["rechitoccupancy"]["Barrel"]["rechits15to30"] = hpdInfo["rechitoccupancy"]["Barrel"]["rechits15to30"] + 1
                        # else:
                        #     hpdInfo["rechitoccupancy"]["Endcap"]["rechits15to30"] = hpdInfo["rechitoccupancy"]["Endcap"]["rechits15to30"] + 1
                    elif enVal > 3.0:
                        hpdInfo[thisHPDIndex]["hits30"] = hpdInfo[thisHPDIndex]["hits30"] + 1
                        hpdInfo["rechitoccupancy"]["overall"]["rechits30"] = hpdInfo["rechitoccupancy"]["overall"]["rechits30"] + 1
                        if plus:
                            hpdInfo["rechitenergy"]["rechits30_energy_ieta%dp_d%d"%(absEta,theDepth)].Fill(enVal)
                            hpdInfo["rechitoccupancy"]["etahists"]["rechits30_ieta%dp_d%d"%(absEta,theDepth)] = hpdInfo["rechitoccupancy"]["etahists"]["rechits30_ieta%dp_d%d"%(absEta,theDepth)] + 1
                            if isBarrel:
                                hpdInfo["rechitoccupancy"][0]["rechits30"] = hpdInfo["rechitoccupancy"][0]["rechits30"] + 1
                            else:
                                hpdInfo["rechitoccupancy"][2]["rechits30"] = hpdInfo["rechitoccupancy"][2]["rechits30"] + 1
                        elif minus:
                            hpdInfo["rechitenergy"]["rechits30_energy_ieta%dm_d%d"%(absEta,theDepth)].Fill(enVal)
                            hpdInfo["rechitoccupancy"]["etahists"]["rechits30_ieta%dm_d%d"%(absEta,theDepth)] = hpdInfo["rechitoccupancy"]["etahists"]["rechits30_ieta%dm_d%d"%(absEta,theDepth)] + 1
                            if isBarrel:
                                hpdInfo["rechitoccupancy"][1]["rechits30"] = hpdInfo["rechitoccupancy"][1]["rechits30"] + 1
                            else:
                                hpdInfo["rechitoccupancy"][3]["rechits30"] = hpdInfo["rechitoccupancy"][3]["rechits30"] + 1
                        # if isBarrel:
                        #     hpdInfo["rechitoccupancy"]["Barrel"]["rechits30"] = hpdInfo["rechitoccupancy"]["Barrel"]["rechits30"] + 1
                        # else:
                        #     hpdInfo["rechitoccupancy"]["Endcap"]["rechits30"] = hpdInfo["rechitoccupancy"]["Endcap"]["rechits30"] + 1
                        if enVal < 5.0:
                            hpdInfo[thisHPDIndex]["hits30to50"] = hpdInfo[thisHPDIndex]["hits30to50"] + 1
                            hpdInfo["rechitoccupancy"]["overall"]["rechits30to50"] = hpdInfo["rechitoccupancy"]["overall"]["rechits30to50"] + 1
                            if plus:
                                hpdInfo["rechitenergy"]["rechits30to50_energy_ieta%dp_d%d"%(absEta,theDepth)].Fill(enVal)
                                hpdInfo["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dp_d%d"%(absEta,theDepth)] = hpdInfo["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dp_d%d"%(absEta,theDepth)] + 1
                                if isBarrel:
                                    hpdInfo["rechitoccupancy"][0]["rechits30to50"] = hpdInfo["rechitoccupancy"][0]["rechits30to50"] + 1
                                else:
                                    hpdInfo["rechitoccupancy"][2]["rechits30to50"] = hpdInfo["rechitoccupancy"][2]["rechits30to50"] + 1
                            elif minus:
                                hpdInfo["rechitenergy"]["rechits30to50_energy_ieta%dm_d%d"%(absEta,theDepth)].Fill(enVal)
                                hpdInfo["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dm_d%d"%(absEta,theDepth)] = hpdInfo["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dm_d%d"%(absEta,theDepth)] + 1
                                if isBarrel:
                                    hpdInfo["rechitoccupancy"][1]["rechits30to50"] = hpdInfo["rechitoccupancy"][1]["rechits30to50"] + 1
                                else:
                                    hpdInfo["rechitoccupancy"][3]["rechits30to50"] = hpdInfo["rechitoccupancy"][3]["rechits30to50"] + 1
                            # if isBarrel:
                            #     hpdInfo["rechitoccupancy"]["Barrel"]["rechits30to50"] = hpdInfo["rechitoccupancy"]["Barrel"]["rechits30to50"] + 1
                            # else:
                            #     hpdInfo["rechitoccupancy"]["Endcap"]["rechits30to50"] = hpdInfo["rechitoccupancy"]["Endcap"]["rechits30to50"] + 1
                        elif enVal > 5.0:
                            hpdInfo[thisHPDIndex]["hits50"] = hpdInfo[thisHPDIndex]["hits50"] + 1
                            hpdInfo["rechitoccupancy"]["overall"]["rechits50"] = hpdInfo["rechitoccupancy"]["overall"]["rechits50"] + 1
                            if plus:
                                hpdInfo["rechitenergy"]["rechits50_energy_ieta%dp_d%d"%(absEta,theDepth)].Fill(enVal)
                                hpdInfo["rechitoccupancy"]["etahists"]["rechits50_ieta%dp_d%d"%(absEta,theDepth)] = hpdInfo["rechitoccupancy"]["etahists"]["rechits50_ieta%dp_d%d"%(absEta,theDepth)] + 1
                                if isBarrel:
                                    hpdInfo["rechitoccupancy"][0]["rechits50"] = hpdInfo["rechitoccupancy"][0]["rechits50"] + 1
                                else:
                                    hpdInfo["rechitoccupancy"][2]["rechits50"] = hpdInfo["rechitoccupancy"][2]["rechits50"] + 1
                            elif minus:
                                hpdInfo["rechitenergy"]["rechits50_energy_ieta%dm_d%d"%(absEta,theDepth)].Fill(enVal)
                                hpdInfo["rechitoccupancy"]["etahists"]["rechits50_ieta%dm_d%d"%(absEta,theDepth)] = hpdInfo["rechitoccupancy"]["etahists"]["rechits50_ieta%dm_d%d"%(absEta,theDepth)] + 1
                                if isBarrel:
                                    hpdInfo["rechitoccupancy"][1]["rechits50"] = hpdInfo["rechitoccupancy"][1]["rechits50"] + 1
                                else:
                                    hpdInfo["rechitoccupancy"][3]["rechits50"] = hpdInfo["rechitoccupancy"][3]["rechits50"] + 1
                            # if isBarrel:
                            #     hpdInfo["rechitoccupancy"]["Barrel"]["rechits50"] = hpdInfo["rechitoccupancy"]["Barrel"]["rechits50"] + 1
                            # else:
                            #     hpdInfo["rechitoccupancy"]["Endcap"]["rechits50"] = hpdInfo["rechitoccupancy"]["Endcap"]["rechits50"] + 1
    
        hpdInfo = fill_hpd_histograms(hpdInfo,nVtx)

    write_hpd_histograms(hpdInfo,outFile)
    outFile.Close()

#def __reconstruct_hpd_occupancy__
def setup_hpd_histograms(myFile):
    r.gROOT.SetBatch(True)
    hpdInformation = {}
    hpdInformation["summary"] = {}
    hpdInformation["rechitoccupancy"] = {}
    hpdInformation["rechitenergy"] = {}
    hpdIdx = 0
    subdetIdx = 0
    #for keyName in hpdNames:
    # individual occupancy for a given iEta value
    energyDir = myFile.mkdir("rechitenergy")
    rechitDir = myFile.mkdir("rechitoccupancy")
    rechitDir.cd()
    hpdInformation["rechitoccupancy"]["overall"] = {}
    hpdInformation["rechitoccupancy"]["overall"]["rechits_vs_nvtx"] = r.TH2D("rechits_vs_nvtx",
                                                                             "rechits_vs_nvtx",
                                                                             60,-0.5,59.5,1000,-0.5,999.5)
    hpdInformation["rechitoccupancy"]["overall"]["rechitsto15_vs_nvtx"] = r.TH2D("rechitsto15_vs_nvtx",
                                                                                 "rechitsto15_vs_nvtx",
                                                                                 60,-0.5,59.5,1000,-0.5,999.5)
    hpdInformation["rechitoccupancy"]["overall"]["rechits15_vs_nvtx"] = r.TH2D("rechits15_vs_nvtx",
                                                                               "rechits15_vs_nvtx",
                                                                               60,-0.5,59.5,1000,-0.5,999.5)
    hpdInformation["rechitoccupancy"]["overall"]["rechits15to30_vs_nvtx"] = r.TH2D("rechits15to30_vs_nvtx",
                                                                                   "rechits15to30_vs_nvtx",
                                                                                   60,-0.5,59.5,1000,-0.5,999.5)
    hpdInformation["rechitoccupancy"]["overall"]["rechits30_vs_nvtx"] = r.TH2D("rechits30_vs_nvtx",
                                                                               "rechits30_vs_nvtx",
                                                                               60,-0.5,59.5,500,-0.5,499.5)
    hpdInformation["rechitoccupancy"]["overall"]["rechits30to50_vs_nvtx"] = r.TH2D("rechits30to50_vs_nvtx",
                                                                                   "rechits30to50_vs_nvtx",
                                                                                   60,-0.5,59.5,500,-0.5,499.5)
    hpdInformation["rechitoccupancy"]["overall"]["rechits50_vs_nvtx"] = r.TH2D("rechits50_vs_nvtx",
                                                                               "rechits50_vs_nvtx",
                                                                               60,-0.5,59.5,300,-0.5,299.5)
    
    hpdInformation["rechitoccupancy"]["overall"]["rechits"]   = 0
    hpdInformation["rechitoccupancy"]["overall"]["rechitsto15"] = 0
    hpdInformation["rechitoccupancy"]["overall"]["rechits15"] = 0
    hpdInformation["rechitoccupancy"]["overall"]["rechits15to30"] = 0
    hpdInformation["rechitoccupancy"]["overall"]["rechits30"] = 0
    hpdInformation["rechitoccupancy"]["overall"]["rechits30to50"] = 0
    hpdInformation["rechitoccupancy"]["overall"]["rechits50"] = 0
    hpdInformation["rechitoccupancy"]["overall"]["rechits_vs_nvtx"]  .Sumw2()
    hpdInformation["rechitoccupancy"]["overall"]["rechitsto15_vs_nvtx"].Sumw2()
    hpdInformation["rechitoccupancy"]["overall"]["rechits15_vs_nvtx"].Sumw2()
    hpdInformation["rechitoccupancy"]["overall"]["rechits15to30_vs_nvtx"].Sumw2()
    hpdInformation["rechitoccupancy"]["overall"]["rechits30_vs_nvtx"].Sumw2()
    hpdInformation["rechitoccupancy"]["overall"]["rechits30to50_vs_nvtx"].Sumw2()
    hpdInformation["rechitoccupancy"]["overall"]["rechits50_vs_nvtx"].Sumw2()
    
    for be in ["Barrel","Endcap"]:
        outputDir = rechitDir.mkdir(be)
        outputDir.cd()
        hpdInformation["rechitoccupancy"][be] = {}
        hpdInformation["rechitoccupancy"][be]["rechits_vs_nvtx"] = r.TH2D("rechits_vs_nvtx_%s"%(be),
                                                                          "rechits_vs_nvtx_%s"%(be),
                                                                          60,-0.5,59.5,1000,-0.5,999.5)
        hpdInformation["rechitoccupancy"][be]["rechitsto15_vs_nvtx"] = r.TH2D("rechitsto15_vs_nvtx_%s"%(be),
                                                                              "rechitsto15_vs_nvtx_%s"%(be),
                                                                              60,-0.5,59.5,500,-0.5,499.5)
        hpdInformation["rechitoccupancy"][be]["rechits15_vs_nvtx"] = r.TH2D("rechits15_vs_nvtx_%s"%(be),
                                                                            "rechits15_vs_nvtx_%s"%(be),
                                                                            60,-0.5,59.5,500,-0.5,499.5)
        hpdInformation["rechitoccupancy"][be]["rechits15to30_vs_nvtx"] = r.TH2D("rechits15to30_vs_nvtx_%s"%(be),
                                                                                "rechits15to30_vs_nvtx_%s"%(be),
                                                                                60,-0.5,59.5,500,-0.5,499.5)
        hpdInformation["rechitoccupancy"][be]["rechits30_vs_nvtx"] = r.TH2D("rechits30_vs_nvtx_%s"%(be),
                                                                            "rechits30_vs_nvtx_%s"%(be),
                                                                            60,-0.5,59.5,300,-0.5,299.5)
        hpdInformation["rechitoccupancy"][be]["rechits30to50_vs_nvtx"] = r.TH2D("rechits30to50_vs_nvtx_%s"%(be),
                                                                                "rechits30to50_vs_nvtx_%s"%(be),
                                                                                60,-0.5,59.5,300,-0.5,299.5)
        hpdInformation["rechitoccupancy"][be]["rechits50_vs_nvtx"] = r.TH2D("rechits50_vs_nvtx_%s"%(be),
                                                                            "rechits50_vs_nvtx_%s"%(be),
                                                                            60,-0.5,59.5,200,-0.5,199.5)
        
        #hpdInformation["rechitoccupancy"][be]["rechits"]   = 0
        #hpdInformation["rechitoccupancy"][be]["rechits15"] = 0
        #hpdInformation["rechitoccupancy"][be]["rechits30"] = 0
        #hpdInformation["rechitoccupancy"][be]["rechits50"] = 0
        hpdInformation["rechitoccupancy"][be]["rechits_vs_nvtx"]  .Sumw2()
        hpdInformation["rechitoccupancy"][be]["rechitsto15_vs_nvtx"].Sumw2()
        hpdInformation["rechitoccupancy"][be]["rechits15_vs_nvtx"].Sumw2()
        hpdInformation["rechitoccupancy"][be]["rechits15to30_vs_nvtx"].Sumw2()
        hpdInformation["rechitoccupancy"][be]["rechits30_vs_nvtx"].Sumw2()
        hpdInformation["rechitoccupancy"][be]["rechits30to50_vs_nvtx"].Sumw2()
        hpdInformation["rechitoccupancy"][be]["rechits50_vs_nvtx"].Sumw2()
            

    hpdInformation["rechitoccupancy"]["etahists"] = {}
    etaDir = rechitDir.mkdir("etahists")
    etaDir.cd()
    for ieta in range(29):
        theEta = ieta + 1
        for depth in range(3):
            if theEta < 15 and depth > 0:
                # barrel has max depth==1
                continue
            elif theEta < 16 and depth > 1:
                # iEta 15 has max depth==2
                continue
            elif theEta == 17 and depth > 0:
                # iEta 17 has depth 1 only
                continue
            elif theEta > 17 and theEta < 27 and depth > 1:
                # iEta 18-26 have max depth==2
                continue
            elif theEta > 28 and depth > 1:
                # iEta 29 have max depth==2
                continue
            # iEta 16,27,28 have max depth==3
            
            etaDir.cd()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)] = r.TH2D("rechits_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                   "rechits_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                   60,-0.5,59.5,75,-0.5,74.5)
            hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)] = r.TH2D("rechitsto15_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                       "rechitsto15_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                       60,-0.5,59.5,75,-0.5,74.5)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)] = r.TH2D("rechits15_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                     "rechits15_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                     60,-0.5,59.5,75,-0.5,74.5)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)] = r.TH2D("rechits15to30_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                         "rechits15to30_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                         60,-0.5,59.5,75,-0.5,74.5)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)] = r.TH2D("rechits30_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                     "rechits30_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                     60,-0.5,59.5,75,-0.5,74.5)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)] = r.TH2D("rechits30to50_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                         "rechits30to50_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                         60,-0.5,59.5,75,-0.5,74.5)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)] = r.TH2D("rechits50_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                     "rechits50_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                     60,-0.5,59.5,75,-0.5,74.5)
            
            hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%dp_d%d"%(ieta+1,depth+1)]   = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dp_d%d"%(ieta+1,depth+1)] = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%dp_d%d"%(ieta+1,depth+1)] = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dp_d%d"%(ieta+1,depth+1)] = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%dp_d%d"%(ieta+1,depth+1)] = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dp_d%d"%(ieta+1,depth+1)] = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%dp_d%d"%(ieta+1,depth+1)] = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)]  .Sumw2()
            hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)].Sumw2()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)].Sumw2()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)].Sumw2()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)].Sumw2()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)].Sumw2()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)].Sumw2()
            
            hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)] = r.TH2D("rechits_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                   "rechits_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                   60,-0.5,59.5,75,-0.5,74.5)
            hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)] = r.TH2D("rechitsto15_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                       "rechitsto15_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                       60,-0.5,59.5,75,-0.5,74.5)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)] = r.TH2D("rechits15_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                     "rechits15_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                     60,-0.5,59.5,75,-0.5,74.5)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)] = r.TH2D("rechits15to30_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                         "rechits15to30_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                         60,-0.5,59.5,75,-0.5,74.5)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)] = r.TH2D("rechits30_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                     "rechits30_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                     60,-0.5,59.5,75,-0.5,74.5)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)] = r.TH2D("rechits30to50_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                         "rechits30to50_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                         60,-0.5,59.5,75,-0.5,74.5)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)] = r.TH2D("rechits50_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                     "rechits50_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                     60,-0.5,59.5,75,-0.5,74.5)
            
            hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%dm_d%d"%(ieta+1,depth+1)]   = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dm_d%d"%(ieta+1,depth+1)] = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%dm_d%d"%(ieta+1,depth+1)] = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dm_d%d"%(ieta+1,depth+1)] = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%dm_d%d"%(ieta+1,depth+1)] = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dm_d%d"%(ieta+1,depth+1)] = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%dm_d%d"%(ieta+1,depth+1)] = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)]  .Sumw2()
            hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)].Sumw2()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)].Sumw2()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)].Sumw2()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)].Sumw2()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)].Sumw2()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)].Sumw2()
            
            hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)] = r.TH2D("rechits_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                  "rechits_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                  60,-0.5,59.5,75,-0.5,74.5)
            hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)] = r.TH2D("rechitsto15_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                      "rechitsto15_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                      60,-0.5,59.5,75,-0.5,74.5)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)] = r.TH2D("rechits15_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                    "rechits15_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                    60,-0.5,59.5,75,-0.5,74.5)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)] = r.TH2D("rechits15to30_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                        "rechits15to30_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                        60,-0.5,59.5,75,-0.5,74.5)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)] = r.TH2D("rechits30_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                    "rechits30_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                    60,-0.5,59.5,75,-0.5,74.5)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)] = r.TH2D("rechits30to50_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                        "rechits30to50_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                        60,-0.5,59.5,75,-0.5,74.5)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)] = r.TH2D("rechits50_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                    "rechits50_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1),
                                                                                                                    60,-0.5,59.5,75,-0.5,74.5)
            
            hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)]  .Sumw2()
            hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)].Sumw2()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)].Sumw2()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)].Sumw2()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)].Sumw2()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)].Sumw2()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)].Sumw2()

            # ## individual rechit energies
            energyDir.cd()
            hpdInformation["rechitenergy"]["rechits_energy_ieta%dp_d%d"%(ieta+1,depth+1)] = r.TH1D("rechits_energy_ieta%dp_d%d"%(ieta+1,depth+1),
                                                                                                   "rechits_energy_ieta%dp_d%d"%(ieta+1,depth+1),
                                                                                                   500,0,50)
            hpdInformation["rechitenergy"]["rechitsto15_energy_ieta%dp_d%d"%(ieta+1,depth+1)] = r.TH1D("rechitsto15_energy_ieta%dp_d%d"%(ieta+1,depth+1),
                                                                                                       "rechitsto15_energy_ieta%dp_d%d"%(ieta+1,depth+1),
                                                                                                       500,0,50)
            hpdInformation["rechitenergy"]["rechits15_energy_ieta%dp_d%d"%(ieta+1,depth+1)] = r.TH1D("rechits15_energy_ieta%dp_d%d"%(ieta+1,depth+1),
                                                                                                     "rechits15_energy_ieta%dp_d%d"%(ieta+1,depth+1),
                                                                                                     500,0,50)
            hpdInformation["rechitenergy"]["rechits15to30_energy_ieta%dp_d%d"%(ieta+1,depth+1)] = r.TH1D("rechits15to30_energy_ieta%dp_d%d"%(ieta+1,depth+1),
                                                                                                         "rechits15to30_energy_ieta%dp_d%d"%(ieta+1,depth+1),
                                                                                                         500,0,50)
            hpdInformation["rechitenergy"]["rechits30_energy_ieta%dp_d%d"%(ieta+1,depth+1)] = r.TH1D("rechits30_energy_ieta%dp_d%d"%(ieta+1,depth+1),
                                                                                                     "rechits30_energy_ieta%dp_d%d"%(ieta+1,depth+1),
                                                                                                     500,0,50)
            hpdInformation["rechitenergy"]["rechits30to50_energy_ieta%dp_d%d"%(ieta+1,depth+1)] = r.TH1D("rechits30to50_energy_ieta%dp_d%d"%(ieta+1,depth+1),
                                                                                                         "rechits30to50_energy_ieta%dp_d%d"%(ieta+1,depth+1),
                                                                                                         500,0,50)
            hpdInformation["rechitenergy"]["rechits50_energy_ieta%dp_d%d"%(ieta+1,depth+1)] = r.TH1D("rechits50_energy_ieta%dp_d%d"%(ieta+1,depth+1),
                                                                                                     "rechits50_energy_ieta%dp_d%d"%(ieta+1,depth+1),
                                                                                                     500,0,50)
            
            hpdInformation["rechitenergy"]["rechits_energy_ieta%dp_d%d"%(ieta+1,depth+1)]  .Sumw2()
            hpdInformation["rechitenergy"]["rechitsto15_energy_ieta%dp_d%d"%(ieta+1,depth+1)].Sumw2()
            hpdInformation["rechitenergy"]["rechits15_energy_ieta%dp_d%d"%(ieta+1,depth+1)].Sumw2()
            hpdInformation["rechitenergy"]["rechits15to30_energy_ieta%dp_d%d"%(ieta+1,depth+1)].Sumw2()
            hpdInformation["rechitenergy"]["rechits30_energy_ieta%dp_d%d"%(ieta+1,depth+1)].Sumw2()
            hpdInformation["rechitenergy"]["rechits30to50_energy_ieta%dp_d%d"%(ieta+1,depth+1)].Sumw2()
            hpdInformation["rechitenergy"]["rechits50_energy_ieta%dp_d%d"%(ieta+1,depth+1)].Sumw2()
            
            hpdInformation["rechitenergy"]["rechits_energy_ieta%dm_d%d"%(ieta+1,depth+1)] = r.TH1D("rechits_energy_ieta%dm_d%d"%(ieta+1,depth+1),
                                                                                                   "rechits_energy_ieta%dm_d%d"%(ieta+1,depth+1),
                                                                                                   500,0,50)
            hpdInformation["rechitenergy"]["rechitsto15_energy_ieta%dm_d%d"%(ieta+1,depth+1)] = r.TH1D("rechitsto15_energy_ieta%dm_d%d"%(ieta+1,depth+1),
                                                                                                       "rechitsto15_energy_ieta%dm_d%d"%(ieta+1,depth+1),
                                                                                                       500,0,50)
            hpdInformation["rechitenergy"]["rechits15_energy_ieta%dm_d%d"%(ieta+1,depth+1)] = r.TH1D("rechits15_energy_ieta%dm_d%d"%(ieta+1,depth+1),
                                                                                                     "rechits15_energy_ieta%dm_d%d"%(ieta+1,depth+1),
                                                                                                     500,0,50)
            hpdInformation["rechitenergy"]["rechits15to30_energy_ieta%dm_d%d"%(ieta+1,depth+1)] = r.TH1D("rechits15to30_energy_ieta%dm_d%d"%(ieta+1,depth+1),
                                                                                                         "rechits15to30_energy_ieta%dm_d%d"%(ieta+1,depth+1),
                                                                                                         500,0,50)
            hpdInformation["rechitenergy"]["rechits30_energy_ieta%dm_d%d"%(ieta+1,depth+1)] = r.TH1D("rechits30_energy_ieta%dm_d%d"%(ieta+1,depth+1),
                                                                                                     "rechits30_energy_ieta%dm_d%d"%(ieta+1,depth+1),
                                                                                                     500,0,50)
            hpdInformation["rechitenergy"]["rechits30to50_energy_ieta%dm_d%d"%(ieta+1,depth+1)] = r.TH1D("rechits30to50_energy_ieta%dm_d%d"%(ieta+1,depth+1),
                                                                                                         "rechits30to50_energy_ieta%dm_d%d"%(ieta+1,depth+1),
                                                                                                         500,0,50)
            hpdInformation["rechitenergy"]["rechits50_energy_ieta%dm_d%d"%(ieta+1,depth+1)] = r.TH1D("rechits50_energy_ieta%dm_d%d"%(ieta+1,depth+1),
                                                                                                     "rechits50_energy_ieta%dm_d%d"%(ieta+1,depth+1),
                                                                                                     500,0,50)
            
            hpdInformation["rechitenergy"]["rechits_energy_ieta%dm_d%d"%(ieta+1,depth+1)]  .Sumw2()
            hpdInformation["rechitenergy"]["rechitsto15_energy_ieta%dm_d%d"%(ieta+1,depth+1)].Sumw2()
            hpdInformation["rechitenergy"]["rechits15_energy_ieta%dm_d%d"%(ieta+1,depth+1)].Sumw2()
            hpdInformation["rechitenergy"]["rechits15to30_energy_ieta%dm_d%d"%(ieta+1,depth+1)].Sumw2()
            hpdInformation["rechitenergy"]["rechits30_energy_ieta%dm_d%d"%(ieta+1,depth+1)].Sumw2()
            hpdInformation["rechitenergy"]["rechits30to50_energy_ieta%dm_d%d"%(ieta+1,depth+1)].Sumw2()
            hpdInformation["rechitenergy"]["rechits50_energy_ieta%dm_d%d"%(ieta+1,depth+1)].Sumw2()
            

        # Only the sum of all depths at a given ieta value
        etaDir.cd()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%dp_vs_nvtx"%(ieta+1)] = r.TH2D("rechits_ieta%dp_vs_nvtx"%(ieta+1),
                                                                                                   "rechits_ieta%dp_vs_nvtx"%(ieta+1),
                                                                                                   60,-0.5,59.5,250,-0.5,249.5)
        hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dp_vs_nvtx"%(ieta+1)] = r.TH2D("rechitsto15_ieta%dp_vs_nvtx"%(ieta+1),
                                                                                                       "rechitsto15_ieta%dp_vs_nvtx"%(ieta+1),
                                                                                                       60,-0.5,59.5,250,-0.5,249.5)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%dp_vs_nvtx"%(ieta+1)] = r.TH2D("rechits15_ieta%dp_vs_nvtx"%(ieta+1),
                                                                                                     "rechits15_ieta%dp_vs_nvtx"%(ieta+1),
                                                                                                     60,-0.5,59.5,250,-0.5,249.5)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dp_vs_nvtx"%(ieta+1)] = r.TH2D("rechits15to30_ieta%dp_vs_nvtx"%(ieta+1),
                                                                                                         "rechits15to30_ieta%dp_vs_nvtx"%(ieta+1),
                                                                                                         60,-0.5,59.5,250,-0.5,249.5)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%dp_vs_nvtx"%(ieta+1)] = r.TH2D("rechits30_ieta%dp_vs_nvtx"%(ieta+1),
                                                                                                     "rechits30_ieta%dp_vs_nvtx"%(ieta+1),
                                                                                                     60,-0.5,59.5,250,-0.5,249.5)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dp_vs_nvtx"%(ieta+1)] = r.TH2D("rechits30to50_ieta%dp_vs_nvtx"%(ieta+1),
                                                                                                         "rechits30to50_ieta%dp_vs_nvtx"%(ieta+1),
                                                                                                         60,-0.5,59.5,250,-0.5,249.5)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%dp_vs_nvtx"%(ieta+1)] = r.TH2D("rechits50_ieta%dp_vs_nvtx"%(ieta+1),
                                                                                                     "rechits50_ieta%dp_vs_nvtx"%(ieta+1),
                                                                                                     60,-0.5,59.5,250,-0.5,249.5)
        
        hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%dp_vs_nvtx"%(ieta+1)]  .Sumw2()
        hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dp_vs_nvtx"%(ieta+1)].Sumw2()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%dp_vs_nvtx"%(ieta+1)].Sumw2()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dp_vs_nvtx"%(ieta+1)].Sumw2()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%dp_vs_nvtx"%(ieta+1)].Sumw2()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dp_vs_nvtx"%(ieta+1)].Sumw2()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%dp_vs_nvtx"%(ieta+1)].Sumw2()
        
        hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%dm_vs_nvtx"%(ieta+1)] = r.TH2D("rechits_ieta%dm_vs_nvtx"%(ieta+1),
                                                                                                   "rechits_ieta%dm_vs_nvtx"%(ieta+1),
                                                                                                   60,-0.5,59.5,250,-0.5,249.5)
        hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dm_vs_nvtx"%(ieta+1)] = r.TH2D("rechitsto15_ieta%dm_vs_nvtx"%(ieta+1),
                                                                                                       "rechitsto15_ieta%dm_vs_nvtx"%(ieta+1),
                                                                                                       60,-0.5,59.5,250,-0.5,249.5)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%dm_vs_nvtx"%(ieta+1)] = r.TH2D("rechits15_ieta%dm_vs_nvtx"%(ieta+1),
                                                                                                     "rechits15_ieta%dm_vs_nvtx"%(ieta+1),
                                                                                                     60,-0.5,59.5,250,-0.5,249.5)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dm_vs_nvtx"%(ieta+1)] = r.TH2D("rechits15to30_ieta%dm_vs_nvtx"%(ieta+1),
                                                                                                         "rechits15to30_ieta%dm_vs_nvtx"%(ieta+1),
                                                                                                         60,-0.5,59.5,250,-0.5,249.5)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%dm_vs_nvtx"%(ieta+1)] = r.TH2D("rechits30_ieta%dm_vs_nvtx"%(ieta+1),
                                                                                                     "rechits30_ieta%dm_vs_nvtx"%(ieta+1),
                                                                                                     60,-0.5,59.5,250,-0.5,249.5)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dm_vs_nvtx"%(ieta+1)] = r.TH2D("rechits30to50_ieta%dm_vs_nvtx"%(ieta+1),
                                                                                                         "rechits30to50_ieta%dm_vs_nvtx"%(ieta+1),
                                                                                                         60,-0.5,59.5,250,-0.5,249.5)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%dm_vs_nvtx"%(ieta+1)] = r.TH2D("rechits50_ieta%dm_vs_nvtx"%(ieta+1),
                                                                                                     "rechits50_ieta%dm_vs_nvtx"%(ieta+1),
                                                                                                     60,-0.5,59.5,250,-0.5,249.5)
        
        hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%dm_vs_nvtx"%(ieta+1)]  .Sumw2()
        hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dm_vs_nvtx"%(ieta+1)].Sumw2()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%dm_vs_nvtx"%(ieta+1)].Sumw2()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dm_vs_nvtx"%(ieta+1)].Sumw2()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%dm_vs_nvtx"%(ieta+1)].Sumw2()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dm_vs_nvtx"%(ieta+1)].Sumw2()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%dm_vs_nvtx"%(ieta+1)].Sumw2()
        
        hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%d_vs_nvtx"%(ieta+1)] = r.TH2D("rechits_ieta%d_vs_nvtx"%(ieta+1),
                                                                                                  "rechits_ieta%d_vs_nvtx"%(ieta+1),
                                                                                                  60,-0.5,59.5,250,-0.5,249.5)
        hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%d_vs_nvtx"%(ieta+1)] = r.TH2D("rechitsto15_ieta%d_vs_nvtx"%(ieta+1),
                                                                                                      "rechitsto15_ieta%d_vs_nvtx"%(ieta+1),
                                                                                                      60,-0.5,59.5,250,-0.5,249.5)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%d_vs_nvtx"%(ieta+1)] = r.TH2D("rechits15_ieta%d_vs_nvtx"%(ieta+1),
                                                                                                    "rechits15_ieta%d_vs_nvtx"%(ieta+1),
                                                                                                    60,-0.5,59.5,250,-0.5,249.5)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%d_vs_nvtx"%(ieta+1)] = r.TH2D("rechits15to30_ieta%d_vs_nvtx"%(ieta+1),
                                                                                                        "rechits15to30_ieta%d_vs_nvtx"%(ieta+1),
                                                                                                        60,-0.5,59.5,250,-0.5,249.5)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%d_vs_nvtx"%(ieta+1)] = r.TH2D("rechits30_ieta%d_vs_nvtx"%(ieta+1),
                                                                                                    "rechits30_ieta%d_vs_nvtx"%(ieta+1),
                                                                                                    60,-0.5,59.5,250,-0.5,249.5)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%d_vs_nvtx"%(ieta+1)] = r.TH2D("rechits30to50_ieta%d_vs_nvtx"%(ieta+1),
                                                                                                        "rechits30to50_ieta%d_vs_nvtx"%(ieta+1),
                                                                                                        60,-0.5,59.5,250,-0.5,249.5)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%d_vs_nvtx"%(ieta+1)] = r.TH2D("rechits50_ieta%d_vs_nvtx"%(ieta+1),
                                                                                                    "rechits50_ieta%d_vs_nvtx"%(ieta+1),
                                                                                                    60,-0.5,59.5,250,-0.5,249.5)
        
        hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%d_vs_nvtx"%(ieta+1)]  .Sumw2()
        hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%d_vs_nvtx"%(ieta+1)].Sumw2()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%d_vs_nvtx"%(ieta+1)].Sumw2()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%d_vs_nvtx"%(ieta+1)].Sumw2()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%d_vs_nvtx"%(ieta+1)].Sumw2()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%d_vs_nvtx"%(ieta+1)].Sumw2()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%d_vs_nvtx"%(ieta+1)].Sumw2()
        
        
    subdetDir = rechitDir.mkdir("subdetectors")
    hpdDir    = myFile.mkdir("hpdInformation")
    for be in ["B","E"]:
        for pm in ["P","M"]:
            subdet = "H%s%s"%(be,pm)
            subdetDir.cd()
            hpdInformation["rechitoccupancy"][subdetIdx] = {}
            hpdInformation["rechitoccupancy"][subdetIdx]["rechits_vs_nvtx"] = r.TH2D("rechits_vs_nvtx_%s"%(subdet),
                                                                                     "rechits_vs_nvtx_%s"%(subdet),
                                                                                     60,-0.5,59.5,500,-0.5,499.5)
            hpdInformation["rechitoccupancy"][subdetIdx]["rechitsto15_vs_nvtx"] = r.TH2D("rechitsto15_vs_nvtx_%s"%(subdet),
                                                                                         "rechitsto15_vs_nvtx_%s"%(subdet),
                                                                                         60,-0.5,59.5,500,-0.5,499.5)
            hpdInformation["rechitoccupancy"][subdetIdx]["rechits15_vs_nvtx"] = r.TH2D("rechits15_vs_nvtx_%s"%(subdet),
                                                                                       "rechits15_vs_nvtx_%s"%(subdet),
                                                                                       60,-0.5,59.5,500,-0.5,499.5)
            hpdInformation["rechitoccupancy"][subdetIdx]["rechits15to30_vs_nvtx"] = r.TH2D("rechits15to30_vs_nvtx_%s"%(subdet),
                                                                                           "rechits15to30_vs_nvtx_%s"%(subdet),
                                                                                           60,-0.5,59.5,500,-0.5,499.5)
            hpdInformation["rechitoccupancy"][subdetIdx]["rechits30_vs_nvtx"] = r.TH2D("rechits30_vs_nvtx_%s"%(subdet),
                                                                                       "rechits30_vs_nvtx_%s"%(subdet),
                                                                                       60,-0.5,59.5,300,-0.5,299.5)
            hpdInformation["rechitoccupancy"][subdetIdx]["rechits30to50_vs_nvtx"] = r.TH2D("rechits30to50_vs_nvtx_%s"%(subdet),
                                                                                           "rechits30to50_vs_nvtx_%s"%(subdet),
                                                                                           60,-0.5,59.5,300,-0.5,299.5)
            hpdInformation["rechitoccupancy"][subdetIdx]["rechits50_vs_nvtx"] = r.TH2D("rechits50_vs_nvtx_%s"%(subdet),
                                                                                       "rechits50_vs_nvtx_%s"%(subdet),
                                                                                       60,-0.5,59.5,200,-0.5,199.5)
            
            hpdInformation["rechitoccupancy"][subdetIdx]["rechits"]   = 0
            hpdInformation["rechitoccupancy"][subdetIdx]["rechitsto15"] = 0
            hpdInformation["rechitoccupancy"][subdetIdx]["rechits15"] = 0
            hpdInformation["rechitoccupancy"][subdetIdx]["rechits15to30"] = 0
            hpdInformation["rechitoccupancy"][subdetIdx]["rechits30"] = 0
            hpdInformation["rechitoccupancy"][subdetIdx]["rechits30to50"] = 0
            hpdInformation["rechitoccupancy"][subdetIdx]["rechits50"] = 0
            hpdInformation["rechitoccupancy"][subdetIdx]["rechits_vs_nvtx"]  .Sumw2()
            hpdInformation["rechitoccupancy"][subdetIdx]["rechitsto15_vs_nvtx"].Sumw2()
            hpdInformation["rechitoccupancy"][subdetIdx]["rechits15_vs_nvtx"].Sumw2()
            hpdInformation["rechitoccupancy"][subdetIdx]["rechits15to30_vs_nvtx"].Sumw2()
            hpdInformation["rechitoccupancy"][subdetIdx]["rechits30_vs_nvtx"].Sumw2()
            hpdInformation["rechitoccupancy"][subdetIdx]["rechits30to50_vs_nvtx"].Sumw2()
            hpdInformation["rechitoccupancy"][subdetIdx]["rechits50_vs_nvtx"].Sumw2()

            hpdDir.cd()
            hpdInformation["summary"][subdetIdx] = {}
            hpdInformation["summary"][subdetIdx]["name"] = subdet
            hpdInformation["summary"][subdetIdx]["hits_vs_nvtx"] = r.TH2D("hits_vs_nvtx_%s"%(subdet),
                                                                          "hits_vs_nvtx_%s"%(subdet),
                                                                          60,-0.5,59.5,20,-0.5,19.5)
            hpdInformation["summary"][subdetIdx]["hitsto15_vs_nvtx"] = r.TH2D("hitsto15_vs_nvtx_%s"%(subdet),
                                                                              "hitsto15_vs_nvtx_%s"%(subdet),
                                                                              60,-0.5,59.5,20,-0.5,19.5)
            hpdInformation["summary"][subdetIdx]["hits15_vs_nvtx"] = r.TH2D("hits15_vs_nvtx_%s"%(subdet),
                                                                            "hits15_vs_nvtx_%s"%(subdet),
                                                                            60,-0.5,59.5,20,-0.5,19.5)
            hpdInformation["summary"][subdetIdx]["hits15to30_vs_nvtx"] = r.TH2D("hits15to30_vs_nvtx_%s"%(subdet),
                                                                                "hits15to30_vs_nvtx_%s"%(subdet),
                                                                                60,-0.5,59.5,20,-0.5,19.5)
            hpdInformation["summary"][subdetIdx]["hits30_vs_nvtx"] = r.TH2D("hits30_vs_nvtx_%s"%(subdet),
                                                                            "hits30_vs_nvtx_%s"%(subdet),
                                                                            60,-0.5,59.5,20,-0.5,19.5)
            hpdInformation["summary"][subdetIdx]["hits30to50_vs_nvtx"] = r.TH2D("hits30to50_vs_nvtx_%s"%(subdet),
                                                                                "hits30to50_vs_nvtx_%s"%(subdet),
                                                                                60,-0.5,59.5,20,-0.5,19.5)
            hpdInformation["summary"][subdetIdx]["hits50_vs_nvtx"] = r.TH2D("hits50_vs_nvtx_%s"%(subdet),
                                                                            "hits50_vs_nvtx_%s"%(subdet),
                                                                            60,-0.5,59.5,20,-0.5,19.5)
            

            hpdInformation["summary"][subdetIdx]["hits_vs_nvtx"]  .Sumw2()
            hpdInformation["summary"][subdetIdx]["hitsto15_vs_nvtx"].Sumw2()
            hpdInformation["summary"][subdetIdx]["hits15_vs_nvtx"].Sumw2()
            hpdInformation["summary"][subdetIdx]["hits15to30_vs_nvtx"].Sumw2()
            hpdInformation["summary"][subdetIdx]["hits30_vs_nvtx"].Sumw2()
            hpdInformation["summary"][subdetIdx]["hits30to50_vs_nvtx"].Sumw2()
            hpdInformation["summary"][subdetIdx]["hits50_vs_nvtx"].Sumw2()
            subdetIdx = subdetIdx + 1
            
            for rbxIdx in range(18):
                keyName = "H%s%s%02d"%(be,pm,rbxIdx+1)
                #hpdInformation[keyName] = {}
                for hpd in range(4):
                    hpdInformation[hpdIdx] = {}
                    hpdInformation[hpdIdx] = {"name":keyName+"_HPD%d"%(hpd+1)}
                    #hpdInformation[keyName+"_HPD%d"%(hpd)]["index"] = hpdIdx
                    
                    hpdInformation[hpdIdx]["hits_vs_nvtx"] = r.TH2D("hits_vs_nvtx_%s_HPD%d"%(keyName,hpd+1),
                                                                                    "hits_vs_nvtx_%s_HPD%d"%(keyName,hpd+1),
                                                                                    60,-0.5,59.5,20,-0.5,19.5)
                    hpdInformation[hpdIdx]["hitsto15_vs_nvtx"] = r.TH2D("hitsto15_vs_nvtx_%s_HPD%d"%(keyName,hpd+1),
                                                                                    "hitsto15_vs_nvtx_%s_HPD%d"%(keyName,hpd+1),
                                                                                    60,-0.5,59.5,20,-0.5,19.5)
                    hpdInformation[hpdIdx]["hits15_vs_nvtx"] = r.TH2D("hits15_vs_nvtx_%s_HPD%d"%(keyName,hpd+1),
                                                                                    "hits15_vs_nvtx_%s_HPD%d"%(keyName,hpd+1),
                                                                                    60,-0.5,59.5,20,-0.5,19.5)
                    hpdInformation[hpdIdx]["hits15to30_vs_nvtx"] = r.TH2D("hits15to30_vs_nvtx_%s_HPD%d"%(keyName,hpd+1),
                                                                                    "hits15to30_vs_nvtx_%s_HPD%d"%(keyName,hpd+1),
                                                                                    60,-0.5,59.5,20,-0.5,19.5)
                    hpdInformation[hpdIdx]["hits30_vs_nvtx"] = r.TH2D("hits30_vs_nvtx_%s_HPD%d"%(keyName,hpd+1),
                                                                                    "hits30_vs_nvtx_%s_HPD%d"%(keyName,hpd+1),
                                                                                    60,-0.5,59.5,20,-0.5,19.5)
                    hpdInformation[hpdIdx]["hits30to50_vs_nvtx"] = r.TH2D("hits30to50_vs_nvtx_%s_HPD%d"%(keyName,hpd+1),
                                                                                    "hits30to50_vs_nvtx_%s_HPD%d"%(keyName,hpd+1),
                                                                                    60,-0.5,59.5,20,-0.5,19.5)
                    hpdInformation[hpdIdx]["hits50_vs_nvtx"] = r.TH2D("hits50_vs_nvtx_%s_HPD%d"%(keyName,hpd+1),
                                                                                    "hits50_vs_nvtx_%s_HPD%d"%(keyName,hpd+1),
                                                                                    60,-0.5,59.5,20,-0.5,19.5)
                    hpdInformation[hpdIdx]["hits"]   = 0
                    hpdInformation[hpdIdx]["hitsto15"] = 0
                    hpdInformation[hpdIdx]["hits15"] = 0
                    hpdInformation[hpdIdx]["hits15to30"] = 0
                    hpdInformation[hpdIdx]["hits30"] = 0
                    hpdInformation[hpdIdx]["hits30to50"] = 0
                    hpdInformation[hpdIdx]["hits50"] = 0
                    hpdInformation[hpdIdx]["hits_vs_nvtx"]  .Sumw2()
                    hpdInformation[hpdIdx]["hitsto15_vs_nvtx"].Sumw2()
                    hpdInformation[hpdIdx]["hits15_vs_nvtx"].Sumw2()
                    hpdInformation[hpdIdx]["hits15to30_vs_nvtx"].Sumw2()
                    hpdInformation[hpdIdx]["hits30_vs_nvtx"].Sumw2()
                    hpdInformation[hpdIdx]["hits30to50_vs_nvtx"].Sumw2()
                    hpdInformation[hpdIdx]["hits50_vs_nvtx"].Sumw2()
                    #hpdInformation[keyName+"_HPD%d"%(hpd)][""] = 
                    #hpdInformation[keyName+"_HPD%d"%(hpd)][""] = 
                    hpdIdx = hpdIdx+1

    
    #print hpdInformation
    return hpdInformation

def reset_hpd_counters(hpdInformation):
    r.gROOT.SetBatch(True)
    hpdInformation["rechitoccupancy"]["overall"]["rechits"]   = 0
    hpdInformation["rechitoccupancy"]["overall"]["rechitsto15"] = 0
    hpdInformation["rechitoccupancy"]["overall"]["rechits15"] = 0
    hpdInformation["rechitoccupancy"]["overall"]["rechits15to30"] = 0
    hpdInformation["rechitoccupancy"]["overall"]["rechits30"] = 0
    hpdInformation["rechitoccupancy"]["overall"]["rechits30to50"] = 0
    hpdInformation["rechitoccupancy"]["overall"]["rechits50"] = 0

    #for be in ["Barrel","Endcap"]:
    #    hpdInformation["rechitoccupancy"][be]["rechits"]   = 0
    #    hpdInformation["rechitoccupancy"][be]["rechits15"] = 0
    #    hpdInformation["rechitoccupancy"][be]["rechits30"] = 0
    #    hpdInformation["rechitoccupancy"][be]["rechits50"] = 0

    for subdetIdx in range(4):
        hpdInformation["rechitoccupancy"][subdetIdx]["rechits"]   = 0
        hpdInformation["rechitoccupancy"][subdetIdx]["rechitsto15"] = 0
        hpdInformation["rechitoccupancy"][subdetIdx]["rechits15"] = 0
        hpdInformation["rechitoccupancy"][subdetIdx]["rechits15to30"] = 0
        hpdInformation["rechitoccupancy"][subdetIdx]["rechits30"] = 0
        hpdInformation["rechitoccupancy"][subdetIdx]["rechits30to50"] = 0
        hpdInformation["rechitoccupancy"][subdetIdx]["rechits50"] = 0
    
    for ieta in range(29):
        theEta = ieta + 1
        for depth in range(3):
            if theEta < 15 and depth > 0:
                # barrel has max depth==1
                continue
            elif theEta < 16 and depth > 1:
                # iEta 15 has max depth==2
                continue
            elif theEta == 17 and depth > 0:
                # iEta 17 has depth 1 only
                continue
            elif theEta > 17 and theEta < 27 and depth > 1:
                # iEta 18-26 have max depth==2
                continue
            elif theEta > 28 and depth > 1:
                # iEta 29 have max depth==2
                continue
            # iEta 16,27,28 have max depth==3

            hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%dp_d%d"%(ieta+1,depth+1)]   = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dp_d%d"%(ieta+1,depth+1)] = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%dp_d%d"%(ieta+1,depth+1)] = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dp_d%d"%(ieta+1,depth+1)] = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%dp_d%d"%(ieta+1,depth+1)] = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dp_d%d"%(ieta+1,depth+1)] = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%dp_d%d"%(ieta+1,depth+1)] = 0
            
            hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%dm_d%d"%(ieta+1,depth+1)]   = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dm_d%d"%(ieta+1,depth+1)] = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%dm_d%d"%(ieta+1,depth+1)] = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dm_d%d"%(ieta+1,depth+1)] = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%dm_d%d"%(ieta+1,depth+1)] = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dm_d%d"%(ieta+1,depth+1)] = 0
            hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%dm_d%d"%(ieta+1,depth+1)] = 0

        ##hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%d"%(ieta+1)]   = 0
        ##hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%d"%(ieta+1)] = 0
        ##hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%d"%(ieta+1)] = 0
        ##hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%d"%(ieta+1)] = 0

    for hpdIndex in range(288):
        hpdInformation[hpdIndex]["hits"]   = 0
        hpdInformation[hpdIndex]["hitsto15"] = 0
        hpdInformation[hpdIndex]["hits15"] = 0
        hpdInformation[hpdIndex]["hits15to30"] = 0
        hpdInformation[hpdIndex]["hits30"] = 0
        hpdInformation[hpdIndex]["hits30to50"] = 0
        hpdInformation[hpdIndex]["hits50"] = 0

    return hpdInformation


def fill_hpd_histograms(hpdInformation,nVtx):
    r.gROOT.SetBatch(True)
    hits       = hpdInformation["rechitoccupancy"]["overall"]["rechits"] 
    hitsto15   = hpdInformation["rechitoccupancy"]["overall"]["rechitsto15"]
    hits15     = hpdInformation["rechitoccupancy"]["overall"]["rechits15"]
    hits15to30 = hpdInformation["rechitoccupancy"]["overall"]["rechits15to30"]
    hits30     = hpdInformation["rechitoccupancy"]["overall"]["rechits30"]
    hits30to50 = hpdInformation["rechitoccupancy"]["overall"]["rechits30to50"]
    hits50     = hpdInformation["rechitoccupancy"]["overall"]["rechits50"]

    hpdInformation["rechitoccupancy"]["overall"]["rechits_vs_nvtx"]  .Fill(nVtx,hits)
    hpdInformation["rechitoccupancy"]["overall"]["rechitsto15_vs_nvtx"].Fill(nVtx,hitsto15)
    hpdInformation["rechitoccupancy"]["overall"]["rechits15_vs_nvtx"].Fill(nVtx,hits15)
    hpdInformation["rechitoccupancy"]["overall"]["rechits15to30_vs_nvtx"].Fill(nVtx,hits15to30)
    hpdInformation["rechitoccupancy"]["overall"]["rechits30_vs_nvtx"].Fill(nVtx,hits30)
    hpdInformation["rechitoccupancy"]["overall"]["rechits30to50_vs_nvtx"].Fill(nVtx,hits30to50)
    hpdInformation["rechitoccupancy"]["overall"]["rechits50_vs_nvtx"].Fill(nVtx,hits50)

    #for be in ["Barrel","Endcap"]:
    hits   = hpdInformation["rechitoccupancy"][0]["rechits"]   + hpdInformation["rechitoccupancy"][1]["rechits"]  
    hitsto15 = hpdInformation["rechitoccupancy"][0]["rechitsto15"] + hpdInformation["rechitoccupancy"][1]["rechitsto15"]
    hits15 = hpdInformation["rechitoccupancy"][0]["rechits15"] + hpdInformation["rechitoccupancy"][1]["rechits15"]
    hits15to30 = hpdInformation["rechitoccupancy"][0]["rechits15to30"] + hpdInformation["rechitoccupancy"][1]["rechits15to30"]
    hits30 = hpdInformation["rechitoccupancy"][0]["rechits30"] + hpdInformation["rechitoccupancy"][1]["rechits30"]
    hits30to50 = hpdInformation["rechitoccupancy"][0]["rechits30to50"] + hpdInformation["rechitoccupancy"][1]["rechits30to50"]
    hits50 = hpdInformation["rechitoccupancy"][0]["rechits50"] + hpdInformation["rechitoccupancy"][1]["rechits50"]
    # hits   = hpdInformation["rechitoccupancy"][be]["rechits"] 
    # hits15 = hpdInformation["rechitoccupancy"][be]["rechits15"]
    # hits30 = hpdInformation["rechitoccupancy"][be]["rechits30"]
    # hits50 = hpdInformation["rechitoccupancy"][be]["rechits50"]
    
    hpdInformation["rechitoccupancy"]["Barrel"]["rechits_vs_nvtx"]  .Fill(nVtx,hits)
    hpdInformation["rechitoccupancy"]["Barrel"]["rechitsto15_vs_nvtx"].Fill(nVtx,hitsto15)
    hpdInformation["rechitoccupancy"]["Barrel"]["rechits15_vs_nvtx"].Fill(nVtx,hits15)
    hpdInformation["rechitoccupancy"]["Barrel"]["rechits15to30_vs_nvtx"].Fill(nVtx,hits15to30)
    hpdInformation["rechitoccupancy"]["Barrel"]["rechits30_vs_nvtx"].Fill(nVtx,hits30)
    hpdInformation["rechitoccupancy"]["Barrel"]["rechits30to50_vs_nvtx"].Fill(nVtx,hits30to50)
    hpdInformation["rechitoccupancy"]["Barrel"]["rechits50_vs_nvtx"].Fill(nVtx,hits50)

    hits       = hpdInformation["rechitoccupancy"][2]["rechits"]   + hpdInformation["rechitoccupancy"][3]["rechits"]  
    hitsto15   = hpdInformation["rechitoccupancy"][2]["rechitsto15"] + hpdInformation["rechitoccupancy"][3]["rechitsto15"]
    hits15     = hpdInformation["rechitoccupancy"][2]["rechits15"] + hpdInformation["rechitoccupancy"][3]["rechits15"]
    hits15to30 = hpdInformation["rechitoccupancy"][2]["rechits15to30"] + hpdInformation["rechitoccupancy"][3]["rechits15to30"]
    hits30     = hpdInformation["rechitoccupancy"][2]["rechits30"] + hpdInformation["rechitoccupancy"][3]["rechits30"]
    hits30to50 = hpdInformation["rechitoccupancy"][2]["rechits30to50"] + hpdInformation["rechitoccupancy"][3]["rechits30to50"]
    hits50     = hpdInformation["rechitoccupancy"][2]["rechits50"] + hpdInformation["rechitoccupancy"][3]["rechits50"]
    # hits   = hpdInformation["rechitoccupancy"][be]["rechits"] 
    # hits15 = hpdInformation["rechitoccupancy"][be]["rechits15"]
    # hits30 = hpdInformation["rechitoccupancy"][be]["rechits30"]
    # hits50 = hpdInformation["rechitoccupancy"][be]["rechits50"]

    hpdInformation["rechitoccupancy"]["Endcap"]["rechits_vs_nvtx"]  .Fill(nVtx,hits)
    hpdInformation["rechitoccupancy"]["Endcap"]["rechitsto15_vs_nvtx"].Fill(nVtx,hitsto15)
    hpdInformation["rechitoccupancy"]["Endcap"]["rechits15_vs_nvtx"].Fill(nVtx,hits15)
    hpdInformation["rechitoccupancy"]["Endcap"]["rechits15to30_vs_nvtx"].Fill(nVtx,hits15to30)
    hpdInformation["rechitoccupancy"]["Endcap"]["rechits30_vs_nvtx"].Fill(nVtx,hits30)
    hpdInformation["rechitoccupancy"]["Endcap"]["rechits30to50_vs_nvtx"].Fill(nVtx,hits30to50)
    hpdInformation["rechitoccupancy"]["Endcap"]["rechits50_vs_nvtx"].Fill(nVtx,hits50)

    for ieta in range(29):
        allPlusHits       = 0
        allPlusHitsto15   = 0
        allPlusHits15     = 0
        allPlusHits15to30 = 0
        allPlusHits30     = 0
        allPlusHits30to50 = 0
        allPlusHits50     = 0

        allMinusHits       = 0
        allMinusHitsto15   = 0
        allMinusHits15     = 0
        allMinusHits15to30 = 0
        allMinusHits30     = 0
        allMinusHits30to50 = 0
        allMinusHits50     = 0
        
        theEta = ieta + 1
        for depth in range(3):
            if theEta < 15 and depth > 0:
                # barrel has max depth==1
                continue
            elif theEta < 16 and depth > 1:
                # iEta 15 has max depth==2
                continue
            elif theEta == 17 and depth > 0:
                # iEta 17 has depth 1 only
                continue
            elif theEta > 17 and theEta < 27 and depth > 1:
                # iEta 18-26 have max depth==2
                continue
            elif theEta > 28 and depth > 1:
                # iEta 29 have max depth==2
                continue
            # iEta 16,27,28 have max depth==3

            hits   = hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%dp_d%d"%(ieta+1,depth+1)] 
            hitsto15 = hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dp_d%d"%(ieta+1,depth+1)]
            hits15 = hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%dp_d%d"%(ieta+1,depth+1)]
            hits15to30 = hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dp_d%d"%(ieta+1,depth+1)]
            hits30 = hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%dp_d%d"%(ieta+1,depth+1)]
            hits30to50 = hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dp_d%d"%(ieta+1,depth+1)]
            hits50 = hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%dp_d%d"%(ieta+1,depth+1)]

            allPlusHits       = allPlusHits   + hits
            allPlusHitsto15   = allPlusHitsto15 + hitsto15
            allPlusHits15     = allPlusHits15 + hits15
            allPlusHits15to30 = allPlusHits15to30 + hits15to30
            allPlusHits30     = allPlusHits30 + hits30
            allPlusHits30to50 = allPlusHits30to50 + hits30to50
            allPlusHits50     = allPlusHits50 + hits50

            hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)]  .Fill(nVtx,hits)
            hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)].Fill(nVtx,hitsto15)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)].Fill(nVtx,hits15)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)].Fill(nVtx,hits15to30)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)].Fill(nVtx,hits30)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)].Fill(nVtx,hits30to50)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)].Fill(nVtx,hits50)
            
            hits       = hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%dm_d%d"%(ieta+1,depth+1)] 
            hitsto15   = hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dm_d%d"%(ieta+1,depth+1)]
            hits15     = hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%dm_d%d"%(ieta+1,depth+1)]
            hits15to30 = hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dm_d%d"%(ieta+1,depth+1)]
            hits30     = hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%dm_d%d"%(ieta+1,depth+1)]
            hits30to50 = hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dm_d%d"%(ieta+1,depth+1)]
            hits50     = hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%dm_d%d"%(ieta+1,depth+1)]

            allMinusHits       = allMinusHits   + hits
            allMinusHitsto15   = allMinusHitsto15 + hitsto15
            allMinusHits15     = allMinusHits15 + hits15
            allMinusHits15to30 = allMinusHits15to30 + hits15to30
            allMinusHits30     = allMinusHits30 + hits30
            allMinusHits30to50 = allMinusHits30to50 + hits30to50
            allMinusHits50     = allMinusHits50 + hits50

            hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)]  .Fill(nVtx,hits)
            hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)].Fill(nVtx,hitsto15)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)].Fill(nVtx,hits15)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)].Fill(nVtx,hits15to30)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)].Fill(nVtx,hits30)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)].Fill(nVtx,hits30to50)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)].Fill(nVtx,hits50)
            
            hits       = hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%dp_d%d"%(ieta+1,depth+1)]   + hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%dm_d%d"%(ieta+1,depth+1)] 
            hitsto15   = hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dp_d%d"%(ieta+1,depth+1)] + hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dm_d%d"%(ieta+1,depth+1)]
            hits15     = hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%dp_d%d"%(ieta+1,depth+1)] + hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%dm_d%d"%(ieta+1,depth+1)]
            hits15to30 = hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dp_d%d"%(ieta+1,depth+1)] + hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dm_d%d"%(ieta+1,depth+1)]
            hits30     = hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%dp_d%d"%(ieta+1,depth+1)] + hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%dm_d%d"%(ieta+1,depth+1)]
            hits30to50 = hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dp_d%d"%(ieta+1,depth+1)] + hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dm_d%d"%(ieta+1,depth+1)]
            hits50     = hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%dp_d%d"%(ieta+1,depth+1)] + hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%dm_d%d"%(ieta+1,depth+1)]
            hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)]  .Fill(nVtx,hits)
            hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)].Fill(nVtx,hitsto15)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)].Fill(nVtx,hits15)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)].Fill(nVtx,hits15to30)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)].Fill(nVtx,hits30)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)].Fill(nVtx,hits30to50)
            hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)].Fill(nVtx,hits50)

        # three depth sum
        hits       = allPlusHits
        hitsto15   = allPlusHitsto15
        hits15     = allPlusHits15
        hits15to30 = allPlusHits15to30
        hits30     = allPlusHits30
        hits30to50 = allPlusHits30to50
        hits50     = allPlusHits50
        hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%dp_vs_nvtx"%(ieta+1)]  .Fill(nVtx,hits)
        hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dp_vs_nvtx"%(ieta+1)].Fill(nVtx,hitsto15)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%dp_vs_nvtx"%(ieta+1)].Fill(nVtx,hits15)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dp_vs_nvtx"%(ieta+1)].Fill(nVtx,hits15to30)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%dp_vs_nvtx"%(ieta+1)].Fill(nVtx,hits30)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dp_vs_nvtx"%(ieta+1)].Fill(nVtx,hits30to50)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%dp_vs_nvtx"%(ieta+1)].Fill(nVtx,hits50)
        
        hits       = allMinusHits
        hitsto15   = allMinusHitsto15
        hits15     = allMinusHits15
        hits15to30 = allMinusHits15to30
        hits30     = allMinusHits30
        hits30to50 = allMinusHits30to50
        hits50     = allMinusHits50
        hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%dm_vs_nvtx"%(ieta+1)]  .Fill(nVtx,hits)
        hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dm_vs_nvtx"%(ieta+1)].Fill(nVtx,hitsto15)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%dm_vs_nvtx"%(ieta+1)].Fill(nVtx,hits15)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dm_vs_nvtx"%(ieta+1)].Fill(nVtx,hits15to30)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%dm_vs_nvtx"%(ieta+1)].Fill(nVtx,hits30)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dm_vs_nvtx"%(ieta+1)].Fill(nVtx,hits30to50)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%dm_vs_nvtx"%(ieta+1)].Fill(nVtx,hits50)
        
        hits       = allPlusHits   + allMinusHits
        hitsto15   = allPlusHitsto15 + allMinusHitsto15
        hits15     = allPlusHits15 + allMinusHits15
        hits15to30 = allPlusHits15to30 + allMinusHits15to30
        hits30     = allPlusHits30 + allMinusHits30
        hits30to50 = allPlusHits30to50 + allMinusHits30to50
        hits50     = allPlusHits50 + allMinusHits50
        hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%d_vs_nvtx"%(ieta+1)]  .Fill(nVtx,hits)
        hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%d_vs_nvtx"%(ieta+1)].Fill(nVtx,hitsto15)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%d_vs_nvtx"%(ieta+1)].Fill(nVtx,hits15)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%d_vs_nvtx"%(ieta+1)].Fill(nVtx,hits15to30)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%d_vs_nvtx"%(ieta+1)].Fill(nVtx,hits30)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%d_vs_nvtx"%(ieta+1)].Fill(nVtx,hits30to50)
        hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%d_vs_nvtx"%(ieta+1)].Fill(nVtx,hits50)

    for subdetIdx in range(4):
        hits       = hpdInformation["rechitoccupancy"][subdetIdx]["rechits"] 
        hitsto15   = hpdInformation["rechitoccupancy"][subdetIdx]["rechitsto15"]
        hits15     = hpdInformation["rechitoccupancy"][subdetIdx]["rechits15"]
        hits15to30 = hpdInformation["rechitoccupancy"][subdetIdx]["rechits15to30"]
        hits30     = hpdInformation["rechitoccupancy"][subdetIdx]["rechits30"]
        hits30to50 = hpdInformation["rechitoccupancy"][subdetIdx]["rechits30to50"]
        hits50     = hpdInformation["rechitoccupancy"][subdetIdx]["rechits50"]
        hpdInformation["rechitoccupancy"][subdetIdx]["rechits_vs_nvtx"]  .Fill(nVtx,hits)
        hpdInformation["rechitoccupancy"][subdetIdx]["rechitsto15_vs_nvtx"].Fill(nVtx,hitsto15)
        hpdInformation["rechitoccupancy"][subdetIdx]["rechits15_vs_nvtx"].Fill(nVtx,hits15)
        hpdInformation["rechitoccupancy"][subdetIdx]["rechits15to30_vs_nvtx"].Fill(nVtx,hits15to30)
        hpdInformation["rechitoccupancy"][subdetIdx]["rechits30_vs_nvtx"].Fill(nVtx,hits30)
        hpdInformation["rechitoccupancy"][subdetIdx]["rechits30to50_vs_nvtx"].Fill(nVtx,hits30to50)
        hpdInformation["rechitoccupancy"][subdetIdx]["rechits50_vs_nvtx"].Fill(nVtx,hits50)

    #for keyName in hpdNames:
    ##for be in ["B","E"]:
    ##    for pm in ["P","M"]:
    ##        for rbxIdx in range(18):
    ##            keyName = "H%s%s%02d"%(be,pm,rbxIdx)
    ##            for hpd in range(4):
    ##hpdInformation[keyName+"_HPD%d"%(hpd)]["hits"] = 0
    ##hpdInformation[keyName+"_HPD%d"%(hpd)]["hits15"] = 0
    ##hpdInformation[keyName+"_HPD%d"%(hpd)]["hits30"] = 0
    ##hpdInformation[keyName+"_HPD%d"%(hpd)]["hits50"] = 0
    for hpdIndex in range(288):
        hits       = hpdInformation[hpdIndex]["hits"]  
        hitsto15   = hpdInformation[hpdIndex]["hitsto15"]
        hits15     = hpdInformation[hpdIndex]["hits15"]
        hits15to30 = hpdInformation[hpdIndex]["hits15to30"]
        hits30     = hpdInformation[hpdIndex]["hits30"]
        hits30to50 = hpdInformation[hpdIndex]["hits30to50"]
        hits50     = hpdInformation[hpdIndex]["hits50"]

        hpdInformation[hpdIndex]["hits_vs_nvtx"]  .Fill(nVtx,hits  )
        hpdInformation[hpdIndex]["hitsto15_vs_nvtx"].Fill(nVtx,hitsto15)
        hpdInformation[hpdIndex]["hits15_vs_nvtx"].Fill(nVtx,hits15)
        hpdInformation[hpdIndex]["hits15to30_vs_nvtx"].Fill(nVtx,hits15to30)
        hpdInformation[hpdIndex]["hits30_vs_nvtx"].Fill(nVtx,hits30)
        hpdInformation[hpdIndex]["hits30to50_vs_nvtx"].Fill(nVtx,hits30to50)
        hpdInformation[hpdIndex]["hits50_vs_nvtx"].Fill(nVtx,hits50)

        #print hpdIndex, nVtx, hits, hits15, hits30, hits50
 
        if hpdIndex < 72:
            hpdInformation["summary"][0]["hits_vs_nvtx"]  .Fill(nVtx,hits  )
            hpdInformation["summary"][0]["hitsto15_vs_nvtx"].Fill(nVtx,hitsto15)
            hpdInformation["summary"][0]["hits15_vs_nvtx"].Fill(nVtx,hits15)
            hpdInformation["summary"][0]["hits15to30_vs_nvtx"].Fill(nVtx,hits15to30)
            hpdInformation["summary"][0]["hits30_vs_nvtx"].Fill(nVtx,hits30)
            hpdInformation["summary"][0]["hits30to50_vs_nvtx"].Fill(nVtx,hits30to50)
            hpdInformation["summary"][0]["hits50_vs_nvtx"].Fill(nVtx,hits50)
        elif hpdIndex < 144:
            hpdInformation["summary"][1]["hits_vs_nvtx"]  .Fill(nVtx,hits  )
            hpdInformation["summary"][1]["hitsto15_vs_nvtx"].Fill(nVtx,hitsto15)
            hpdInformation["summary"][1]["hits15_vs_nvtx"].Fill(nVtx,hits15)
            hpdInformation["summary"][1]["hits15to30_vs_nvtx"].Fill(nVtx,hits15to30)
            hpdInformation["summary"][1]["hits30_vs_nvtx"].Fill(nVtx,hits30)
            hpdInformation["summary"][1]["hits30to50_vs_nvtx"].Fill(nVtx,hits30to50)
            hpdInformation["summary"][1]["hits50_vs_nvtx"].Fill(nVtx,hits50)
        elif hpdIndex < 216:
            hpdInformation["summary"][2]["hits_vs_nvtx"]  .Fill(nVtx,hits  )
            hpdInformation["summary"][2]["hitsto15_vs_nvtx"].Fill(nVtx,hitsto15)
            hpdInformation["summary"][2]["hits15_vs_nvtx"].Fill(nVtx,hits15)
            hpdInformation["summary"][2]["hits15to30_vs_nvtx"].Fill(nVtx,hits15to30)
            hpdInformation["summary"][2]["hits30_vs_nvtx"].Fill(nVtx,hits30)
            hpdInformation["summary"][2]["hits30to50_vs_nvtx"].Fill(nVtx,hits30to50)
            hpdInformation["summary"][2]["hits50_vs_nvtx"].Fill(nVtx,hits50)
        else:
            hpdInformation["summary"][3]["hits_vs_nvtx"]  .Fill(nVtx,hits  )
            hpdInformation["summary"][3]["hitsto15_vs_nvtx"].Fill(nVtx,hitsto15)
            hpdInformation["summary"][3]["hits15_vs_nvtx"].Fill(nVtx,hits15)
            hpdInformation["summary"][3]["hits15to30_vs_nvtx"].Fill(nVtx,hits15to30)
            hpdInformation["summary"][3]["hits30_vs_nvtx"].Fill(nVtx,hits30)
            hpdInformation["summary"][3]["hits30to50_vs_nvtx"].Fill(nVtx,hits30to50)
            hpdInformation["summary"][3]["hits50_vs_nvtx"].Fill(nVtx,hits50)


    return hpdInformation

def write_hpd_histograms(hpdInformation,myFile):
    r.gROOT.SetBatch(True)
    energyDir = myFile.Get("rechitenergy")
    rechitDir = myFile.Get("rechitoccupancy")
    rechitDir.cd()
    hpdInformation["rechitoccupancy"]["overall"]["rechits_vs_nvtx"]  .Write()
    hpdInformation["rechitoccupancy"]["overall"]["rechitsto15_vs_nvtx"].Write()
    hpdInformation["rechitoccupancy"]["overall"]["rechits15_vs_nvtx"].Write()
    hpdInformation["rechitoccupancy"]["overall"]["rechits15to30_vs_nvtx"].Write()
    hpdInformation["rechitoccupancy"]["overall"]["rechits30_vs_nvtx"].Write()
    hpdInformation["rechitoccupancy"]["overall"]["rechits30to50_vs_nvtx"].Write()
    hpdInformation["rechitoccupancy"]["overall"]["rechits50_vs_nvtx"].Write()

    for be in ["Barrel","Endcap"]:
        outputDir = rechitDir.Get(be)
        outputDir.cd()
        hpdInformation["rechitoccupancy"][be]["rechits_vs_nvtx"]  .Write()
        hpdInformation["rechitoccupancy"][be]["rechitsto15_vs_nvtx"].Write()
        hpdInformation["rechitoccupancy"][be]["rechits15_vs_nvtx"].Write()
        hpdInformation["rechitoccupancy"][be]["rechits15to30_vs_nvtx"].Write()
        hpdInformation["rechitoccupancy"][be]["rechits30_vs_nvtx"].Write()
        hpdInformation["rechitoccupancy"][be]["rechits30to50_vs_nvtx"].Write()
        hpdInformation["rechitoccupancy"][be]["rechits50_vs_nvtx"].Write()

    etaDir = rechitDir.Get("etahists")
    etaDir.cd()
    for ieta in range(29):
        theEta = ieta + 1
        for depth in range(3):
            if theEta < 15 and depth > 0:
                # barrel has max depth==1
                continue
            elif theEta < 16 and depth > 1:
                # iEta 15 has max depth==2
                continue
            elif theEta == 17 and depth > 0:
                # iEta 17 has depth 1 only
                continue
            elif theEta > 17 and theEta < 27 and depth > 1:
                # iEta 18-26 have max depth==2
                continue
            elif theEta > 28 and depth > 1:
                # iEta 29 have max depth==2
                continue
            # iEta 16,27,28 have max depth==3

            etaDir.cd()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)]  .Write()
            hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)].Write()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)].Write()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)].Write()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)].Write()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)].Write()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%dp_d%d_vs_nvtx"%(ieta+1,depth+1)].Write()
            
            hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)]  .Write()
            hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)].Write()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)].Write()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)].Write()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)].Write()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)].Write()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%dm_d%d_vs_nvtx"%(ieta+1,depth+1)].Write()
            
            hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)]  .Write()
            hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)].Write()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)].Write()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)].Write()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)].Write()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)].Write()
            hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%d_d%d_vs_nvtx"%(ieta+1,depth+1)].Write()

            energyDir.cd()
            hpdInformation["rechitenergy"]["rechits_energy_ieta%dp_d%d"%(ieta+1,depth+1)]  .Write()
            hpdInformation["rechitenergy"]["rechitsto15_energy_ieta%dp_d%d"%(ieta+1,depth+1)].Write()
            hpdInformation["rechitenergy"]["rechits15_energy_ieta%dp_d%d"%(ieta+1,depth+1)].Write()
            hpdInformation["rechitenergy"]["rechits15to30_energy_ieta%dp_d%d"%(ieta+1,depth+1)].Write()
            hpdInformation["rechitenergy"]["rechits30_energy_ieta%dp_d%d"%(ieta+1,depth+1)].Write()
            hpdInformation["rechitenergy"]["rechits30to50_energy_ieta%dp_d%d"%(ieta+1,depth+1)].Write()
            hpdInformation["rechitenergy"]["rechits50_energy_ieta%dp_d%d"%(ieta+1,depth+1)].Write()
            
            hpdInformation["rechitenergy"]["rechits_energy_ieta%dm_d%d"%(ieta+1,depth+1)]  .Write()
            hpdInformation["rechitenergy"]["rechitsto15_energy_ieta%dm_d%d"%(ieta+1,depth+1)].Write()
            hpdInformation["rechitenergy"]["rechits15_energy_ieta%dm_d%d"%(ieta+1,depth+1)].Write()
            hpdInformation["rechitenergy"]["rechits15to30_energy_ieta%dm_d%d"%(ieta+1,depth+1)].Write()
            hpdInformation["rechitenergy"]["rechits30_energy_ieta%dm_d%d"%(ieta+1,depth+1)].Write()
            hpdInformation["rechitenergy"]["rechits30to50_energy_ieta%dm_d%d"%(ieta+1,depth+1)].Write()
            hpdInformation["rechitenergy"]["rechits50_energy_ieta%dm_d%d"%(ieta+1,depth+1)].Write()
            

        # cumulative depths
        etaDir.cd()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%dp_vs_nvtx"%(ieta+1)]  .Write()
        hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dp_vs_nvtx"%(ieta+1)].Write()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%dp_vs_nvtx"%(ieta+1)].Write()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dp_vs_nvtx"%(ieta+1)].Write()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%dp_vs_nvtx"%(ieta+1)].Write()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dp_vs_nvtx"%(ieta+1)].Write()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%dp_vs_nvtx"%(ieta+1)].Write()

        hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%dm_vs_nvtx"%(ieta+1)]  .Write()
        hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%dm_vs_nvtx"%(ieta+1)].Write()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%dm_vs_nvtx"%(ieta+1)].Write()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%dm_vs_nvtx"%(ieta+1)].Write()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%dm_vs_nvtx"%(ieta+1)].Write()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%dm_vs_nvtx"%(ieta+1)].Write()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%dm_vs_nvtx"%(ieta+1)].Write()

        hpdInformation["rechitoccupancy"]["etahists"]["rechits_ieta%d_vs_nvtx"%(ieta+1)]  .Write()
        hpdInformation["rechitoccupancy"]["etahists"]["rechitsto15_ieta%d_vs_nvtx"%(ieta+1)].Write()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits15_ieta%d_vs_nvtx"%(ieta+1)].Write()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits15to30_ieta%d_vs_nvtx"%(ieta+1)].Write()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits30_ieta%d_vs_nvtx"%(ieta+1)].Write()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits30to50_ieta%d_vs_nvtx"%(ieta+1)].Write()
        hpdInformation["rechitoccupancy"]["etahists"]["rechits50_ieta%d_vs_nvtx"%(ieta+1)].Write()

    subdetDir = rechitDir.Get("subdetectors")
    subdetDir.cd()
    for subdetIdx in range(4):
        hpdInformation["rechitoccupancy"][subdetIdx]["rechits_vs_nvtx"]  .Write()
        hpdInformation["rechitoccupancy"][subdetIdx]["rechitsto15_vs_nvtx"].Write()
        hpdInformation["rechitoccupancy"][subdetIdx]["rechits15_vs_nvtx"].Write()
        hpdInformation["rechitoccupancy"][subdetIdx]["rechits15to30_vs_nvtx"].Write()
        hpdInformation["rechitoccupancy"][subdetIdx]["rechits30_vs_nvtx"].Write()
        hpdInformation["rechitoccupancy"][subdetIdx]["rechits30to50_vs_nvtx"].Write()
        hpdInformation["rechitoccupancy"][subdetIdx]["rechits50_vs_nvtx"].Write()
    #for keyName in hpdNames:
    ##for be in ["B","E"]:
    ##    for pm in ["P","M"]:
    ##        for rbxIdx in range(18):
    ##            keyName = "H%s%s%02d"%(be,pm,rbxIdx)
    ##            for hpd in range(4):
    ##hpdInformation[keyName+"_HPD%d"%(hpd)]["hits"] = 0
    ##hpdInformation[keyName+"_HPD%d"%(hpd)]["hits15"] = 0
    ##hpdInformation[keyName+"_HPD%d"%(hpd)]["hits30"] = 0
    ##hpdInformation[keyName+"_HPD%d"%(hpd)]["hits50"] = 0
    myFile.cd()
    hpdDir = myFile.Get("hpdInformation")
    myFile.cd("hpdInformation")
    for hpdIndex in range(288):
        hpdInformation[hpdIndex]["hits_vs_nvtx"]  .Write()
        hpdInformation[hpdIndex]["hitsto15_vs_nvtx"].Write()
        hpdInformation[hpdIndex]["hits15_vs_nvtx"].Write()
        hpdInformation[hpdIndex]["hits15to30_vs_nvtx"].Write()
        hpdInformation[hpdIndex]["hits30_vs_nvtx"].Write()
        hpdInformation[hpdIndex]["hits30to50_vs_nvtx"].Write()
        hpdInformation[hpdIndex]["hits50_vs_nvtx"].Write()

    #myFile.cd("hpdInformation")
    for subdetIndex in range(4):
        #hpdDir.cd()
        hpdInformation["summary"][subdetIndex]["hits_vs_nvtx"]  .Write()
        hpdInformation["summary"][subdetIndex]["hitsto15_vs_nvtx"].Write()
        hpdInformation["summary"][subdetIndex]["hits15_vs_nvtx"].Write()
        hpdInformation["summary"][subdetIndex]["hits15to30_vs_nvtx"].Write()
        hpdInformation["summary"][subdetIndex]["hits30_vs_nvtx"].Write()
        hpdInformation["summary"][subdetIndex]["hits30to50_vs_nvtx"].Write()
        hpdInformation["summary"][subdetIndex]["hits50_vs_nvtx"].Write()

    myFile.Write()

    return        

######
def map_channel_to_hpd(eta,phi,depth):
    r.gROOT.SetBatch(True)
    return map_channel_to_hpd1(eta,phi,depth)

def map_channel_to_hpd1(eta,phi,depth):
    r.gROOT.SetBatch(True)
    ##minus side mapping still off, not quite sure how to fix yet
    #hbp01 = 0
    #hbm01 = 72
    
    #hep01 = 144
    #hem01 = 216
    absValEta = abs(eta)
    hpdIndex = -1
    if eta > 0:
        if (absValEta < 16 or (absValEta==16 and depth < 3)):
            hpdIndex = (phi+1)%72
        elif (absValEta<21):
            hpdIndex = 144+(phi+1)%72
        elif (absValEta < 29):
            hpdIndex = 144+(phi+1)%72+(absValEta%2)
        elif absValEta==29:
            hpdIndex = 144+(phi+1)%72+depth-1
    elif eta < 0:
        if (absValEta < 16 or (absValEta==16 and depth < 3)):
            hpdIndex = 72+(phi+1)%72
        elif (absValEta<21):
            hpdIndex = 216+(phi+1)%72
        elif (absValEta < 29):
            hpdIndex = 216+(phi+1)%72+(absValEta%2)
        elif absValEta==29:
            hpdIndex = 216+(phi+1)%72+depth-1
    return hpdIndex

def map_channel_to_hpd2(eta,phi,depth):
    r.gROOT.SetBatch(True)
    absValEta = abs(eta)
    hpdIndex = -1
    if eta > 0 and (absValEta < 16 or (absValEta==16 and depth < 3)):
        hpdIndex = (phi+1)%72
    elif eta < 0 and (absValEta < 16 or (absValEta==16 and depth < 3)):
        hpdIndex = 72+(phi+1)%72
        #hpdIndex = 72+(phi+70)%72
        
    elif (absValEta<21):
        if eta > 0:
            hpdIndex = 144+(phi+1)%72
        elif eta < 0:
            hpdIndex = 216+(phi+1)%72
    elif (absValEta < 29):
        if eta > 0:
            hpdIndex = 144+(phi+1)%72+(absValEta%2)
        elif eta < 0:
            hpdIndex = 216+(phi+1)%72+(absValEta%2)
    elif absValEta==29:
        if eta > 0:
            hpdIndex = 144+(phi+1)%72+depth-1
        else:
            hpdIndex = 216+(phi+1)%72+depth-1
    #if absValEta > 0 and (
    #    (absValEta<15 and depth==1) or
    #    (absValEta in [15,16] and depth in [1,2]) or
    #    (absValEta in [16] and depth==3) or
    #    (absValEta in [17] and depth==1) or
    #    (absValEta in [18,19,20] and depth <3) or
    #    (phi%2==1 and (
    #            (absValEta > 20 and depth <3) or
    #            (absValEta in [27,28] and depth==3)
    #            ))
    #    ):
    #    print eta,phi,depth,hpdIndex

    ## iPhi plus: 71,1,3,5,...
    ## iPhi minus: 1,71,5,3,...
    ## HE HPD types, keyed by iphi
    # odd iEta -> hpd 2,3
    # even iEta -> hpd 1,4
    # iEta 29 depth 1 -> even iEta
    # iEta 29 depth 2 -> odd iEta
    # typeI:1,5,9,13,... depth 1-> hpd
    # typeII:3,7,11,15,... depth 1-> hpd 1
#    elif absValEta == 29:
#        if depth == 1:
#            hpdIndex = 
#        else:
#            hpdIndex =
#
#    else:
#        if absValEta%2 == 0:
#            ##should map to hpd's 1,4
#            hpdIndex = 
#        else:
#            ##should map to hpd's 1,4
#            hpdIndex = 
    return hpdIndex

if __name__ == '__main__':
    r.gROOT.SetBatch(True)
    main()
    #main("analyzingHPDs.root")
    #profile.run('main("outFile1.root")')
    #cProfile.run('main("outFile2.root")')

