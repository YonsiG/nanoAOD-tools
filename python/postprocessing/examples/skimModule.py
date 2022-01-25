from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

ROOT.gROOT.SetBatch(True)

import os
base = os.getenv("CMSSW_BASE")

class vbsHwwSkimProducer_hadronic(Module):
    def __init__(self):
        print("Loading NanoCORE shared libraries...")
        if (os.path.isfile(base+"/src/PhysicsTools/NanoAODTools/NanoTools/NanoCORE/libNANO_CORE.so")):
          ROOT.gSystem.Load(base+"/src/PhysicsTools/NanoAODTools/NanoTools/NanoCORE/libNANO_CORE.so")
          header_files = ["ElectronSelections", "MuonSelections", "TauSelections", "Config"]
          for header_file in header_files:
            print("Loading NanoCORE {} header file...".format(header_file))
            ROOT.gROOT.ProcessLine(".L "+base+"/src/PhysicsTools/NanoAODTools/NanoTools/NanoCORE/{}.h".format(header_file))
        else:
          ROOT.gSystem.Load(base+"/libNANO_CORE.so")
          header_files = ["ElectronSelections", "MuonSelections", "TauSelections", "Config"]
          for header_file in header_files:
            print("Loading NanoCORE {} header file...".format(header_file))
            ROOT.gROOT.ProcessLine(".L "+base+"/{}.h".format(header_file))


    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self._tchain = ROOT.TChain("Events")
        self._tchain.Add(inputFile.GetName())
        print(inputFile)
        if "UL16" in inputFile.GetName():
            ROOT.gconf.nanoAOD_ver = 8
        if "UL17" in inputFile.GetName():
            ROOT.gconf.nanoAOD_ver = 8
        if "UL18" in inputFile.GetName():
            ROOT.gconf.nanoAOD_ver = 8
        ROOT.nt.Init(self._tchain)
        ROOT.gconf.GetConfigs(ROOT.nt.year())
        print("year = {}".format(ROOT.nt.year()))
        print("WP_DeepFlav_loose = {}".format(ROOT.gconf.WP_DeepFlav_loose))
        print("WP_DeepFlav_medium = {}".format(ROOT.gconf.WP_DeepFlav_medium))
        print("WP_DeepFlav_tight = {}".format(ROOT.gconf.WP_DeepFlav_tight))
        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        # print(event._entry)
        ROOT.nt.GetEntry(event._entry)
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        fatjets = Collection(event, "FatJet")

 

        charges_veto = []
        leptons_veto = []
        leptons_veto_jetIdx = []
        fjets = []

        # Loop over the muons to select the leptons
        nmuons_veto = 0
        for i, lep in enumerate(muons):

          # Check that it passes veto Id
          if ROOT.ttH.muonID(i, ROOT.ttH.IDveto, ROOT.nt.year()):
              nmuons_veto += 1
              charges_veto.append(lep.charge)
              leptons_veto.append(ROOT.nt.Muon_p4()[i])
              leptons_veto_jetIdx.append(ROOT.nt.Muon_jetIdx()[i])


        # Loop over the electrons
        nelectrons_veto = 0
        for i, lep in enumerate(electrons):

            # check that if passes loose
            if ROOT.ttH.electronID(i, ROOT.ttH.IDveto, ROOT.nt.year()):
                nelectrons_veto += 1
                charges_veto.append(lep.charge)
                leptons_veto.append(ROOT.nt.Electron_p4()[i])
                leptons_veto_jetIdx.append(ROOT.nt.Electron_jetIdx()[i])

        #if not (nelectrons_veto + nmuons_veto >= 1): print "lepton veto failed" # First check that we have at least one light lepton
        
        nfatjets=0
        
        # Loop over the fatjets (they have priority over jets)
        for i, fjet in enumerate(fatjets):

            isOverlap = False
            # Perform lepton - jet overlap removal
            #for lep in leptons_veto:
            #    if ROOT.Math.VectorUtil.DeltaR(ROOT.nt.FatJet_p4()[i], lep) < 0.4:
            #        isOverlap = True
            #        break

            if isOverlap:
                continue

            # Count jets with pt > 20
            if fjet.pt >= 250 and fjet.msoftdrop>=40 and abs(fjet.eta)<=2.5 and fjet.jetId>0:
                nfatjets += 1
                fjets.append(ROOT.nt.FatJet_p4()[i])



        njets_VBF=0
        njets_central=0
        
        indicesVBF=[]

        for i, jet in enumerate(jets):

            # Perform lepton - jet overlap removal
            isOverlap = False
            #for ilep_jetidx in leptons_veto_jetIdx:
            #    if i == ilep_jetidx:
            #        isOverlap = True
            #        break

            # Perform lepton - jet overlap removal
            for fjet in fjets:
                if ROOT.Math.VectorUtil.DeltaR(ROOT.nt.Jet_p4()[i], fjet) < 0.8:
                    isOverlap = True
                    break

            if isOverlap:
                continue

            # Count jets with pt > 20
            if jet.pt > 25 and abs(jet.eta)<4.7:
                njets_VBF += 1
                indicesVBF.append(i)

            # Count jets with pt > 30
            if jet.pt > 30 and abs(jet.eta)<2.5:
                njets_central += 1
        
                
        mjj_mjj_max=-1
        deta_mjj_max=-1
        
        mjj_deta_max=-1
        deta_deta_max=-1
        
        mjj_method3=-1
        deta_method3=-1
        
        o,p=-1,-1
        for index1 in indicesVBF:
            for index2 in indicesVBF:
              if (index1==index2): 
                continue
              mjj=(ROOT.nt.Jet_p4()[index1]+ROOT.nt.Jet_p4()[index2]).M()
              deta=abs(jets[index1].eta-jets[index2].eta)
              
              if mjj>mjj_mjj_max:
                mjj_mjj_max=mjj
                deta_mjj_max=deta
                o=index1
                p=index2
              
              if (deta>deta_deta_max):
                deta_deta_max=deta
                mjj_deta_max=mjj
        
        #method3
        Emax=-1
        Imax=-1                      
        Imax2=-1
        Emax2=-1
        
        for index1 in indicesVBF:
            if(ROOT.nt.Jet_p4()[index1].E()>Emax):
              Emax=ROOT.nt.Jet_p4()[index1].E()
              Imax=index1

        for index1 in indicesVBF:
            if (index1==Imax): 
              continue
            if(jets[index1].eta*jets[Imax].eta<0):
              if(ROOT.nt.Jet_p4()[index1].E()>Emax2):
                Emax2=ROOT.nt.Jet_p4()[index1].E()
                Imax2=index1
                
        if(Imax>0 and Imax2>0):
          mjj_method3=(ROOT.nt.Jet_p4()[Imax]+ROOT.nt.Jet_p4()[Imax2]).M()
          deta_method3=abs(jets[Imax].eta-jets[Imax2].eta)
        else:
          mjj_method3=mjj_deta_max
          deta_method3=deta_deta_max
          
        #end of method 3
        
        VBF1=(mjj_mjj_max>500 and deta_mjj_max>3.0)
        VBF2=(mjj_deta_max>500 and deta_deta_max>3.0)
        VBF3=(mjj_method3>500 and deta_method3>3.0)
        VBF_OR = (VBF1 or VBF2 or VBF3)

        '''passo=True
        if (nelectrons_veto + nmuons_veto >= 1):
          passo=False
        if (nfatjets<1):
          passo=False
        if (nfatjets==1 and not VBF_OR):
         passo=False
        if (nfatjets==2 and not VBF_OR):
         passo=False
        if (nfatjets>=3 and njets_VBF==0):
         passo=False
        passo=int(passo)'''    
        #print "event number: %s pass or not: %s nleptons: %s njets: %s nfatjets: %s VBF max mass: %s VBF max deltaEta: %s" %(event._entry, passo, nelectrons_veto + nmuons_veto, njets_VBF, nfatjets, mjj_method3, deta_method3)
        #print "event number: %s pass or not: %s nleptons: %s njets: %s nfatjets: %s VBF max mass: %s VBF max deltaEta: %s" %(event._entry, passo, nelectrons_veto + nmuons_veto, njets_VBF, nfatjets, mjj_mjj_max, deta_mjj_max)
        #print "event number: %s pass or not: %s nleptons: %s njets: %s nfatjets: %s VBF max mass: %s VBF max deltaEta: %s" %(event._entry, passo, nelectrons_veto + nmuons_veto, njets_VBF, nfatjets, mjj_deta_max, deta_deta_max)  
        #for index1 in indicesVBF: 
        #    f1=int((index1==o) or (index1==p))
        #    print "VBF Jet flag: %s Jet_mass: %s Jet_Pt:%s Jet_Eta:%s Jet_Phi: %s" %( f1, jets[index1].mass, jets[index1].pt, jets[index1].eta, jets[index1].phi )              
 
        if (nelectrons_veto + nmuons_veto >= 1):
          return False
        if (nfatjets<1):
          return False
        if (nfatjets==1 and not VBF_OR):
          return False
        if (nfatjets==2 and not VBF_OR):
          return False
        if (nfatjets>=3 and njets_VBF==0):
          return False
        
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

vbsHwwSkimModuleConstr = lambda: vbsHwwSkimProducer_hadronic()
 

