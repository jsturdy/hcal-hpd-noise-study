import datetime
import sys,os,errno
import ROOT as r
import rootGarbageCollection
import numpy as numpy
from itertools import izip

import optparse

#############    
def main():
    parser = optparse.OptionParser(description="Switch debug info")
    parser.add_option('-d', '--debug',                  action="store_true", default=False, dest="debug")
    parser.add_option('-n', '--nevents', type='int',    action="store", default=1000000,    dest="nevents")
    parser.add_option('-v', '--vertices',type='int',    action="store", default=20,         dest="nVtx")
    parser.add_option('-s', '--sample',  type='string', action="store", default="SingleMu", dest="sample")
    options, args = parser.parse_args()

    r.gROOT.SetBatch(True)
    samples = ["MultiJet","SingleMu","MET","HTMHT","HcalHPDNoise"]
    #sample = samples[1]
    sample = options.sample

    rootFile = r.TFile("%s_hpdInformation.root"%(sample),"READ")
    myDay = datetime.date.today()
    mkdir_p("%s"%(myDay))
    outRootFile = r.TFile("%s_V5/%s_nvtx%d_hpdPredictions.root"%(myDay,sample,options.nVtx),"RECREATE")

    for hits in ["","15","30","50"]:
        hpdHBHitsActual = rootFile.Get(  "hpdInformation/hits%s_vs_nvtx_HBP"%(hits))
        hpdHBHitsActual.Add(rootFile.Get("hpdInformation/hits%s_vs_nvtx_HBM"%(hits)))
        hpdHEHitsActual = rootFile.Get(  "hpdInformation/hits%s_vs_nvtx_HEP"%(hits))
        hpdHEHitsActual.Add(rootFile.Get("hpdInformation/hits%s_vs_nvtx_HEM"%(hits)))
        
        #outRootFile.cd()
        
        newCanvas = r.TCanvas("newCanvas%s"%(hits),
                              "newCanvas%s"%(hits),1024,1024)
        newCanvas.Divide(2,2)
        hpdHB  = r.TH2D("%s_hits%s_hpdHB" %(sample,hits),
                        "%s_hits%s_hpdHB" %(sample,hits),
                        50,-0.5,49.5,20,-0.5,19.5)
        hpdHE0 = r.TH2D("%s_hits%s_hpdHE0"%(sample,hits),
                        "%s_hits%s_hpdHE0"%(sample,hits),
                        50,-0.5,49.5,20,-0.5,19.5)
        hpdHE1 = r.TH2D("%s_hits%s_hpdHE1"%(sample,hits),
                        "%s_hits%s_hpdHE1"%(sample,hits),
                        50,-0.5,49.5,20,-0.5,19.5)
        hpdHE  = r.TH2D("%s_hits%s_hpdHE" %(sample,hits),
                        "%s_hits%s_hpdHE" %(sample,hits),
                        50,-0.5,49.5,20,-0.5,19.5)
        
        probabilities = {}
        puHistogram = hpdHBHitsActual.Clone("puHistogram_hits%s"%(hits))
        puHistogram.Add(hpdHEHitsActual)
        puDistribution = generatePileupDistribution(puHistogram)
        puDistribution.SetName("puDistribution_hits%s"%(hits))
        
        for nVtx in range(75):
            probabilities["nVtx%d"%(nVtx)] = {"d1":{},"d2":{},"d3":{},
                                              "weight":puDistribution.GetBinContent(nVtx+1)}
            
        for depth in range(3):
            etacanvas = r.TCanvas("%s_hits%s_iEtaDepth%dCanvas"%(sample,hits,depth+1),
                                  "%s_hits%s_iEtaDepth%dCanvas"%(sample,hits,depth+1),1980,1980)
            etacanvas.Divide(5,6)
            for etaval in range(29):
                ieta = etaval+1
                basename = "rechitoccupancy/etahists/rechits"
                etaOccupancyHist = rootFile.Get("%s%s_ieta%d_d%d_vs_nvtx"%(basename,hits,ieta,depth+1))
                etacanvas.cd(ieta)
                nPhiChannels = 144.0
                if ieta > 20:
                    nPhiChannels = 72.0
                if etaOccupancyHist:
                    if options.debug:
                        print depth+1,ieta,options.nVtx
                    outEtaHist = printIEtaInfoVsNVTX(etaOccupancyHist,nPhiChannels,
                                                     "%s%d"%(hits,(depth+1)*100+(etaval+1)),
                                                     options.debug)
                    if options.debug and ieta==28:
                        outEtaHist = printIEtaInfoVsNVTX(etaOccupancyHist,nPhiChannels,
                                                         "%s%d"%(hits,(depth+1)*100+(etaval+1)),
                                                         True)

                    for nVtx in range(outEtaHist.GetNbinsX()):
                        probabilities["nVtx%d"%(nVtx)]["d%d"%(depth+1)]["ieta%d"%(ieta)] = outEtaHist.GetBinContent(outEtaHist.FindBin(nVtx))
                    outEtaHist.SetMarkerStyle(20)
                    outEtaHist.SetStats(False)
                    outEtaHist.SetMaximum(1.0)
                    outEtaHist.SetMinimum(0.001)
                    outEtaHist.SetTitle("hit>%s GeV probability i#eta==%d,depth==%d vs. N_{vtx}"%(hits,ieta,
                                                                                                  depth+1))
                    outEtaHist.Draw("p0")
                    r.gPad.SetLogy(1)
                
            etacanvas.SaveAs("%s_V5/%s_hits%s_ietad%dHitProbability.png"%(myDay,sample,hits,depth+1))
            etacanvas.SaveAs("%s_V5/%s_hits%s_ietad%dHitProbability.pdf"%(myDay,sample,hits,depth+1))
            if options.debug:
                print probabilities
                sys.stdout.flush()
        #############Timing code###########
        i = 0
        decade  = 0
        century = 0
        tsw = r.TStopwatch()
        tenpcount = 1
        onepcount = 1
        sys.stdout.flush()
        nVtx = options.nVtx
        probs = probabilities["nVtx%d"%(nVtx)]
        nTrials = int(options.nevents*probs["weight"])
        for trial in range(nTrials):
            if ( i==0):
                tsw.Start()
                # print('.', end='')
                sys.stdout.write('.')
                sys.stdout.flush()
            if ((i*10)/(nTrials) == tenpcount ) :
                tsw.Stop()
                time = tsw.RealTime()
                tsw.Start(r.kFALSE)
                finTime = 0.
                frac = (i*1.0)/(nTrials*1.0)
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
                    
            elif ( (i*100)/(nTrials) == onepcount ) :
                # print('.', end='')
                sys.stdout.write('.')
                sys.stdout.flush()
                onepcount = onepcount + 1
                
            i = i + 1
            # print nVtx
            # print probabilities["nVtx%d"%(nVtx)]["d1"]
            # print probabilities["nVtx%d"%(nVtx)]["d2"]
            # print probabilities["nVtx%d"%(nVtx)]["d3"]
            hbVal  = countHPDCounts(probs,True,1 ,False)
            he0Val = countHPDCounts(probs,False,0,False)
            he1Val = countHPDCounts(probs,False,1,False)
        
            outRootFile.cd()
            #for hbVal,he0Val,he1Val in izip(hbVals,he0Vals,he1Vals):
            hpdHB .Fill(nVtx+0.5,hbVal)
            hpdHE0.Fill(nVtx+0.5,he0Val)
            hpdHE1.Fill(nVtx+0.5,he1Val)
            hpdHE .Fill(nVtx+0.5,he0Val)
            hpdHE .Fill(nVtx+0.5,he1Val)
        ############### done with the loop

        newCanvas.cd(1)
        r.gPad.SetLogz(1)
        hpdHB .Draw("colz")
        newCanvas.cd(2)
        r.gPad.SetLogz(1)
        hpdHBHitsActual.Draw("colz")
        #hpdHE .Draw("colz")
        newCanvas.cd(3)
        r.gPad.SetLogz(1)
        hpdHE.Draw("colz")
        #hpdHE0.Draw("colz")
        newCanvas.cd(4)
        r.gPad.SetLogz(1)
        hpdHEHitsActual.Draw("colz")
        #hpdHE1.Draw("colz")
        newCanvas.SaveAs("%s_V5/%s_hits%s_hpdPredictedOccupancy.png"%(myDay,sample,hits))
        newCanvas.SaveAs("%s_V5/%s_hits%s_hpdPredictedOccupancy.pdf"%(myDay,sample,hits))
        
        hpdHB.Write()
        hpdHE0.Write()
        hpdHE1.Write()
        hpdHE.Write()
        
        hpdHBHitsActual.Write()
        hpdHEHitsActual.Write()
        puHistogram.Write()
        puDistribution.Write()
        #raw_input("Press Enter to continue...")
        
        #outRootFile.()
    #outRootFile.Save()
    outRootFile.cd()
    outRootFile.Close()

