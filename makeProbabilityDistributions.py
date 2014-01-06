import datetime
import pickle
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
    parser.add_option('-r', '--fitRange',type='int',    action="store", default=40,         dest="fitRange")
    parser.add_option('-s', '--sample',  type='string', action="store", default="SingleMu", dest="sample")
    options, args = parser.parse_args()

    print options
    sys.stdout.flush()
    r.gROOT.SetBatch(True)
    samples = ["MultiJet","SingleMu","MET","HTMHT","HcalHPDNoise"]
    #sample = samples[1]
    sample = options.sample

    rootFile = r.TFile("%s_hpdInformation_v2.root"%(sample),"READ")
    myDay = datetime.date.today()
    outBaseDir = "%s_V0"%(myDay)
    mkdir_p(outBaseDir)
    mkdir_p("/afs/cern.ch/user/s/sturdy/public/html/HCAL/NoiseStudies/%s/"%(outBaseDir))
    outRootFile = r.TFile("%s_fitTo%d_hpdProbabilities_v2.root"%(sample,options.fitRange),"RECREATE")

    ##should probably do this once and store the results in a file
    ##then can read the information from a file rather than recreating
    ##the information every program run
    probFunc = {}
    for hits in ["","to15","15","15to30","30","30to50","50"]:
        if options.debug:
            print "%s - %s"%(options.sample,hits)
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
                        150,-0.5,149.5,20,-0.5,19.5)
        hpdHE0 = r.TH2D("%s_hits%s_hpdHE0"%(sample,hits),
                        "%s_hits%s_hpdHE0"%(sample,hits),
                        150,-0.5,149.5,20,-0.5,19.5)
        hpdHE1 = r.TH2D("%s_hits%s_hpdHE1"%(sample,hits),
                        "%s_hits%s_hpdHE1"%(sample,hits),
                        150,-0.5,149.5,20,-0.5,19.5)
        hpdHE  = r.TH2D("%s_hits%s_hpdHE" %(sample,hits),
                        "%s_hits%s_hpdHE" %(sample,hits),
                        150,-0.5,149.5,20,-0.5,19.5)
        
        probabilities = {}
        probFunc["hits%s"%(hits)] = {}
        puHistogram = hpdHBHitsActual.Clone("puHistogram_hits%s"%(hits))
        puHistogram.Add(hpdHEHitsActual)
        puDistribution = generatePileupDistribution(puHistogram)
        puDistribution.SetName("puDistribution_hits%s"%(hits))
        
        for nVtx in range(150):
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
                                                     "hits%sieta%dd%d"%(hits,etaval+1,depth+1),
                                                     #"%s%d"%(hits,(depth+1)*100+(etaval+1)),
                                                     options.debug)
                    if options.debug and ieta==28:
                        outEtaHist = printIEtaInfoVsNVTX(etaOccupancyHist,nPhiChannels,
                                                         "hits%sieta%dd%d"%(hits,etaval+1,depth+1),
                                                         #"%s%d"%(hits,(depth+1)*100+(etaval+1)),
                                                         True)

                    probFunc["hits%s"%hits]["ieta%dd%d"%(ieta,depth+1)] = makeEtaHitProbability(outEtaHist,options.fitRange)
                    for nVtx in range(outEtaHist.GetNbinsX()):
                        probabilities["nVtx%d"%(nVtx)]["d%d"%(depth+1)]["ieta%d"%(ieta)] = outEtaHist.GetBinContent(outEtaHist.FindBin(nVtx))
                    outEtaHist.SetMarkerStyle(20)
                    outEtaHist.SetStats(False)
                    outEtaHist.SetMaximum(1.0)
                    outEtaHist.SetMinimum(0.00001)
                    outEtaHist.SetTitle("hit>%s GeV probability i#eta==%d,depth==%d vs. N_{vtx}"%(hits,ieta,
                                                                                                  depth+1))
                    outEtaHist.Draw("p0")
                    r.gPad.SetLogy(1)
                    # ## here run a fit on the distribution of probabilities
                    # # and take the probabilites from here
                    # probFit = r.TF1("pol1","")

            etacanvas.SaveAs("~/public/html/HCAL/NoiseStudies/%s/%s_hits%s_ietad%dHitProbability.png"%(outBaseDir,sample,hits,depth+1))
            etacanvas.SaveAs("~/public/html/HCAL/NoiseStudies/%s/%s_hits%s_ietad%dHitProbability.pdf"%(outBaseDir,sample,hits,depth+1))
            if options.debug:
                print probabilities
                sys.stdout.flush()
        probFunc["hits%s"%(hits)]["nVtxInfo"] = probabilities
    outRootFile.cd()
    for hitKey in probFunc.keys():
        for funcKey in probFunc[hitKey].keys():
            if funcKey not in ["nVtxInfo"]:
                probFunc[hitKey][funcKey].Write()
    outRootFile.Close()
    pickle.dump(probFunc, open('%s_fitTo%d_probs_v2.pkl'%(options.sample,options.fitRange), 'wb'))
################
def mkdir_p(path):
    r.gROOT.SetBatch(True)
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

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

#############    
def generatePileupDistribution(histo):
    r.gROOT.SetBatch(True)
    puDist = histo.ProjectionX("puDist")
    puDist.Scale(1./puDist.GetEntries())
    return puDist
    
#############    
def makeEtaHitProbability(histo,fitRange):
    ## need to make sure probability never goes to 0 nor above 1
    # even still, using a poisson with probability as the mean
    # can't be correct, as there will be probability to get more than
    # 1 events, probably better to use the binomial with 1 try integrated
    # but this gave a much narrower distribution than was expected
    r.gROOT.SetBatch(True)
    fit = r.TF1("%s_fit"%(histo.GetName()),"pol1",4,fitRange)
    result = histo.Fit(fit,"REMFSO+")
    ##fitter = r.TVirtualFitter.GetFitter( r.TVirtualFitter() )
    #covm = result.GetCovarianceMatrix()
    #corm = result.GetCorrelationMatrix()
    #result.Print("V")
    #chi2 = fit.GetChisquare()
    #ndf  = fit.GetNDF()
    ##chi2ndf = chi2/ndf
    #p0   = fit.GetParameter(0)
    #e0   = fit.GetParError(0)
    #p1   = fit.GetParameter(1)
    #e1   = fit.GetParError(1)
    #covp0p1 = covm[0][1]
    
    return fit
    
#############    
if __name__ == "__main__":
    r.gROOT.SetBatch(True)
    main()
    
