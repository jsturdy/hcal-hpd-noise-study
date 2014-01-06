import datetime
import sys,os,errno
from files import noiseFiles

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
################

samples = ["SingleMu","MultiJet"]#,"MET","HTMHT"]#,"HcalHPDNoise"]
#samples = ["MultiJet"]#,"MET","HTMHT"]#,"HcalHPDNoise"]
nentries = 1000000
myDay = datetime.date.today()
for sample in samples:
    print sample,nentries
    #mkdir_p("%s/%s"%(myDay,sample))
    #for nVtx in range(0,50):
    #for nVtx in range(50,100):
    for nVtx in range(100,150):
        for run in range(20):
            mkdir_p("%s_V%d"%(myDay,run))
            cmd = "python runPredictions.py -r 40 -v %d -s %s -n %d -j %d > & %s_V%d/%s_prediction_job%d_%d.out"%(nVtx,
                  sample,
                  nentries,
                  run,
                  myDay,
                  run,
                  sample,
                  nVtx,
                  run)
            print cmd
            sys.stdout.flush()
            jobFile = open("%s_prediction_job%d_%d.csh"%(sample,nVtx,run),'w')
            jobFile.write("""#!/bin/csh
cd /afs/cern.ch/work/s/sturdy/public/CMSSW_6_2_0_patch1/src/
cmsenv
%s\n"""%(cmd))
            jobFile.close()
        
            cmd = "chmod 755 %s_prediction_job%d_%d.csh"%(sample,nVtx,run)
            print cmd
            sys.stdout.flush()
            os.system(cmd)
            
            cmd = "bsub -q 8nh -J %s_prediction_job%d_%d < %s_prediction_job%d_%d.csh"%(sample,nVtx,run,sample,nVtx,run)
            print cmd
            sys.stdout.flush()
            os.system(cmd)
        
