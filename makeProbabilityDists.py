import sys,os
samples = ["MultiJet","SingleMu","MET","HTMHT"]#,"HcalHPDNoise"]
for sample in samples:
    for fitRange in [5,10,15,20,25,30,40,50]:
        cmd = "python makeProbabilityDistributions.py -r %d -s %s"%(fitRange,sample)
        
        print cmd
        os.system(cmd)
