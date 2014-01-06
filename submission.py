import sys,os
#bounds = [1,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
bounds = [(x)*2+1 for x in range(50)]
print bounds
for i in range(len(bounds)-1):

    cmd = "python smallAnalyzer.py -o %dto%d.root -l %d -u %d > & %dto%d.out"%(bounds[i],bounds[i+1]-1,
                                                                               bounds[i],bounds[i+1],
                                                                               bounds[i],bounds[i+1]-1
                                                                               )
    jobFile = open("./job%d.csh"%(i+1),'w')
    jobFile.write("""#!/bin/csh
cd /afs/cern.ch/work/s/sturdy/public/CMSSW_6_2_0_patch1/src
cmsenv
%s"""%(cmd))
    cmd = "chmod 744 job%d.csh"%(i+1)
    print cmd
    os.system(cmd)

    cmd = "bsub -q 1nh -J job%d < job%d.csh"%(i+1,i+1)
    print cmd
    #os.system(cmd)

##python smallAnalyzer.py -o secondGroup.root -l 10 -u 20 > & 10to19.out &
##python smallAnalyzer.py -o thirdGroup.root -l 20 -u 30 > & 20to29.out &
##python smallAnalyzer.py -o tenthGroup.root -l 90 -u 100 > & 90to99.out &
