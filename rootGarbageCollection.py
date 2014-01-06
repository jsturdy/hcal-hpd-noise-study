from ROOT import RooFit as roofit
from ROOT import kTRUE,kFALSE
import ROOT as r

# keep a pointer to the original TCanvas constructor
oldtcaninit = r.TCanvas.__init__

# define a new TCanvas class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentTCanvas(r.TCanvas):
    def __init__(self, *args):
        oldtcaninit(self,*args)
        r.SetOwnership(self,False)

# replace the old TCanvas class by the new one
r.TCanvas = GarbageCollectionResistentTCanvas

# keep a pointer to the original TPad constructor
oldtpadinit = r.TPad.__init__

# define a new TPad class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentTPad(r.TPad):
    def __init__(self, *args):
        oldtpadinit(self,*args)
        r.SetOwnership(self,False)

# replace the old TPad class by the new one
r.TPad = GarbageCollectionResistentTPad

# keep a pointer to the original TLine constructor
oldtlineinit = r.TLine.__init__

# define a new TLine class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentTLine(r.TLine):
    def __init__(self, *args):
        oldtlineinit(self,*args)
        r.SetOwnership(self,False)

# replace the old TLine class by the new one
r.TLine = GarbageCollectionResistentTLine

# keep a pointer to the original THStack constructor
oldthstackinit = r.THStack.__init__

# define a new THStack class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentTHStack(r.THStack):
    def __init__(self, *args):
        oldthstackinit(self,*args)
        r.SetOwnership(self,False)

# replace the old THStack class by the new one
r.THStack = GarbageCollectionResistentTHStack

# keep a pointer to the original TH1D constructor
oldth1dinit = r.TH1D.__init__

# define a new TH1D class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentTH1D(r.TH1D):
    def __init__(self, *args):
        oldth1dinit(self,*args)
        r.SetOwnership(self,False)

# replace the old TH1D class by the new one
r.TH1D = GarbageCollectionResistentTH1D

# keep a pointer to the original TH2D constructor
oldth2dinit = r.TH2D.__init__

# define a new TH2D class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentTH2D(r.TH2D):
    def __init__(self, *args):
        oldth2dinit(self,*args)
        r.SetOwnership(self,False)

# replace the old TH2D class by the new one
r.TH2D = GarbageCollectionResistentTH2D

# keep a pointer to the original TProfile constructor
oldtprofileinit = r.TProfile.__init__

# define a new TProfile class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentTProfile(r.TProfile):
    def __init__(self, *args):
        oldtprofileinit(self,*args)
        r.SetOwnership(self,False)

# replace the old TProfile class by the new one
r.TProfile = GarbageCollectionResistentTProfile
