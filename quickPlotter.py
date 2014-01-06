import sys,os
import ROOT as r
from rootGarbageCollection import *

r.gROOT.SetBatch(True)
        
chain = r.TChain("ExportTree/HcalNoiseTree")
chain.Add("root://eoscms//eos/cms/store/caf/user/chenyi/HcalNoiseTree/V00-03-12142/537p6/FT_P_V42D/HBHEYesHFNoHONo/000003/HTMHT/NoiseTree_*.root")

##Make plot of individual channel occupancy as a function of #Vtx
##Measure this slope as a function of iEta
##Make plot of individual channel occupancy as a function of #Vtx, combining stats from all barrel channels,
## and all endcap channels
##make these plots as a function of the threshold on individual channel contributions (1.5/3/5 GeV)
##have to add up these values to get the individual HPD occupancies
##HPD is constructed from consecutive values in iEta and iPhi

analysisTree = chain
branches = {
    "RunNumber",       #RunNumber
    "EventNumber",     #EventNumber
    "LumiSection",     #LumiSection
    "Bunch",           #Bunch
    "Orbit",           #Orbit
    "Time",    #Time
    "TTrigger",        #TTrigger[64]
    "L1Trigger",       #L1Trigger[128]
    "HLTrigger",      #HLTrigger[256]
    "EBET",    #EBET[2]
    "EEET",    #EEET[2]
    "HBET",    #HBET[2]
    "HEET",    #HEET[2]
    "HFET",    #HFET[2]
    "NominalMET",      #NominalMET[2]
    "EBSumE",  #EBSumE
    "EESumE",  #EESumE
    "HBSumE",  #HBSumE
    "HESumE",  #HESumE
    "HFSumE",  #HFSumE
    "EBSumET", #EBSumET
    "EESumET", #EESumET
    "HBSumET", #HBSumET
    "HESumET", #HESumET
    "HFSumET", #HFSumET
    "NumberOfGoodTracks",      #NumberOfGoodTracks
    "NumberOfGoodTracks15",    #NumberOfGoodTracks15
    "NumberOfGoodTracks30",    #NumberOfGoodTracks30
    "TotalPTTracks",   #TotalPTTracks[2]
    "SumPTTracks",     #SumPTTracks
    "SumPTracks",      #SumPTracks
    "NumberOfGoodPrimaryVertices",     #NumberOfGoodPrimaryVertices
    "NumberOfMuonCandidates",          #NumberOfMuonCandidates
    "NumberOfCosmicMuonCandidates",    #NumberOfCosmicMuonCandidates
    "PulseCount",      #PulseCount
    "Charge",          #Charge[5184][10]
    "Pedestal",        #Pedestal[5184][10]
    "Energy",          #Energy[5184]
    "IEta",            #IEta[5184]
    "IPhi",            #IPhi[5184]
    "Depth",           #Depth[5184]
    "RecHitTime",      #RecHitTime[5184]
    "FlagWord",        #FlagWord[5184]
    "AuxWord",         #AuxWord[5184]
    "RespCorrGain",    #RespCorrGain[5184]
    "fCorr",           #fCorr[5184]
    "SamplesToAdd",    #SamplesToAdd [5184]
    "RBXCharge",       #RBXCharge[72][10]
    "RBXEnergy",       #RBXEnergy[72]
    "RBXCharge15",     #RBXCharge15[72][10]
    "RBXEnergy15",     #RBXEnergy15[72]
    "HPDHits",         #HPDHits
    "HPDNoOtherHits",  #HPDNoOtherHits
    "MaxZeros",        #MaxZeros
    "MinE2E10",        #MinE2E10
    "MaxE2E10",        #MaxE2E10
    "LeadingJetEta",   #LeadingJetEta
    "LeadingJetPhi",   #LeadingJetPhi
    "LeadingJetPt",    #LeadingJetPt
    "LeadingJetHad",   #LeadingJetHad
    "LeadingJetEM",    #LeadingJetEM
    "FollowingJetEta", #FollowingJetEta
    "FollowingJetPhi", #FollowingJetPhi
    "FollowingJetPt",  #FollowingJetPt
    "FollowingJetHad", #FollowingJetHad
    "FollowingJetEM",  #FollowingJetEM
    "JetCount20",      #JetCount20
    "JetCount30",      #JetCount30
    "JetCount50",      #JetCount50
    "JetCount100",     #JetCount100
    "HOMaxEnergyRing0",          #HOMaxEnergyRing0
    "HOSecondMaxEnergyRing0",    #HOSecondMaxEnergyRing0
    "HOMaxEnergyIDRing0",        #HOMaxEnergyIDRing0
    "HOSecondMaxEnergyIDRing0",  #HOSecondMaxEnergyIDRing0
    "HOHitCount100Ring0",        #HOHitCount100Ring0
    "HOHitCount150Ring0",        #HOHitCount150Ring0
    "HOMaxEnergyRing12",         #HOMaxEnergyRing12
    "HOSecondMaxEnergyRing12",   #HOSecondMaxEnergyRing12
    "HOMaxEnergyIDRing12",       #HOMaxEnergyIDRing12
    "HOSecondMaxEnergyIDRing12", #HOSecondMaxEnergyIDRing12
    "HOHitCount100Ring12",       #HOHitCount100Ring12
    "HOHitCount150Ring12",       #HOHitCount150Ring12
    "OfficialDecision",          #OfficialDecision
    }

#analysisTree.Draw("HPDHits:HPDNoOtherHits","","colz")
#raw_input("Press Enter to continue...")
#analysisTree.Draw("HPDHits:IEta","","colz")
#raw_input("Press Enter to continue...")
#analysisTree.Draw("HPDNoOtherHits:IEta","","colz")
#raw_input("Press Enter to continue...")
#analysisTree.Draw("HPDHits:RespCorrGain","","colz")
#raw_input("Press Enter to continue...")
#analysisTree.Draw("HPDHits:fCorr","","colz")
#raw_input("Press Enter to continue...")

#analysisTree.Draw("IEta","","")
#raw_input("Press Enter to continue...")
#hcalPlusCanvas  = r.TCanvas("hcalPlusCanvas" ,"hcalPlusCanvas" ,600,400)
#hcalPlusCanvas.cd()
#hcalPlusCanvas.Divide(2,1)
#
#hcalMinusCanvas = r.TCanvas("hcalMinusCanvas","hcalMinusCanvas",600,400)
#hcalMinusCanvas.cd()
#hcalMinusCanvas.Divide(2,1)

hcalCanvas  = r.TCanvas("hcalCanvas" ,"hcalCanvas" ,800,800)
hcalCanvas.cd()
hcalCanvas.Divide(2,2)

