This is a small collection of scripts to analyze rechits and compute some information
about the hit occupancy.  Scripts, as they are currently written, should be run on
lxplus, as the source root files made by Yi Chen are on the eos filesystem at CERN.
Once the output of smallAnalyzer.py is done, you can migrate the output files and
source code to any other machine and finish running the code there.


smallAnalyzer.py:
    reads in the ntuples created by Yi Chen and outputs histograms (1D and 2D)
    of various distributions related to HPD occupancy, rechit occupancy
    as a function of NPV, eta, HPD channel name, gemoetry
    histograms are done for various hit energy threshold levels (no explicit cut, > 1.5 GeV,
    > 3.0 GeV, > 5.0 GeV, < 1.5 GeV, 1.5 GeV < hit < 3.0 GeV, 3.0 GeV < hit < 5.0 GeV)

submission.py:
    driver file for smallAnalyzer.py, submits to the batch queue (lxbatch with bsub)

makeProbabilityDistributions.py:
    reads in the output of smallAnalyzer and creates probability distributions for the
    different channels

makeProbabilityDists.py:
    driver file for the makeProbabilityDistributions.py script

runPredictions.py:
    runs the full prediction code, using the probability distributions from makeProbabilityDistributions.py
    and the histograms from smallAnalyzer.py.
    Currently the prediction is based on a linear extrapolation of the probability as a function
    of nVtx.  This can be modified to take into account different models, including adding results
    from different nVtx bins to get a prediction on the sum, but this has not yet been implemented

submitPredictions.py:
    driver file for the runPredictions.py script

createOutput.sh:
    hadds the output of the runPredictions.py jobs together

rootGarbageCollection.py:
  wraps some of the ROOT objects into garbage collected items that prevent some
  crashes.

Other extraneous scripts
quickPlotter.py:

makeSimpleCanvas.py:

files.py:

etaHistograms.py:

compareEnergyDistributions.py:

anyPlotter.py:

