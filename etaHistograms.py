import sys,os
import ROOT as r
from rootGarbageCollection import *

def main():
    r.gROOT.SetBatch(True)
    
    enCuts   = ["hits","hits15","hits30","hits50"]
    puBins = {
        "allPU":    [0,-1],
        "lowPU":    [1,12],
        "medPU":    [13,20],
        "highPU":   [21,28],
        "vhighPU":  [29,37],
        "extremePU":[38,-1],
        }

    #for puInfo in puBins.keys():
    #    for enCut in enCuts:
    #        print enCut,puInfo,puBins[puInfo]
    #        makeThePlots(enCut[0],puInfo,puBins[puInfo])

    makeThePlots(enCuts[0],"allPU",puBins["allPU"])

def makeThePlots(enCut,puLabel,puBounds):
    #myFile = r.TFile("fullHPDHistograms.root","READ")
    myFile = r.TFile("completeHPDHistograms.root","READ")
    
    plusCan = r.TCanvas("plusCan","plusCan",1600,1600)
    plusCan.cd()
    plusCan.Divide(5,6)
    
    minusCan = r.TCanvas("minusCan","minusCan",1600,1600)
    minusCan.cd()
    minusCan.Divide(5,6)
    
    summaryCan = r.TCanvas("summaryCan","summaryCan",1600,1600)
    summaryCan.cd()
    summaryCan.Divide(5,6)
    
    plusProbCan = r.TCanvas("plusProbCan","plusProbCan",1600,1600)
    plusProbCan.cd()
    plusProbCan.Divide(5,6)
    
    minusProbCan = r.TCanvas("minusProbCan","minusProbCan",1600,1600)
    minusProbCan.cd()
    minusProbCan.Divide(5,6)
    
    summaryProbCan = r.TCanvas("summaryProbCan","summaryProbCan",1600,1600)
    summaryProbCan.cd()
    summaryProbCan.Divide(5,6)
    
    for ieta in range(29):
        plusCan.cd(ieta+1)
        plus_histo    = myFile.Get("rechitoccupancy/etahists/rechits_ieta%dp_d1_vs_nvtx"%(ieta+1))
        plus_histo.Draw("colz")

        minusCan.cd(ieta+1)
        minus_histo   = myFile.Get("rechitoccupancy/etahists/rechits_ieta%dm_d1_vs_nvtx"%(ieta+1))
        minus_histo.Draw("colz")

        summaryCan.cd(ieta+1)
        summary_histo = plus_histo.Clone("rechits_vs_ieta%d_d1_vs_nvtx_summary"%(ieta+1))
        summary_histo.Add(minus_histo)
        summary_histo.Draw("colz")

        # ##
        plusProbCan.cd(ieta+1)
        plus_proj    = plus_histo.ProjectionX()
        plus_proj.Scale(1./plus_proj.GetEntries())
        plus_proj.SetMaximum(1)
        plus_proj.SetMarkerStyle(20)
        plus_proj.SetMinimum(0.000001)
        plus_proj.Draw()
        print plus_proj.Integral()

        minusProbCan.cd(ieta+1)
        minus_proj   = minus_histo.ProjectionX()
        minus_proj.Scale(1./minus_proj.GetEntries())
        minus_proj.SetMaximum(1)
        minus_proj.SetMinimum(0.000001)
        minus_proj.SetMarkerStyle(20)
        minus_proj.Draw()
        print minus_proj.Integral()

        summaryProbCan.cd(ieta+1)
        summary_proj = summary_histo.ProjectionX()
        summary_proj.Scale(1./summary_proj.GetEntries())
        summary_proj.SetMaximum(1)
        summary_proj.SetMinimum(0.000001)
        summary_proj.SetMarkerStyle(20)
        summary_proj.Draw()
        print summary_proj.Integral()

                        
    plusCan.SaveAs("ieta_plus2D.png")
    plusCan.SaveAs("ieta_plus2D.pdf")
    
    minusCan.SaveAs("ieta_minus2D.png")
    minusCan.SaveAs("ieta_minus2D.pdf")

    summaryCan.SaveAs("ieta_summary2D.png")
    summaryCan.SaveAs("ieta_summary2D.pdf")

    plusProbCan.SaveAs("ieta_plusProbability.png")
    plusProbCan.SaveAs("ieta_plusProbability.pdf")
    
    minusProbCan.SaveAs("ieta_minusProbability.png")
    minusProbCan.SaveAs("ieta_minusProbability.pdf")

    summaryProbCan.SaveAs("ieta_summaryProbability.png")
    summaryProbCan.SaveAs("ieta_summaryProbability.pdf")
    
    return

if __name__ == "__main__":
    main()
    