plusHistoSlope    = {"en1.5":[],"en3.0":[],"en5.0":[]}
minusHistoSlope   = {"en1.5":[],"en3.0":[],"en5.0":[]}
plusProfileSlope  = {"en1.5":[],"en3.0":[],"en5.0":[]}
minusProfileSlope = {"en1.5":[],"en3.0":[],"en5.0":[]}
plusHistoSlopeErr    = {"en1.5":[],"en3.0":[],"en5.0":[]}
minusHistoSlopeErr   = {"en1.5":[],"en3.0":[],"en5.0":[]}
plusProfileSlopeErr  = {"en1.5":[],"en3.0":[],"en5.0":[]}
minusProfileSlopeErr = {"en1.5":[],"en3.0":[],"en5.0":[]}
for energyCut in [1.5,3.0,5.0]:
    for ieta in range(1,30):
        
        print ieta,energyCut
        # hcalPlusCanvas.cd(1)
        hcalCanvas.cd(1)
        r.gStyle.SetOptStat(0)
        r.gStyle.SetOptFit(1111)
        plusHisto = r.TH2D("plusHisto","plusHisto_iEta%d_cut%2.1f"%(ieta,energyCut),50,-0.5,49.5,20,-0.5,19.5)
        analysisTree.Draw("HPDHits:NumberOfGoodPrimaryVertices>>plusHisto","IEta==%d&&Energy>%f"%(ieta,energyCut),"colz")
        
        plusFit   = r.TF1("plusFit","pol1",3,39)
        plusHisto.Fit(plusFit,"REMF")
        plusHisto.Draw("colz")
        plusHistoSlope["en%2.1f"%(energyCut)].append(plusFit.GetParameter(1))
        plusHistoSlopeErr["en%2.1f"%(energyCut)].append(plusFit.GetParError(1))
        
        # hcalPlusCanvas.cd(2)
        hcalCanvas.cd(2)
        r.gStyle.SetOptStat(0)
        r.gStyle.SetOptFit(1111)
        plusProfile    = plusHisto.ProfileX("plusProfile_iEta%d_cut%2.1f"%(ieta,energyCut));
        plusProfile.SetMaximum(20)
        plusProfileFit = r.TF1("plusProfileFit","pol1",3,39)
        plusProfile.Fit(plusProfileFit,"REMF")
        plusProfileSlope["en%2.1f"%(energyCut)].append(plusProfileFit.GetParameter(1))
        plusProfileSlopeErr["en%2.1f"%(energyCut)].append(plusProfileFit.GetParError(1))
        
        # hcalMinusCanvas.cd(1)
        hcalCanvas.cd(3)
        r.gStyle.SetOptStat(0)
        r.gStyle.SetOptFit(1111)
        minusHisto = r.TH2D("minusHisto","minusHisto_iEta%d_cut%2.1f"%(ieta,energyCut),50,-0.5,49.5,20,-0.5,19.5)
        analysisTree.Draw("HPDHits:NumberOfGoodPrimaryVertices>>minusHisto","IEta==-%d&&Energy>%f"%(ieta,energyCut),"colz")
        
        minusFit   = r.TF1("minusFit","pol1",3,39)
        minusHisto.Fit(minusFit,"REMF")
        minusHisto.Draw("colz")
        minusHistoSlope["en%2.1f"%(energyCut)].append(minusFit.GetParameter(1))
        minusHistoSlopeErr["en%2.1f"%(energyCut)].append(minusFit.GetParError(1))
        
        # hcalMinusCanvas.cd(2)
        hcalCanvas.cd(4)
        r.gStyle.SetOptStat(0)
        r.gStyle.SetOptFit(1111)
        minusProfile    = minusHisto.ProfileX("minusProfile_iEta%d_cut%2.1f"%(ieta,energyCut));
        minusProfile.SetMaximum(20)
        minusProfileFit = r.TF1("minusProfileFit","pol1",3,39)
        minusProfile.Fit(minusProfileFit,"REMF")
        minusProfileSlope["en%2.1f"%(energyCut)].append(minusProfileFit.GetParameter(1))
        minusProfileSlopeErr["en%2.1f"%(energyCut)].append(minusProfileFit.GetParError(1))
        
        hcalCanvas.SaveAs("~/public/html/HCAL/NoiseStudies/hpdHits_vs_nVtx_iEta%d_cut%2.1f.png"%(ieta,energyCut))
        hcalCanvas.SaveAs("~/public/html/HCAL/NoiseStudies/hpdHits_vs_nVtx_iEta%d_cut%2.1f.pdf"%(ieta,energyCut))
        # raw_input("Press Enter to continue...")
        
        plusHisto.Delete()
        plusProfile.Delete()
        minusHisto.Delete()
        minusProfile.Delete()
        
print "plusHistoSlope    = ",plusHistoSlope   
print "plusProfileSlope  = ",plusProfileSlope 
print "minusHistoSlope   = ",minusHistoSlope  
print "minusProfileSlope = ",minusProfileSlope

print "plusHistoSlopeErr    = ",plusHistoSlopeErr   
print "plusProfileSlopeErr  = ",plusProfileSlopeErr 
print "minusHistoSlopeErr   = ",minusHistoSlopeErr  
print "minusProfileSlopeErr = ",minusProfileSlopeErr

#raw_input("Press Enter to exit")
