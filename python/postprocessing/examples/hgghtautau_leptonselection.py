import ROOT
import array
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Object 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

class HHggtautauLepSelector(Module):
    def __init__(self, jetSelection, muSelection, eSelection, data, year="2016"):
        self.jetSel = jetSelection
        self.muSel = muSelection
        self.eSel = eSelection
        self.data = data
        self.year = year
        
        ### ref link useful later on
        ### reduced JES uncertainties (see https://twiki.cern.ch/twiki/bin/viewauth/CMS/JECUncertaintySources#Run_2_reduced_set_of_uncertainty)
       
    def beginJob(self):
        pass
    
    def endJob(self):
        pass
    
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        
        self.out = wrappedOutputTree
        self.out.branch("Category",   "I");
        self.out.branch("Category_lveto",   "I");
        self.out.branch("eleHidx","I", 2);
        self.out.branch("muHidx","I", 2);
        self.out.branch("Jet_Filter",  "O", 1, "nJet");
        self.out.branch("Tau_Filter",  "O", 1, "nTau");
        
        self.out.branch("nselectedMuon",   "I");
        self.out.branch("nselectedElectron",   "I");

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass       
    
    def elid(self, el, wp, noiso=False):
        if (wp == "80"):
            return el.mvaFall17V2Iso_WP80
        elif (wp == "90"):
            return el.mvaFall17V2Iso_WP90
        elif (wp == "80" and noiso==True):
            return el.mvaFall17V2noIso_WP80
        elif (wp == "90" and noiso==True):
            return el.mvaFall17V2noIso_WP90
        
    def analyze(self, event):

        electrons = list(Collection(event, "Electron"))
        muons = list(Collection(event, "Muon"))
        jets = list(Collection(event, "Jet"))        
        photons = list(Collection(event, "Photon"))
        taus = list(Collection(event, "Tau"))
        gHidx = getattr(event, "gHidx")
        ggMass = getattr(event, "gg_mass")        
        
        Category = -1
        Category_lveto = -1
        eleHidx=[-1,-1]
        muHidx=[-1,-1]
        nSelElectrons=0
        nSelMuons=0
       
        
        # adding these criteria to cross clean only from the gg Pair
        # I just reset the gHidx in cas
        # Can be removed
        if gHidx[0]>=0:
          if not (photons[gHidx[0]].mvaID > -0.7 and  photons[gHidx[0]].pt/ggMass > 0.33):
            gHidx[0]=-1
        if gHidx[1]>=0:
          if not (photons[gHidx[1]].mvaID > -0.7 and  photons[gHidx[1]].pt/ggMass > 0.25):
            gHidx[1]=-1

        #cross cleaning of leptons
        hphotonFilter = lambda j : ((deltaR(j,photons[gHidx[0]])>0.2 if gHidx[0]>=0 else 1) and (deltaR(j,photons[gHidx[1]])>0.2 if gHidx[1]>=0 else 1))
        
        #cross cleaning of jets
        hphotonFilter4 = lambda j : ((deltaR(j,photons[gHidx[0]])>0.4 if gHidx[0]>=0 else 1) and (deltaR(j,photons[gHidx[1]])>0.4 if gHidx[1]>=0 else 1))

        #leptons selection
        lElectrons = [x for x in electrons if x.pt > 10 and (self.elid(x,"90") or (x.pfRelIso03_all < 0.3 and self.elid(x,"90", True)))  and abs(x.dxy) < 0.045 and abs(x.dz) < 0.2 and abs(x.eta)<2.5 and hphotonFilter(x) ] #electron ecal cracks?
        lMuons = [x for x in muons if x.pt > 10 and x.pfRelIso03_all < 0.3 and abs(x.dxy) < 0.045 and abs(x.dz) < 0.2 and abs(x.eta)<2.4 and hphotonFilter(x) ] #pfRelIso03_all or pfRelIso04_all ??
        
        ##bbtautau tight used to be (left as comment)
        #tElectrons = [x for x in electrons if self.elid(x,"80") and x.pt > 25 and abs(x.dxy) < 0.045 and abs(x.dz) < 0.2 and abs(x.eta)<2.5 and hphotonFilter(x)]        
        #tMuons = [x for x in muons if x.pt > 20 and x.tightId >= 1 and x.pfRelIso04_all < 0.15 and abs(x.dxy) < 0.045 and abs(x.dz) < 0.2 and abs(x.eta)<2.4 and hphotonFilter(x)]      
        
        nSelElectrons=len(lElectrons)
        nSelMuons=len(lMuons)
 
        # these should be use for jet counting and for the taus they are applied before the tau selection
        jetFilterFlags = [True]*len(jets)
        tauFilterFlags = [True]*len(taus)
    
        for i in range(len(jets)):
            #selected pho cross cleaning
            if (hphotonFilter4(jets[i])==0):
                jetFilterFlags[i]=False
                
        #sel lep cross celaning for jets        
        for lepton in lElectrons+lMuons:
            jetInd = lepton.jetIdx
            if jetInd >= 0:
                jetFilterFlags[jetInd] = False
                
        for i in range(len(taus)):
            #selected pho cross cleaning
            if (hphotonFilter(taus[i])==0):
              tauFilterFlags[i]=False
            #selected lep cross cleaning
            for lepton in lElectrons+lMuons:
              if deltaR(lepton, taus[i])<0.2:
                tauFilterFlags[i]=False
       
        #dilepton categories first
        # done here as taus are not needed
        # priority order
        # 1. mumu - 2. emu - 3. ee
        for i in range(len(lMuons)):
          for j in range(i+1,len(lMuons)):
            if (lMuons[i].charge*lMuons[j].charge==-1):
              Category=4 
          for j in range(0,len(lElectrons)):
            if (lMuons[i].charge*lElectrons[j].charge==-1):
              Category=6
    
        for i in range(len(lElectrons)):
          for j in range(i+1,len(lElectrons)):
            if (lElectrons[i].charge*lElectrons[j].charge==-1):
              Category=5

        if Category<0:  # i.e. no opposite sgn lepton pairs were found
            if (len(lMuons)==1):
                Category=1
            elif (len(lElectrons)==1):
                Category=2
            elif(len(lMuons+lElectrons)==0):
                Category=3

        #leptons vetos
        # almost a repetition, but excludes extra leptons of the same sign
        if (Category==1 and len(lMuons+lElectrons)==1):
            Category_lveto=1
        elif (Category==2 and len(lMuons+lElectrons)==1):
            Category_lveto=2
        elif (Category==3):
            Category_lveto=3
        elif(Category==4 and len(lMuons+lElectrons)==2):
            Category_lveto=4
        elif(Category==5 and len(lMuons+lElectrons)==2):
            Category_lveto=5
        elif(Category==6 and len(lMuons+lElectrons)==2):
            Category_lveto=6

        ### the lepton only categories dont need any tau ID
        ### and once we are here we are sure the pairs are formed in an unique way beacause of pairs+lep veto.
        if (Category_lveto==4):
            muHidx[0]=muons.index(lMuons[0])
            muHidx[1]=muons.index(lMuons[1])
        elif (Category_lveto==5):
            eleHidx[0]=electrons.index(lElectrons[0])
            eleHidx[1]=electrons.index(lElectrons[1])
        elif (Category_lveto==6):
            eleHidx[0]=electrons.index(lElectrons[0])
            muHidx[0]=muons.index(lMuons[0])
            
        #one index is filled when the tau PAIR is lep+had
        elif (Category_lveto==2):
            eleHidx[0]=electrons.index(lElectrons[0])
        elif (Category_lveto==1):
            muHidx[0]=muons.index(lMuons[0])


        self.out.fillBranch("eleHidx",  eleHidx);
        self.out.fillBranch("muHidx",  muHidx);
        self.out.fillBranch("Category",  Category);
        self.out.fillBranch("Category_lveto",  Category_lveto);
        self.out.fillBranch("Jet_Filter",jetFilterFlags)
        self.out.fillBranch("Tau_Filter",tauFilterFlags)
        
        self.out.fillBranch("nselectedElectron",nSelElectrons)
        self.out.fillBranch("nselectedMuon",nSelMuons)
        
        return True



