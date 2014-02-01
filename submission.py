import sys,os
from files import noiseFiles
#jobName = "singlemu"
#jobName = "hpdnoise"
#jobName = "met"
jobName = "htmht"
#jobName = "multijet"

filesPerJob = 3
fileList = noiseFiles[jobName]["files"]
totalFiles = len(fileList)
numJobs = totalFiles/filesPerJob
moduloIs = totalFiles%filesPerJob
if moduloIs > 0:
    numJobs = numJobs + 1
print jobName,totalFiles,filesPerJob,numJobs,moduloIs
for i in range(numJobs):
    jobNum = i + 1
    filesList = ""
    for j in range(filesPerJob):
        if j == 0:
            filesList = "%s"%(fileList[i*filesPerJob+j])
        elif i*filesPerJob+j<totalFiles:
            filesList = "%s,%s"%(filesList,fileList[i*filesPerJob+j])
    print filesList
    cmd = "python smallAnalyzer.py -o hpdInformation_job%d -j %s -f %s > & %s_job%d.out"%(jobNum,
                                                                                          noiseFiles[jobName]["dir"],
                                                                                          filesList,
                                                                                          jobName,jobNum)
    print cmd
    jobFile = open("%s_job%d.csh"%(jobName,jobNum),'w')
    jobFile.write("""#!/bin/csh
cd /afs/cern.ch/work/s/sturdy/public/CMSSW_6_2_0_patch1/src/
cmsenv
%s\n"""%(cmd))
    jobFile.close()

    cmd = "chmod 755 %s_job%d.csh"%(jobName,jobNum)
    print cmd
    os.system(cmd)

    cmd = "bsub -q 8nh -J %s_job%d < %s_job%d.csh"%(jobName,jobNum,jobName,jobNum)
    print cmd
    os.system(cmd)

##python smallAnalyzer_v2.py -o secondGroup.root -l 10 -u 20 > & 10to19.out &
##python smallAnalyzer_v2.py -o thirdGroup.root -l 20 -u 30 > & 20to29.out &
##python smallAnalyzer_v2.py -o tenthGroup.root -l 90 -u 100 > & 90to99.out &
