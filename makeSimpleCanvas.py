import sys,os
import ROOT as r
from rootGarbageCollection import *
from array import array

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

    sample = "HcalHPDNoise"
    #rootFile = r.TFile("completeHPDHistograms.root","READ")
    rootFile = r.TFile("%s_hpdInformation.root"%(sample),"READ")
    fitVals = makeEtaProfiles("hits15",rootFile,sample)
    print fitVals
    makeEtaSlopePlot(1,fitVals,"hits15",sample)
    makeEtaSlopePlot(2,fitVals,"hits15",sample)
    makeEtaSlopePlot(3,fitVals,"hits15",sample)
    #for puInfo in puBins.keys():
    #    for enCut in enCuts:
    #        print enCut,puInfo,puBins[puInfo]
    #
    #        makeThePlots(enCut,puInfo,puBins[puInfo])

def makeEtaSlopePlot(depth,fitVals,enCut,sample):
    xvals = []
    xerrs = []
    yvals = []
    yerrs = []
    for eta in range(29):
        ieta = eta+1
        if ieta < 15 and depth > 1:
            continue
        elif ieta < 16 and depth > 2:
            continue
        elif ieta > 16 and ieta < 27 and depth > 2:
            continue
        elif ieta > 28 and depth > 2:
            continue

        xvals.append(ieta)
        xerrs.append(0.5)
        yvals.append(fitVals["ie%dd%d"%(ieta,depth)]["slope"])
        yerrs.append(fitVals["ie%dd%d"%(ieta,depth)]["slopeErr"])


    theCanvas = r.TCanvas("theCanvas","theCanvas",800,800)
    r.gPad.SetLogy(1)
    theCanvas.cd()
    myGraph = r.TGraphErrors(len(xvals),array('d',xvals),array('d',yvals),array('d',xerrs),array('d',yerrs))
    myGraph.SetMinimum(0.001)
    myGraph.SetMaximum(2)
    myGraph.SetMarkerStyle(23)
    myGraph.SetMarkerSize(1)
    myGraph.Draw("aep")
    
    theCanvas.SaveAs("%s_slope_vs_ieta_d%d_cut_%s.png"%(sample,depth,enCut))
    theCanvas.SaveAs("%s_slope_vs_ieta_d%d_cut_%s.pdf"%(sample,depth,enCut))
    return