################
def mkdir_p(path):
    r.gROOT.SetBatch(True)
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
################
def countHPDCounts(probs,barrel,hpdType,useBinomial):
    r.gROOT.SetBatch(True)
    #hitsInEta = 
    odd = True
    channels = {"d1":{"etas":[]},
                "d2":{"etas":[]},
                "d3":{"etas":[]}
            }
    depths = ["d1","d2"]
    if barrel:
        channels["d1"]["etas"].extend(range(1,17))
        channels["d2"]["etas"].extend([15,16])
        #loop over ieta 1 to 16 depth 1
        #loop over ieta 15 and 16 depth 2
        #count the number of hits above threshold
    else:
        depths.append("d3")
        channels["d1"]["etas"].extend([17,18,19,20])
        channels["d2"]["etas"].extend([18,19,20])
        channels["d3"]["etas"].extend([16])
        if hpdType==1:
            odd = True
            channels["d1"]["etas"].extend([21,23,25,27])
            channels["d2"]["etas"].extend([21,23,25,27,29])
            channels["d3"]["etas"].extend([27])
            #(22,24,26,28 for odd==false
        else:
            odd = False
            channels["d1"]["etas"].extend([22,24,26,28,29])
            channels["d2"]["etas"].extend([22,24,26,28])
            channels["d3"]["etas"].extend([28])
            #[21,23,25,27] otherwise)

        #loop over ieta 17 to 29 depth 1
        #loop over ieta 18-29 depth 2
        #loop over ieta 16,27,28 depth 3
        #count the number of hits above threshold
    #print channels
    ##nTrials = int(nevents*probs["weight"])
    ##hitCounts = numpy.ndarray((nTrials,),int)
    ##for trial in range(nTrials):
    ##    hitCounts[trial] = 0
    hitCounts = 0
    for depth in depths:
        for eta in channels[depth]["etas"]:
            probability = probs[depth]["ieta%d"%(eta)]
            #print depth,eta,probability
            if useBinomial:
                for trial in range(nTrials):
                    isHitBin   = numpy.random.binomial(1,probability)
                    if isHitBin:
                        hitCounts += hit
            else:
                isHitPoiss = numpy.random.poisson(probability,1)
                if isHitPoiss[0]:
                    hitCounts += isHitPoiss[0]
    return hitCounts