HHggtautaulep2016 = lambda : HHggtautauLepSelector(jetSelection= lambda j : j.pt > 15, muSelection= lambda mu : mu.pt > 9, eSelection= lambda e : e.pt > 9, data = False, year="2016")
HHggtautaulep2017 = lambda : HHggtautauLepSelector(jetSelection= lambda j : j.pt > 15, muSelection= lambda mu : mu.pt > 9, eSelection= lambda e : e.pt > 9, data = False, year="2017")
HHggtautaulep2018 = lambda : HHggtautauLepSelector(jetSelection= lambda j : j.pt > 15, muSelection= lambda mu : mu.pt > 9, eSelection= lambda e : e.pt > 9, data = False, year="2018")

HHggtautaulepDATA18 = lambda : HHggtautauLepSelector(jetSelection= lambda j : j.pt > 15, muSelection= lambda mu : mu.pt > 9, eSelection= lambda e : e.pt > 9, data = True, year="2018")
HHggtautaulepDATA17 = lambda : HHggtautauLepSelector(jetSelection= lambda j : j.pt > 15, muSelection= lambda mu : mu.pt > 9, eSelection= lambda e : e.pt > 9, data = True, year="2017")
HHggtautaulepDATA16 = lambda : HHggtautauLepSelector(jetSelection= lambda j : j.pt > 15, muSelection= lambda mu : mu.pt > 9, eSelection= lambda e : e.pt > 9, data = True, year="2016")





 