def makeEtaProfiles(enCut,rootFile,sample):
    depth1HitsCan = r.TCanvas("depth1HitsCan","depth1HitsCan",1600,1600)
    depth1HitsCan.cd()
    depth1HitsCan.Divide(5,6)
    depth2HitsCan = r.TCanvas("depth2HitsCan","depth2HitsCan",1600,1600)
    depth2HitsCan.cd()
    depth2HitsCan.Divide(5,6)
    depth3HitsCan = r.TCanvas("depth3HitsCan","depth3HitsCan",1600,1600)
    depth3HitsCan.cd()
    depth3HitsCan.Divide(5,6)

    depth1Can = r.TCanvas("depth1Can","depth1Can",1600,1600)
    depth1Can.cd()
    depth1Can.Divide(5,6)
    depth2Can = r.TCanvas("depth2Can","depth2Can",1600,1600)
    depth2Can.cd()
    depth2Can.Divide(5,6)
    depth3Can = r.TCanvas("depth3Can","depth3Can",1600,1600)
    depth3Can.cd()
    depth3Can.Divide(5,6)

    fitVals = {}

    for eta in range(29):
        ieta = eta + 1
        for depth in range(3):
            idepth = depth + 1
            if ieta < 15 and depth > 0:
                continue
            elif ieta < 16 and depth > 1:
                continue
            elif ieta > 16 and ieta < 27 and depth > 1:
                continue
            elif ieta > 28 and depth > 1:
                continue

            if idepth == 1:
                depth1HitsCan.cd(ieta)
            elif idepth == 2:
                depth2HitsCan.cd(ieta)
            elif idepth == 3:
                depth3HitsCan.cd(ieta)

            histoName = "rechitoccupancy/etahists/rec%s_ieta%d_d%d_vs_nvtx"%(enCut,ieta,idepth)
            print histoName
            sys.stdout.flush()
            baseHisto = rootFile.Get(histoName)
            print baseHisto
            sys.stdout.flush()
            baseHisto.Draw("colz")
            
            if idepth == 1:
                depth1Can.cd(ieta)
            elif idepth == 2:
                depth2Can.cd(ieta)
            elif idepth == 3:
                depth3Can.cd(ieta)

            r.gStyle.SetOptFit(1111)
            profileHist = baseHisto.ProfileX("profile_ieta%d_d%d_vs_nvtx"%(ieta,idepth))

            profileFit = r.TF1("profileFit","pol1",3,39)
            profileHist.Fit(profileFit,"REMF")
            profileOffset = profileFit.GetParameter(0 )
            profileOffsetErr = profileFit.GetParError(0)
            profileSlope = profileFit.GetParameter(1)
            profileSlopeErr = profileFit.GetParError(1)
            fitVals["ie%dd%d"%(ieta,idepth)] = {"offset":profileOffset,
                                                "offsetErr":profileOffsetErr,
                                                "slope":profileSlope,
                                                "slopeErr":profileSlopeErr}
            
    depth1Can.SaveAs("%s_%s_profile_ieta_vs_nvtx_depth1.png"%(sample,enCut))
    depth1Can.SaveAs("%s_%s_profile_ieta_vs_nvtx_depth1.pdf"%(sample,enCut))
    depth2Can.SaveAs("%s_%s_profile_ieta_vs_nvtx_depth2.png"%(sample,enCut))
    depth2Can.SaveAs("%s_%s_profile_ieta_vs_nvtx_depth2.pdf"%(sample,enCut))
    depth3Can.SaveAs("%s_%s_profile_ieta_vs_nvtx_depth3.png"%(sample,enCut))
    depth3Can.SaveAs("%s_%s_profile_ieta_vs_nvtx_depth3.pdf"%(sample,enCut))

    depth1HitsCan.SaveAs("%s_%s_ieta_vs_nvtx_depth1.png"%(sample,enCut))
    depth1HitsCan.SaveAs("%s_%s_ieta_vs_nvtx_depth1.pdf"%(sample,enCut))
    depth2HitsCan.SaveAs("%s_%s_ieta_vs_nvtx_depth2.png"%(sample,enCut))
    depth2HitsCan.SaveAs("%s_%s_ieta_vs_nvtx_depth2.pdf"%(sample,enCut))
    depth3HitsCan.SaveAs("%s_%s_ieta_vs_nvtx_depth3.png"%(sample,enCut))
    depth3HitsCan.SaveAs("%s_%s_ieta_vs_nvtx_depth3.pdf"%(sample,enCut))
    return fitVals

def makeThePlots(enCut,puLabel,puBounds):
    myFile = r.TFile("fullHPDHistograms.root","READ")
    
    summaryCan1 = r.TCanvas("summaryCan1","summaryCan1",1600,1600)
    summaryCan1.cd()
    summaryCan1.Divide(2,2)
    
    summaryCan2 = r.TCanvas("summaryCan2","summaryCan2",1600,1600)
    summaryCan2.cd()
    summaryCan2.Divide(2,2)
    
    hbpCan1 = r.TCanvas("hbpCan1","hbpCan1",1600,900)
    hbpCan1.cd()
    hbpCan1.Divide(9,4)
    hbmCan1 = r.TCanvas("hbmCan1","hbmCan1",1600,900)
    hbmCan1.cd()
    hbmCan1.Divide(9,4)
    hepCan1 = r.TCanvas("hepCan1","hepCan1",1600,900)
    hepCan1.cd()
    hepCan1.Divide(9,4)
    hemCan1 = r.TCanvas("hemCan1","hemCan1",1600,900)
    hemCan1.cd()
    hemCan1.Divide(9,4)
    
    hbpCan2 = r.TCanvas("hbpCan2","hbpCan2",1600,900)
    hbpCan2.cd()
    hbpCan2.Divide(9,4)
    hbmCan2 = r.TCanvas("hbmCan2","hbmCan2",1600,900)
    hbmCan2.cd()
    hbmCan2.Divide(9,4)
    hepCan2 = r.TCanvas("hepCan2","hepCan2",1600,900)
    hepCan2.cd()
    hepCan2.Divide(9,4)
    hemCan2 = r.TCanvas("hemCan2","hemCan2",1600,900)
    hemCan2.cd()
    hemCan2.Divide(9,4)

    for be in ["B","E"]:
        for pm in ["P","M"]:
            
            #print "%s_vs_nvtx_H%s%s"%(enCut,be,pm)
            histoName_summary = myFile.Get("%s_vs_nvtx_H%s%s"%(enCut,be,pm))
            
            #print histoName_summary.GetName()
            profile_summary = histoName_summary.ProfileX()
            profile_summary = histoName_summary.ProfileX()
            if be == "B" and pm == "P":
                summaryCan1.cd(1)
            elif be == "B" and pm == "M":
                summaryCan1.cd(3)
            elif be == "E" and pm == "P":
                summaryCan1.cd(2)
            elif be == "E" and pm == "M":
                summaryCan1.cd(4)
                
            profile_summary.Draw("")


            projection_summary = histoName_summary.ProjectionY(histoName_summary.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
            projection_summary.Scale(1./projection_summary.GetEntries())
            projection_summary.SetMaximum(1)
            projection_summary.SetMinimum(0.000001)
            if be == "B" and pm == "P":
                summaryCan2.cd(1)
                r.gPad.SetLogy(1)
                projection_summary.Draw("")
            elif be == "B" and pm == "M":
                summaryCan2.cd(3)
                r.gPad.SetLogy(1)
                projection_summary.Draw("")
            elif be == "E" and pm == "P":
                summaryCan2.cd(2)
                r.gPad.SetLogy(1)
                projection_summary.Draw("")
            elif be == "E" and pm == "M":
                summaryCan2.cd(4)
                r.gPad.SetLogy(1)
                projection_summary.Draw("")

        #projection_summary.Draw("colz")


            for rbxIdx in range(18):
                keyName = "H%s%s%02d"%(be,pm,rbxIdx)
                
                
                histoName_hpd1 = myFile.Get("%s_vs_nvtx_%s_HPD0"%(enCut,keyName))
                histoName_hpd2 = myFile.Get("%s_vs_nvtx_%s_HPD1"%(enCut,keyName))
                histoName_hpd3 = myFile.Get("%s_vs_nvtx_%s_HPD2"%(enCut,keyName))
                histoName_hpd4 = myFile.Get("%s_vs_nvtx_%s_HPD3"%(enCut,keyName))
                
                if be == "B" and pm == "P":
                    if rbxIdx < 9:
                        hbpCan1.cd(rbxIdx+1)
                        histoName_hpd1.Draw("colz")
                        hbpCan1.cd(10+rbxIdx)
                        histoName_hpd2.Draw("colz")
                        hbpCan1.cd(19+rbxIdx)
                        histoName_hpd3.Draw("colz")
                        hbpCan1.cd(28+rbxIdx)
                        histoName_hpd4.Draw("colz")

                    else:
                        hbpCan2.cd(rbxIdx+1-9)
                        histoName_hpd1.Draw("colz")
                        hbpCan2.cd(10+rbxIdx-9)
                        histoName_hpd2.Draw("colz")
                        hbpCan2.cd(19+rbxIdx-9)
                        histoName_hpd3.Draw("colz")
                        hbpCan2.cd(28+rbxIdx-9)
                        histoName_hpd4.Draw("colz")
                elif be == "B" and pm == "M":
                    if rbxIdx < 9:
                        hbmCan1.cd(rbxIdx+1)
                        histoName_hpd1.Draw("colz")
                        hbmCan1.cd(10+rbxIdx)
                        histoName_hpd2.Draw("colz")
                        hbmCan1.cd(19+rbxIdx)
                        histoName_hpd3.Draw("colz")
                        hbmCan1.cd(28+rbxIdx)
                        histoName_hpd4.Draw("colz")
                        
                    else:
                        hbmCan2.cd(rbxIdx+1-9)
                        histoName_hpd1.Draw("colz")
                        hbmCan2.cd(10+rbxIdx-9)
                        histoName_hpd2.Draw("colz")
                        hbmCan2.cd(19+rbxIdx-9)
                        histoName_hpd3.Draw("colz")
                        hbmCan2.cd(28+rbxIdx-9)
                        histoName_hpd4.Draw("colz")
                        
                elif be == "E" and pm == "P":
                    if rbxIdx < 9:
                        hepCan1.cd(rbxIdx+1)
                        histoName_hpd1.Draw("colz")
                        hepCan1.cd(10+rbxIdx)
                        histoName_hpd2.Draw("colz")
                        hepCan1.cd(19+rbxIdx)
                        histoName_hpd3.Draw("colz")
                        hepCan1.cd(28+rbxIdx)
                        histoName_hpd4.Draw("colz")
                        
                    else:
                        hepCan2.cd(rbxIdx+1-9)
                        histoName_hpd1.Draw("colz")
                        hepCan2.cd(10+rbxIdx-9)
                        histoName_hpd2.Draw("colz")
                        hepCan2.cd(19+rbxIdx-9)
                        histoName_hpd3.Draw("colz")
                        hepCan2.cd(28+rbxIdx-9)
                        histoName_hpd4.Draw("colz")
                elif be == "E" and pm == "M":
                    if rbxIdx < 9:
                        hemCan1.cd(rbxIdx+1)
                        histoName_hpd1.Draw("colz")
                        hemCan1.cd(10+rbxIdx)
                        histoName_hpd2.Draw("colz")
                        hemCan1.cd(19+rbxIdx)
                        histoName_hpd3.Draw("colz")
                        hemCan1.cd(28+rbxIdx)
                        histoName_hpd4.Draw("colz")
                        
                    else:
                        hemCan2.cd(rbxIdx+1-9)
                        histoName_hpd1.Draw("colz")
                        hemCan2.cd(10+rbxIdx-9)
                        histoName_hpd2.Draw("colz")
                        hemCan2.cd(19+rbxIdx-9)
                        histoName_hpd3.Draw("colz")
                        hemCan2.cd(28+rbxIdx-9)
                        histoName_hpd4.Draw("colz")
                        
    summaryCan1.SaveAs("%s/summaryProfile.png"%(enCut))
    summaryCan1.SaveAs("%s/summaryProfile.pdf"%(enCut))
    
    summaryCan2.SaveAs("%s/summaryHitProbability_%s.png"%(enCut,puLabel))
    summaryCan2.SaveAs("%s/summaryHitProbability_%s.pdf"%(enCut,puLabel))
    
    hbpCan1.SaveAs("%s/hbpCan1.png"%(enCut))
    hbmCan1.SaveAs("%s/hbmCan1.png"%(enCut))
    hepCan1.SaveAs("%s/hepCan1.png"%(enCut))
    hemCan1.SaveAs("%s/hemCan1.png"%(enCut))
    
    hbpCan2.SaveAs("%s/hbpCan2.png"%(enCut))
    hbmCan2.SaveAs("%s/hbmCan2.png"%(enCut))
    hepCan2.SaveAs("%s/hepCan2.png"%(enCut))
    hemCan2.SaveAs("%s/hemCan2.png"%(enCut))
    
    
    hbpCan1.SaveAs("%s/hbpCan1.pdf"%(enCut))
    hbmCan1.SaveAs("%s/hbmCan1.pdf"%(enCut))
    hepCan1.SaveAs("%s/hepCan1.pdf"%(enCut))
    hemCan1.SaveAs("%s/hemCan1.pdf"%(enCut))
    
    hbpCan2.SaveAs("%s/hbpCan2.pdf"%(enCut))
    hbmCan2.SaveAs("%s/hbmCan2.pdf"%(enCut))
    hepCan2.SaveAs("%s/hepCan2.pdf"%(enCut))
    hemCan2.SaveAs("%s/hemCan2.pdf"%(enCut))
    
    for rbxIdx in range(18):
        for be in ["B","E"]:
            for pm in ["P","M"]:
                keyName = "H%s%s%02d"%(be,pm,rbxIdx)
                
                histoName_hpd1 = myFile.Get("%s_vs_nvtx_%s_HPD0"%(enCut,keyName))
                histoName_hpd2 = myFile.Get("%s_vs_nvtx_%s_HPD1"%(enCut,keyName))
                histoName_hpd3 = myFile.Get("%s_vs_nvtx_%s_HPD2"%(enCut,keyName))
                histoName_hpd4 = myFile.Get("%s_vs_nvtx_%s_HPD3"%(enCut,keyName))
                
                if be == "B" and pm == "P":
                    if rbxIdx < 9:
                        hbpCan1.cd(rbxIdx+1)
                        r.gPad.SetLogy(1)
                        projection_hpd1 = histoName_hpd1.ProjectionY(histoName_hpd1.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd1.Scale(1./projection_hpd1.GetEntries())
                        projection_hpd1.SetMaximum(1)
                        projection_hpd1.SetMinimum(0.000001)
                        projection_hpd1.Draw()
                        
                        hbpCan1.cd(10+rbxIdx)
                        r.gPad.SetLogy(1)
                        projection_hpd2 = histoName_hpd2.ProjectionY(histoName_hpd2.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd2.Scale(1./projection_hpd2.GetEntries())
                        projection_hpd2.SetMaximum(1)
                        projection_hpd2.SetMinimum(0.000001)
                        projection_hpd2.Draw()
                        
                        hbpCan1.cd(19+rbxIdx)
                        r.gPad.SetLogy(1)
                        projection_hpd3 = histoName_hpd3.ProjectionY(histoName_hpd3.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd3.Scale(1./projection_hpd3.GetEntries())
                        projection_hpd3.SetMaximum(1)
                        projection_hpd3.SetMinimum(0.000001)
                        projection_hpd3.Draw()
                        
                        hbpCan1.cd(28+rbxIdx)
                        r.gPad.SetLogy(1)
                        projection_hpd4 = histoName_hpd4.ProjectionY(histoName_hpd4.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd4.Scale(1./projection_hpd4.GetEntries())
                        projection_hpd4.SetMaximum(1)
                        projection_hpd4.SetMinimum(0.000001)
                        projection_hpd4.Draw()
                        
                    else:
                        hbpCan2.cd(rbxIdx+1-9)
                        r.gPad.SetLogy(1)
                        projection_hpd1 = histoName_hpd1.ProjectionY(histoName_hpd1.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd1.Scale(1./projection_hpd1.GetEntries())
                        projection_hpd1.SetMaximum(1)
                        projection_hpd1.SetMinimum(0.000001)
                        projection_hpd1.Draw()
                        
                        hbpCan2.cd(10+rbxIdx-9)
                        r.gPad.SetLogy(1)
                        projection_hpd2 = histoName_hpd2.ProjectionY(histoName_hpd2.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd2.Scale(1./projection_hpd2.GetEntries())
                        projection_hpd2.SetMaximum(1)
                        projection_hpd2.SetMinimum(0.000001)
                        projection_hpd2.Draw()
                        
                        hbpCan2.cd(19+rbxIdx-9)
                        r.gPad.SetLogy(1)
                        projection_hpd3 = histoName_hpd3.ProjectionY(histoName_hpd3.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd3.Scale(1./projection_hpd3.GetEntries())
                        projection_hpd3.SetMaximum(1)
                        projection_hpd3.SetMinimum(0.000001)
                        projection_hpd3.Draw()
                        
                        hbpCan2.cd(28+rbxIdx-9)
                        r.gPad.SetLogy(1)
                        projection_hpd4 = histoName_hpd4.ProjectionY(histoName_hpd4.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd4.Scale(1./projection_hpd4.GetEntries())
                        projection_hpd4.SetMaximum(1)
                        projection_hpd4.SetMinimum(0.000001)
                        projection_hpd4.SetMaximum(1)
                        projection_hpd4.SetMinimum(0.000001)
                        projection_hpd4.Draw()
                        
                elif be == "B" and pm == "M":
                    if rbxIdx < 9:
                        hbmCan1.cd(rbxIdx+1)
                        r.gPad.SetLogy(1)
                        projection_hpd1 = histoName_hpd1.ProjectionY(histoName_hpd1.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd1.Scale(1./projection_hpd1.GetEntries())
                        projection_hpd1.SetMaximum(1)
                        projection_hpd1.SetMinimum(0.000001)
                        projection_hpd1.Draw()
                        
                        hbmCan1.cd(10+rbxIdx)
                        r.gPad.SetLogy(1)
                        projection_hpd2 = histoName_hpd2.ProjectionY(histoName_hpd2.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd2.Scale(1./projection_hpd2.GetEntries())
                        projection_hpd2.SetMaximum(1)
                        projection_hpd2.SetMinimum(0.000001)
                        projection_hpd2.Draw()
                        
                        hbmCan1.cd(19+rbxIdx)
                        r.gPad.SetLogy(1)
                        projection_hpd3 = histoName_hpd3.ProjectionY(histoName_hpd3.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd3.Scale(1./projection_hpd3.GetEntries())
                        projection_hpd3.SetMaximum(1)
                        projection_hpd3.SetMinimum(0.000001)
                        projection_hpd3.Draw()
                        
                        hbmCan1.cd(28+rbxIdx)
                        r.gPad.SetLogy(1)
                        projection_hpd4 = histoName_hpd4.ProjectionY(histoName_hpd4.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd4.Scale(1./projection_hpd4.GetEntries())
                        projection_hpd4.SetMaximum(1)
                        projection_hpd4.SetMinimum(0.000001)
                        projection_hpd4.Draw()
                        
                    else:
                        hbmCan2.cd(rbxIdx+1-9)
                        r.gPad.SetLogy(1)
                        projection_hpd1 = histoName_hpd1.ProjectionY(histoName_hpd1.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd1.Scale(1./projection_hpd1.GetEntries())
                        projection_hpd1.SetMaximum(1)
                        projection_hpd1.SetMinimum(0.000001)
                        projection_hpd1.Draw()
                        
                        hbmCan2.cd(10+rbxIdx-9)
                        r.gPad.SetLogy(1)
                        projection_hpd2 = histoName_hpd2.ProjectionY(histoName_hpd2.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd2.Scale(1./projection_hpd2.GetEntries())
                        projection_hpd2.SetMaximum(1)
                        projection_hpd2.SetMinimum(0.000001)
                        projection_hpd2.Draw()
                        
                        hbmCan2.cd(19+rbxIdx-9)
                        r.gPad.SetLogy(1)
                        projection_hpd3 = histoName_hpd3.ProjectionY(histoName_hpd3.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd3.Scale(1./projection_hpd3.GetEntries())
                        projection_hpd3.SetMaximum(1)
                        projection_hpd3.SetMinimum(0.000001)
                        projection_hpd3.Draw()
                        
                        hbmCan2.cd(28+rbxIdx-9)
                        r.gPad.SetLogy(1)
                        projection_hpd4 = histoName_hpd4.ProjectionY(histoName_hpd4.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd4.Scale(1./projection_hpd4.GetEntries())
                        projection_hpd4.SetMaximum(1)
                        projection_hpd4.SetMinimum(0.000001)
                        projection_hpd4.Draw()
                        
                elif be == "E" and pm == "P":
                    if rbxIdx < 9:
                        hepCan1.cd(rbxIdx+1)
                        r.gPad.SetLogy(1)
                        projection_hpd1 = histoName_hpd1.ProjectionY(histoName_hpd1.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd1.Scale(1./projection_hpd1.GetEntries())
                        projection_hpd1.SetMaximum(1)
                        projection_hpd1.SetMinimum(0.000001)
                        projection_hpd1.Draw()
                        
                        hepCan1.cd(10+rbxIdx)
                        r.gPad.SetLogy(1)
                        projection_hpd2 = histoName_hpd2.ProjectionY(histoName_hpd2.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd2.Scale(1./projection_hpd2.GetEntries())
                        projection_hpd2.SetMaximum(1)
                        projection_hpd2.SetMinimum(0.000001)
                        projection_hpd2.Draw()
                        
                        hepCan1.cd(19+rbxIdx)
                        r.gPad.SetLogy(1)
                        projection_hpd3 = histoName_hpd3.ProjectionY(histoName_hpd3.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd3.Scale(1./projection_hpd3.GetEntries())
                        projection_hpd3.SetMaximum(1)
                        projection_hpd3.SetMinimum(0.000001)
                        projection_hpd3.Draw()
                        
                        hepCan1.cd(28+rbxIdx)
                        r.gPad.SetLogy(1)
                        projection_hpd4 = histoName_hpd4.ProjectionY(histoName_hpd4.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd4.Scale(1./projection_hpd4.GetEntries())
                        projection_hpd4.SetMaximum(1)
                        projection_hpd4.SetMinimum(0.000001)
                        projection_hpd4.Draw()
                        
                    else:
                        hepCan2.cd(rbxIdx+1-9)
                        r.gPad.SetLogy(1)
                        projection_hpd1 = histoName_hpd1.ProjectionY(histoName_hpd1.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd1.Scale(1./projection_hpd1.GetEntries())
                        projection_hpd1.SetMaximum(1)
                        projection_hpd1.SetMinimum(0.000001)
                        projection_hpd1.Draw()
                        
                        hepCan2.cd(10+rbxIdx-9)
                        r.gPad.SetLogy(1)
                        projection_hpd2 = histoName_hpd2.ProjectionY(histoName_hpd2.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd2.Scale(1./projection_hpd2.GetEntries())
                        projection_hpd2.SetMaximum(1)
                        projection_hpd2.SetMinimum(0.000001)
                        projection_hpd2.Draw()
                        
                        hepCan2.cd(19+rbxIdx-9)
                        r.gPad.SetLogy(1)
                        projection_hpd3 = histoName_hpd3.ProjectionY(histoName_hpd3.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd3.Scale(1./projection_hpd3.GetEntries())
                        projection_hpd3.SetMaximum(1)
                        projection_hpd3.SetMinimum(0.000001)
                        projection_hpd3.Draw()
                        
                        hepCan2.cd(28+rbxIdx-9)
                        r.gPad.SetLogy(1)
                        projection_hpd4 = histoName_hpd4.ProjectionY(histoName_hpd4.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd4.Scale(1./projection_hpd4.GetEntries())
                        projection_hpd4.SetMaximum(1)
                        projection_hpd4.SetMinimum(0.000001)
                        projection_hpd4.Draw()
                        
                elif be == "E" and pm == "M":
                    if rbxIdx < 9:
                        hemCan1.cd(rbxIdx+1)
                        r.gPad.SetLogy(1)
                        projection_hpd1 = histoName_hpd1.ProjectionY(histoName_hpd1.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd1.Scale(1./projection_hpd1.GetEntries())
                        projection_hpd1.SetMaximum(1)
                        projection_hpd1.SetMinimum(0.000001)
                        projection_hpd1.Draw()
                        
                        hemCan1.cd(10+rbxIdx)
                        r.gPad.SetLogy(1)
                        projection_hpd2 = histoName_hpd2.ProjectionY(histoName_hpd2.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd2.Scale(1./projection_hpd2.GetEntries())
                        projection_hpd2.SetMaximum(1)
                        projection_hpd2.SetMinimum(0.000001)
                        projection_hpd2.Draw()
                        
                        hemCan1.cd(19+rbxIdx)
                        r.gPad.SetLogy(1)
                        projection_hpd3 = histoName_hpd3.ProjectionY(histoName_hpd3.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd3.Scale(1./projection_hpd3.GetEntries())
                        projection_hpd3.SetMaximum(1)
                        projection_hpd3.SetMinimum(0.000001)
                        projection_hpd3.Draw()
                        
                        hemCan1.cd(28+rbxIdx)
                        r.gPad.SetLogy(1)
                        projection_hpd4 = histoName_hpd4.ProjectionY(histoName_hpd4.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd4.Scale(1./projection_hpd4.GetEntries())
                        projection_hpd4.SetMaximum(1)
                        projection_hpd4.SetMinimum(0.000001)
                        projection_hpd4.Draw()
                        
                    else:
                        hemCan2.cd(rbxIdx+1-9)
                        r.gPad.SetLogy(1)
                        projection_hpd1 = histoName_hpd1.ProjectionY(histoName_hpd1.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd1.Scale(1./projection_hpd1.GetEntries())
                        projection_hpd1.SetMaximum(1)
                        projection_hpd1.SetMinimum(0.000001)
                        projection_hpd1.Draw()
                        
                        hemCan2.cd(10+rbxIdx-9)
                        r.gPad.SetLogy(1)
                        projection_hpd2 = histoName_hpd2.ProjectionY(histoName_hpd2.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd2.Scale(1./projection_hpd2.GetEntries())
                        projection_hpd2.SetMaximum(1)
                        projection_hpd2.SetMinimum(0.000001)
                        projection_hpd2.Draw()
                        
                        hemCan2.cd(19+rbxIdx-9)
                        r.gPad.SetLogy(1)
                        projection_hpd3 = histoName_hpd3.ProjectionY(histoName_hpd3.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd3.Scale(1./projection_hpd3.GetEntries())
                        projection_hpd3.SetMaximum(1)
                        projection_hpd3.SetMinimum(0.000001)
                        projection_hpd3.Draw()
                        
                        hemCan2.cd(28+rbxIdx-9)
                        r.gPad.SetLogy(1)
                        projection_hpd4 = histoName_hpd4.ProjectionY(histoName_hpd4.GetName()+"_%s"%(puLabel),puBounds[0],puBounds[1])
                        projection_hpd4.Scale(1./projection_hpd4.GetEntries())
                        projection_hpd4.SetMaximum(1)
                        projection_hpd4.SetMinimum(0.000001)
                        projection_hpd4.Draw()
                        
                        
    hbpCan1.SaveAs("%s/hbpCan1_projection_%s.png"%(enCut,puLabel))
    hbmCan1.SaveAs("%s/hbmCan1_projection_%s.png"%(enCut,puLabel))
    hepCan1.SaveAs("%s/hepCan1_projection_%s.png"%(enCut,puLabel))
    hemCan1.SaveAs("%s/hemCan1_projection_%s.png"%(enCut,puLabel))
    
    hbpCan2.SaveAs("%s/hbpCan2_projection_%s.png"%(enCut,puLabel))
    hbmCan2.SaveAs("%s/hbmCan2_projection_%s.png"%(enCut,puLabel))
    hepCan2.SaveAs("%s/hepCan2_projection_%s.png"%(enCut,puLabel))
    hemCan2.SaveAs("%s/hemCan2_projection_%s.png"%(enCut,puLabel))
    
    
    hbpCan1.SaveAs("%s/hbpCan1_projection_%s.pdf"%(enCut,puLabel))
    hbmCan1.SaveAs("%s/hbmCan1_projection_%s.pdf"%(enCut,puLabel))
    hepCan1.SaveAs("%s/hepCan1_projection_%s.pdf"%(enCut,puLabel))
    hemCan1.SaveAs("%s/hemCan1_projection_%s.pdf"%(enCut,puLabel))
    
    hbpCan2.SaveAs("%s/hbpCan2_projection_%s.pdf"%(enCut,puLabel))
    hbmCan2.SaveAs("%s/hbmCan2_projection_%s.pdf"%(enCut,puLabel))
    hepCan2.SaveAs("%s/hepCan2_projection_%s.pdf"%(enCut,puLabel))
    hemCan2.SaveAs("%s/hemCan2_projection_%s.pdf"%(enCut,puLabel))
    return

if __name__ == "__main__":
    main()
    