#############    

def countHBHPDCounts(threshold):
    r.gROOT.SetBatch(True)
    #ieta 1 to 14 depth = 1
    #ieta 15 and 16 depth = 1,2
    
    return hitCounts
#############    

def printIEtaInfoVsNVTX(histo,nPhiChannels,jobNum,debug):
    r.gROOT.SetBatch(True)
    nBinsX = histo.GetNbinsX()
    nBinsY = histo.GetNbinsY()
    probHisto = r.TH1D("probHisto_%s"%(jobNum),"probHisto_%s"%(jobNum),nBinsX,-0.5,nBinsX-0.5)
    hitHisto  = r.TH1D("hitHisto_%s"%(jobNum),"hitHisto_%s"%(jobNum),nBinsX,-0.5,nBinsX-0.5)
    for xBin in range(nBinsX):
        nVtx = xBin
        totalHitCounts = 0
        weightedHitCounts = 0
        #print "nVtx,recHitCounts,thisBinHits,totalHitCounts,weightedHitCounts"
        for yBin in range(nBinsY):
            recHitCounts = yBin
            thisBinHits = histo.GetBinContent(nVtx+1,recHitCounts+1)
            totalHitCounts = totalHitCounts + thisBinHits
            weightedHitCounts = weightedHitCounts + (recHitCounts*thisBinHits)
            #print nVtx,recHitCounts,thisBinHits,totalHitCounts,weightedHitCounts
        avgHits = 0.0
        if totalHitCounts>0:
            avgHits = weightedHitCounts/totalHitCounts
        hitProb = avgHits/nPhiChannels
        if debug:
            print "nVtx,totalHitCounts,weightedHitCounts,avgHits,prob"
            print nVtx,totalHitCounts,weightedHitCounts,avgHits,hitProb
        hitHisto.SetBinContent(nVtx+1,avgHits)
        probHisto.SetBinContent(nVtx+1,hitProb)
        #raw_input("Press Enter to continue...")
    #probHisto.Draw()
    #raw_input("Press Enter to continue...")
    #hitHisto.Draw()
    #raw_input("Press Enter to continue...")
    return probHisto
    #return hitHisto
#############    

def makeHPDHitProbability(histo,binNumber):
    r.gROOT.SetBatch(True)
    projection = histo.ProjectionY(histo.GetName()+"_npv%d"%(binNumber-1),binNumber,binNumber,"e")
    projection.SetTitle("HPD hit probability N_{vtx}==%d"%(binNumber-1))
    projection.GetXaxis().SetTitle("HPD hits")
    projection.SetStats(r.kFALSE)
    entries =  projection.GetEntries()
    #print binNumber,entries
    if entries > 0:
        projection.Scale(1./entries)
    projection.SetMaximum(1)
    projection.SetMinimum(0.000001)
    
    return projection

def generatePileupDistribution(histo):
    r.gROOT.SetBatch(True)
    puDist = histo.ProjectionX("puDist")
    puDist.Scale(1./puDist.GetEntries())
    return puDist
    
#############    
if __name__ == "__main__":
    r.gROOT.SetBatch(True)
    main()
    
