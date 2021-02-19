import ROOT
import array
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Object 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi

import os, math

base = os.getenv("CMSSW_BASE")
arch = os.getenv("SCRAM_ARCH")

ROOT.gROOT.ProcessLine(".L %s/lib/%s/libTauAnalysisSVfitTF.so"%(base, arch))
ROOT.gROOT.ProcessLine(".L %s/lib/%s/libTauAnalysisClassicSVfit.so"%(base, arch))
ROOT.gROOT.ProcessLine(".L %s/src/PhysicsTools/NanoAODTools/python/postprocessing/helpers//SVFitFunc.cc+"%base)


class HHggtautauProducer(Module):
    def __init__(self, jetSelection, muSelection, eSelection, data, year="2016", hadtau1="Loose", hadtau2="Loose"):
        self.jetSel = jetSelection
        self.muSel = muSelection
        self.eSel = eSelection
        self.data = data
        self.year = year
        self.hadtau1 = hadtau1
        self.hadtau2 = hadtau2
        self.postfix = hadtau1+(hadtau2 if hadtau1!=hadtau2 else "")
        
        ### ref link useful later on
        ### reduced JES uncertainties (see https://twiki.cern.ch/twiki/bin/viewauth/CMS/JECUncertaintySources#Run_2_reduced_set_of_uncertainty)
       
    def beginJob(self):
        print "OVO"
        pass
    
    def endJob(self):
        pass
    
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        
        self.out = wrappedOutputTree
                
        self.out.branch("pt_tautau"+self.postfix,  "F");   
        self.out.branch("eta_tautau"+self.postfix,  "F"); 
        self.out.branch("phi_tautau"+self.postfix,  "F"); 
        self.out.branch("m_tautau"+self.postfix,  "F"); 
        self.out.branch("dR_tautau"+self.postfix,  "F");
        
        self.out.branch("pt_tautauSVFit"+self.postfix,  "F");   
        self.out.branch("eta_tautauSVFit"+self.postfix,  "F"); 
        self.out.branch("phi_tautauSVFit"+self.postfix,  "F"); 
        self.out.branch("m_tautauSVFit"+self.postfix,  "F"); 
        self.out.branch("dR_tautauSVFit"+self.postfix,  "F");
        
        self.out.branch("dR_ggtautau"+self.postfix,  "F");
        self.out.branch("dPhi_ggtautau"+self.postfix,  "F");
        self.out.branch("dR_ggtautauSVFit"+self.postfix,  "F");
        self.out.branch("dPhi_ggtautauSVFit"+self.postfix,  "F");
        
        self.out.branch("nselectedTau"+self.postfix, "I")
        
        self.out.branch("selectedTau"+self.postfix+"_ptSVFit",  "F", 2);   
        self.out.branch("selectedTau"+self.postfix+"_etaSVFit",  "F", 2); 
        self.out.branch("selectedTau"+self.postfix+"_phiSVFit",  "F", 2); 
        self.out.branch("selectedTau"+self.postfix+"_mSVFit",  "F", 2);
        
        self.out.branch("selectedMuon_ptSVFit",  "F", 2);   
        self.out.branch("selectedMuon_etaSVFit",  "F", 2); 
        self.out.branch("selectedMuon_phiSVFit",  "F", 2); 
        self.out.branch("selectedMuon_mSVFit",  "F", 2); 
        
        self.out.branch("selectedElectron_ptSVFit",  "F", 2);   
        self.out.branch("selectedElectron_etaSVFit",  "F", 2); 
        self.out.branch("selectedElectron_phiSVFit",  "F", 2); 
        self.out.branch("selectedElectron_mSVFit",  "F", 2); 
        
        self.out.branch("tauHidx"+self.postfix,  "I", 2);
        self.out.branch("Category_tausel"+self.postfix,   "I");
        self.out.branch("Category_pairs"+self.postfix,   "I");
        
        self.out.branch("Jet_Filter"+self.postfix,  "O", 1, "nJet"); 

        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def invMass(self, obj1, obj2, mass1=-1, mass2=-1):
        j1 = ROOT.TLorentzVector()
        j2 = ROOT.TLorentzVector()
        if (mass1==-1):
            j1.SetPtEtaPhiM(obj1.pt, obj1.eta, obj1.phi, obj1.mass)
        else:
            j1.SetPtEtaPhiM(obj1.pt, obj1.eta, obj1.phi, mass1)
        if (mass2==-1):
            j2.SetPtEtaPhiM(obj2.pt, obj2.eta, obj2.phi, obj2.mass)
        else:
            j2.SetPtEtaPhiM(obj2.pt, obj2.eta, obj2.phi, mass2)        
        return (j1+j2).M() 
      
    def PtEtaPhi(self, obj1, obj2, mass1=-1, mass2=-1):
        j1 = ROOT.TLorentzVector()
        j2 = ROOT.TLorentzVector()
        if (mass1==-1):
            j1.SetPtEtaPhiM(obj1.pt, obj1.eta, obj1.phi, obj1.mass)
        else:
            j1.SetPtEtaPhiM(obj1.pt, obj1.eta, obj1.phi, mass1)
        if (mass2==-1):
            j2.SetPtEtaPhiM(obj2.pt, obj2.eta, obj2.phi, obj2.mass)
        else:
            j2.SetPtEtaPhiM(obj2.pt, obj2.eta, obj2.phi, mass2)        
        return (j1+j2).Pt(),(j1+j2).Eta(),(j1+j2).Phi()  
   
    def analyze(self, event):
        
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        electrons = list(Collection(event, "Electron"))
        muons = list(Collection(event, "Muon"))
        jets = list(Collection(event, "Jet"))        
        taus = list(Collection(event, "Tau"))
        photons = list(Collection(event, "Photon"))
        MET = Object(event, "MET")
        
        gHidx = getattr(event, "gHidx")
        ggEta = getattr(event, "gg_eta")   
        ggPhi = getattr(event, "gg_phi")   
        
        eleHidx = getattr(event, "eleHidx")
        muHidx = getattr(event, "muHidx")
        tauHidx = [-1,-1]
        globtauHidx = [-1,-1]
        
        Category_lveto = getattr(event, "Category_lveto")
        jetlepFilterFlags = getattr(event, "Jet_Filter")
        
        tautauMass=tautauPt=tautauPhi=tautauEta=-1  
        tautaudR=-1
        
        Category_tausel = -1
        Category_pairs = -1
        
        selectedMuon_ptSVFit     = selectedMuon_etaSVFit     = selectedMuon_phiSVFit     = selectedMuon_mSVFit     = [-1,-1]         
        selectedElectron_ptSVFit = selectedElectron_etaSVFit = selectedElectron_phiSVFit = selectedElectron_mSVFit = [-1,-1] 
        selectedTau_ptSVFit      = selectedTau_etaSVFit      = selectedTau_phiSVFit      = selectedTau_mSVFit      = [-1,-1] 
                        
        tautauMassSVFit = tautauPtSVFit = tautauEtaSVFit = tautauPhiSVFit = tautaudRSVFit=-1
        
        ggtautaudR = ggtautaudPhi = ggtautaudRSVFit = ggtautaudPhiSVFit = -1
        
        jetFilterFlags = jetlepFilterFlags # adding tau filter on top

        deepTauId_vsJet={"Medium":16, "Loose":8, "VLoose":4, "VVLoose":2, "VVVLoose":1}
        tausForHiggs = [x for x in taus if (x.pt>20 and 
                                            abs(x.eta)<2.3  and 
                                            x.idDecayModeNewDMs and 
                                            x.idDeepTau2017v2p1VSe>=2 and #VVLoose
                                            (x.idDeepTau2017v2p1VSjet>=deepTauId_vsJet[self.hadtau1] or x.idDeepTau2017v2p1VSjet>=deepTauId_vsJet[self.hadtau2]) and #choosing the WP for both tau
                                            x.idDeepTau2017v2p1VSmu>=1 and #VLoose
                                            abs(x.dz) < 0.2 and 
                                            x.Filter # using this filter which contains leptons and photns form previous modules
                                            )]

        ##reminder in comment 
        ##bbtautau has different WP depending on the lep category
        ### tau+mu x.idDeepTau2017v2p1VSe>=4, x.idDeepTau2017v2p1VSmu>=8
        ### tau+mu x.idDeepTau2017v2p1VSe>=32, x.idDeepTau2017v2p1VSmu>=8
        ### tau+tau x.idDeepTau2017v2p1VSe>=2, x.idDeepTau2017v2p1VSmu>=1
        # idDeepTau2017v2p1VSjet medium everywhere, but we change it        
            
        nSelTaus = len(tausForHiggs)
        
        # one tau index
        if (Category_lveto==3 and len(tausForHiggs)>0):
          for tauCand in tausForHiggs:
                if (tauCand.idDeepTau2017v2p1VSjet>=deepTauId_vsJet[self.hadtau1]):
                    tauHidx[0] = taus.index(tauCand)
                    break

        if (Category_lveto==1 and len(tausForHiggs)>0):
            Category_tausel=1
        elif (Category_lveto==2 and len(tausForHiggs)>0):
            Category_tausel=2
        elif (Category_lveto==3 and len(tausForHiggs)>1):
            Category_tausel=3

        if (Category_tausel==1 and len(tausForHiggs)):
            charge = muons[muHidx[0]].charge
            for j in range(len(tausForHiggs)):
                if (charge*tausForHiggs[j].charge==-1):
                    tauHidx[0] = taus.index(tausForHiggs[j])
                    
        elif (Category_tausel==2 and len(tausForHiggs)):
            charge = electrons[eleHidx[0]].charge
            for j in range(len(tausForHiggs)):
                if (charge*tausForHiggs[j].charge==-1):
                    tauHidx[0] = taus.index(tausForHiggs[j])
        
        elif (Category_tausel==3):
            charge=0
            for tauCand in tausForHiggs:
                if (tauCand.idDeepTau2017v2p1VSjet>=deepTauId_vsJet[self.hadtau1]):
                    tauHidx[0] = taus.index(tauCand)
                    charge=tauCand.charge
                    break
            if (charge!=0):
                for tauCand in tausForHiggs:
                    if (charge*tauCand.charge==-1 and tauCand.idDeepTau2017v2p1VSjet>=deepTauId_vsJet[self.hadtau2]):
                        tauHidx[1] = taus.index(tauCand)
        
        #global index sorting
        if (Category_tausel==1):
          globtauHidx[0]=muHidx[0]
          globtauHidx[1]=tauHidx[0]
        elif (Category_tausel==2):
          globtauHidx[0]=eleHidx[0]
          globtauHidx[1]=tauHidx[0]
        elif (Category_tausel==3):
          globtauHidx[0]=tauHidx[0]
          globtauHidx[1]=tauHidx[1]
        elif (Category_lveto==4):
          globtauHidx[0]=muHidx[0]
          globtauHidx[1]=muHidx[1]
        elif (Category_lveto==5):
          globtauHidx[0]=eleHidx[0]
          globtauHidx[1]=eleHidx[1]
        elif (Category_lveto==6):
          globtauHidx[0]=eleHidx[0]
          globtauHidx[1]=muHidx[0]

        
        covMET_XX=MET.covXX
        covMET_XY=MET.covXY
        covMET_YY=MET.covYY
        measuredMETx=MET.pt*math.cos(MET.phi)
        measuredMETy=MET.pt*math.sin(MET.phi)
        index1=globtauHidx[0]
        index2=globtauHidx[1]
        
        if (index1>=0 and index2>=0 and Category_tausel==3):
            Category_pairs=3
            tautauMass=self.invMass(taus[index1],taus[index2])
            tautauPt,tautauEta,tautauPhi=self.PtEtaPhi(taus[index1],taus[index2])
            res=ROOT.SVfit_results( measuredMETx, measuredMETy, covMET_XX, covMET_XY, covMET_YY, 
                                    taus[index1].decayMode, taus[index2].decayMode, Category_pairs, 0, 
                                    taus[index1].pt,taus[index1].eta,taus[index1].phi,taus[index1].mass, 
                                    taus[index2].pt,taus[index2].eta,taus[index2].phi,taus[index2].mass )
            
            tautauPtSVFit   = res[0]
            tautauEtaSVFit  = res[1]
            tautauPhiSVFit  = res[2]
            tautauMassSVFit = res[3]
            
            selectedTau_ptSVFit[0]  = res[4]
            selectedTau_etaSVFit[0] = res[5]
            selectedTau_phiSVFit[0] = res[6]
            selectedTau_mSVFit[0]   = res[7]
            selectedTau_ptSVFit[1]  = res[8]
            selectedTau_etaSVFit[1] = res[9]
            selectedTau_phiSVFit[1] = res[10]
            selectedTau_mSVFit[1]   = res[11]
            
            tautaudRSVFit = deltaR(selectedTau_etaSVFit[0], selectedTau_phiSVFit[0], selectedTau_etaSVFit[1], selectedTau_phiSVFit[1])
            tautaudR = deltaR(taus[index1],taus[index2])
            
            ggtautaudR = deltaR(ggEta,tautauEta,ggPhi,tautauPhi)
            ggtautaudPhi = deltaPhi(ggPhi,tautauPhi)
            ggtautaudRSVFit = deltaR(ggEta,tautauEtaSVFit,ggPhi,tautauPhiSVFit)
            ggtautaudPhiSVFit = deltaPhi(ggPhi,tautauPhiSVFit)
            
        elif (index1>=0 and index2>=0 and Category_tausel==2):
            Category_pairs=2
            tautauMass=self.invMass(electrons[index1],taus[index2],0.511/1000.)
            tautauPt,tautauEta,tautauPhi=self.PtEtaPhi(electrons[index1],taus[index2],0.511/1000.)
            res=ROOT.SVfit_results( measuredMETx, measuredMETy, covMET_XX, covMET_XY, covMET_YY, 
                                    1, taus[index2].decayMode, Category_pairs, 0, 
                                    electrons[index1].pt,electrons[index1].eta,electrons[index1].phi,0.51100e-3,
                                    taus[index2].pt,taus[index2].eta,taus[index2].phi,taus[index2].mass)
            
            tautauPtSVFit   = res[0]
            tautauEtaSVFit  = res[1]
            tautauPhiSVFit  = res[2]
            tautauMassSVFit = res[3]
            
            selectedElectron_ptSVFit[0]  = res[4]
            selectedElectron_etaSVFit[0] = res[5]
            selectedElectron_phiSVFit[0] = res[6]
            selectedElectron_mSVFit[0]   = res[7]
            selectedTau_ptSVFit[0]  = res[8]
            selectedTau_etaSVFit[0] = res[9]
            selectedTau_phiSVFit[0] = res[10]
            selectedTau_mSVFit[0]   = res[11]
            
            tautaudRSVFit = deltaR(selectedTau_etaSVFit[0], selectedTau_phiSVFit[0], selectedTau_etaSVFit[1], selectedTau_phiSVFit[1])
            tautaudR = deltaR(electrons[index1],taus[index2])
            
            ggtautaudR = deltaR(ggEta,tautauEta,ggPhi,tautauPhi)
            ggtautaudPhi = deltaPhi(ggPhi,tautauPhi)
            ggtautaudRSVFit = deltaR(ggEta,tautauEtaSVFit,ggPhi,tautauPhiSVFit)
            ggtautaudPhiSVFit = deltaPhi(ggPhi,tautauPhiSVFit)
            
        elif (index1>=0 and index2>=0 and Category_tausel==1):
            Category_pairs=1
            tautauMass=self.invMass(muons[index1],taus[index2])
            tautauPt,tautauEta,tautauPhi=self.PtEtaPhi(muons[index1],taus[index2])
            res=ROOT.SVfit_results( measuredMETx, measuredMETy, covMET_XX, covMET_XY, covMET_YY, 
                                    1, taus[index2].decayMode, Category_pairs, 0, 
                                    muons[index1].pt,muons[index1].eta,muons[index1].phi,0.10566,
                                    taus[index2].pt,taus[index2].eta,taus[index2].phi,taus[index2].mass )
            
            tautauPtSVFit   = res[0]
            tautauEtaSVFit  = res[1]
            tautauPhiSVFit  = res[2]
            tautauMassSVFit = res[3]
            
            selectedMuon_ptSVFit[0]  = res[4]
            selectedMuon_etaSVFit[0] = res[5]
            selectedMuon_phiSVFit[0] = res[6]
            selectedMuon_mSVFit[0]   = res[7]
            selectedTau_ptSVFit[0]  = res[8]
            selectedTau_etaSVFit[0] = res[9]
            selectedTau_phiSVFit[0] = res[10]
            selectedTau_mSVFit[0]   = res[11]
            
            tautaudRSVFit = deltaR(selectedTau_etaSVFit[0], selectedTau_phiSVFit[0], selectedTau_etaSVFit[1], selectedTau_phiSVFit[1])
            tautaudR = deltaR(muons[index1],taus[index2])
            
            ggtautaudR = deltaR(ggEta,tautauEta,ggPhi,tautauPhi)
            ggtautaudPhi = deltaPhi(ggPhi,tautauPhi)
            ggtautaudRSVFit = deltaR(ggEta,tautauEtaSVFit,ggPhi,tautauPhiSVFit)
            ggtautaudPhiSVFit = deltaPhi(ggPhi,tautauPhiSVFit)
        
        # visible mass etc for leptonic categories
        if (index1>=0 and index2>=0 and Category_lveto==4):
            Category_tausel=4
            Category_pairs=4
            tautauMass=self.invMass(muons[index1],muons[index2])
            tautauPt,tautauEta,tautauPhi=self.PtEtaPhi(muons[index1],muons[index2])
            res=ROOT.SVfit_results( measuredMETx, measuredMETy, covMET_XX, covMET_XY, covMET_YY, 
                                    1, 1, 1, 1, 
                                    muons[index1].pt,muons[index1].eta,muons[index1].phi,0.10566,
                                    muons[index2].pt,muons[index2].eta,muons[index2].phi,0.10566 )
            
            tautauPtSVFit   = res[0]
            tautauEtaSVFit  = res[1]
            tautauPhiSVFit  = res[2]
            tautauMassSVFit = res[3]
            
            selectedMuon_ptSVFit[0]  = res[4]
            selectedMuon_etaSVFit[0] = res[5]
            selectedMuon_phiSVFit[0] = res[6]
            selectedMuon_mSVFit[0]   = res[7]
            selectedMuon_ptSVFit[1]  = res[8]
            selectedMuon_etaSVFit[1] = res[9]
            selectedMuon_phiSVFit[1] = res[10]
            selectedMuon_mSVFit[1]   = res[11]
            
            tautaudRSVFit = deltaR(selectedTau_etaSVFit[0], selectedTau_phiSVFit[0], selectedTau_etaSVFit[1], selectedTau_phiSVFit[1])
            tautaudR = deltaR(muons[index1],muons[index2])
            
            ggtautaudR = deltaR(ggEta,tautauEta,ggPhi,tautauPhi)
            ggtautaudPhi = deltaPhi(ggPhi,tautauPhi)
            ggtautaudRSVFit = deltaR(ggEta,tautauEtaSVFit,ggPhi,tautauPhiSVFit)
            ggtautaudPhiSVFit = deltaPhi(ggPhi,tautauPhiSVFit)

        elif (index1>=0 and index2>=0 and Category_lveto==5):
            Category_tausel=5
            Category_pairs=5
            tautauMass=self.invMass(electrons[index1],electrons[index2],0.511/1000.,0.511/1000.)
            tautauPt,tautauEta,tautauPhi=self.PtEtaPhi(electrons[index1],electrons[index2],0.511/1000.,0.511/1000.)
            res=ROOT.SVfit_results( measuredMETx, measuredMETy, covMET_XX, covMET_XY, covMET_YY, 
                                    1, 1, 2, 2, 
                                    electrons[index1].pt,electrons[index1].eta,electrons[index1].phi,0.51100e-3,
                                    electrons[index2].pt,electrons[index2].eta,electrons[index2].phi,0.51100e-3)
            
            tautauPtSVFit   = res[0]
            tautauEtaSVFit  = res[1]
            tautauPhiSVFit  = res[2]
            tautauMassSVFit = res[3]
            
            selectedElectron_ptSVFit[0]  = res[4]
            selectedElectron_etaSVFit[0] = res[5]
            selectedElectron_phiSVFit[0] = res[6]
            selectedElectron_mSVFit[0]   = res[7]
            selectedElectron_ptSVFit[1]  = res[8]
            selectedElectron_etaSVFit[1] = res[9]
            selectedElectron_phiSVFit[1] = res[10]
            selectedElectron_mSVFit[1]   = res[11]
            
            tautaudRSVFit = deltaR(selectedTau_etaSVFit[0], selectedTau_phiSVFit[0], selectedTau_etaSVFit[1], selectedTau_phiSVFit[1])
            tautaudR = deltaR(electrons[index1],electrons[index2])
            
            ggtautaudR = deltaR(ggEta,tautauEta,ggPhi,tautauPhi)
            ggtautaudPhi = deltaPhi(ggPhi,tautauPhi)
            ggtautaudRSVFit = deltaR(ggEta,tautauEtaSVFit,ggPhi,tautauPhiSVFit)
            ggtautaudPhiSVFit = deltaPhi(ggPhi,tautauPhiSVFit)

        elif (index1>=0 and index2>=0 and Category_lveto==6):
            Category_tausel=6
            Category_pairs=6
            tautauMass=self.invMass(electrons[index1],muons[index2],0.511/1000.)
            tautauPt,tautauEta,tautauPhi=self.PtEtaPhi(electrons[index1],muons[index2],0.511/1000.)
            res=ROOT.SVfit_results( measuredMETx, measuredMETy, covMET_XX, covMET_XY, covMET_YY, 
                                    1, 1, 2, 1, 
                                    electrons[index1].pt,electrons[index1].eta,electrons[index1].phi,0.51100e-3,
                                    muons[index2].pt,muons[index2].eta,muons[index2].phi,0.10566)
            
            tautauPtSVFit   = res[0]
            tautauEtaSVFit  = res[1]
            tautauPhiSVFit  = res[2]
            tautauMassSVFit = res[3]
            
            selectedElectron_ptSVFit[0]  = res[8]
            selectedElectron_etaSVFit[0] = res[9]
            selectedElectron_phiSVFit[0] = res[10]
            selectedElectron_mSVFit[0]   = res[11]
            selectedMuon_ptSVFit[1]  = res[4]
            selectedMuon_etaSVFit[1] = res[5]
            selectedMuon_phiSVFit[1] = res[6]
            selectedMuon_mSVFit[1]   = res[7]
            
            tautaudRSVFit = deltaR(selectedTau_etaSVFit[0], selectedTau_phiSVFit[0], selectedTau_etaSVFit[1], selectedTau_phiSVFit[1])
            tautaudR = deltaR(electrons[index1],muons[index2])
            
            ggtautaudR = deltaR(ggEta,tautauEta,ggPhi,tautauPhi)
            ggtautaudPhi = deltaPhi(ggPhi,tautauPhi)
            ggtautaudRSVFit = deltaR(ggEta,tautauEtaSVFit,ggPhi,tautauPhiSVFit)
            ggtautaudPhiSVFit = deltaPhi(ggPhi,tautauPhiSVFit)
            
        #jet filter flags addition
        for i in range(len(jets)):
            if (Category_pairs==3):
                if (deltaR(jets[i],taus[tauHidx[0]])<0.4):
                    jetFilterFlags[i]=False
                if (deltaR(jets[i],taus[tauHidx[1]])<0.4):
                    jetFilterFlags[i]=False
            elif (Category_pairs==2 or Category_pairs==1):
                if (deltaR(jets[i],taus[tauHidx[0]])<0.4):
                    jetFilterFlags[i]=False



          
        self.out.fillBranch("Jet_Filter"+self.postfix, jetFilterFlags)  
   
        self.out.fillBranch("Category_tausel"+self.postfix, Category_tausel)
        self.out.fillBranch("Category_pairs"+self.postfix, Category_pairs)
        
        self.out.fillBranch("pt_tautau"+self.postfix,  tautauPt);   
        self.out.fillBranch("eta_tautau"+self.postfix,  tautauEta); 
        self.out.fillBranch("phi_tautau"+self.postfix,  tautauPhi); 
        self.out.fillBranch("m_tautau"+self.postfix,  tautauMass); 
        self.out.fillBranch("dR_tautau"+self.postfix,  tautaudR);
        
        self.out.fillBranch("pt_tautauSVFit"+self.postfix,  tautauPtSVFit);   
        self.out.fillBranch("eta_tautauSVFit"+self.postfix,  tautauEtaSVFit); 
        self.out.fillBranch("phi_tautauSVFit"+self.postfix,  tautauPhiSVFit); 
        self.out.fillBranch("m_tautauSVFit"+self.postfix,  tautauMassSVFit); 
        self.out.fillBranch("dR_tautauSVFit"+self.postfix,  tautaudRSVFit);
        
        self.out.fillBranch("dR_ggtautau"+self.postfix,  ggtautaudR);
        self.out.fillBranch("dPhi_ggtautau"+self.postfix,  ggtautaudPhi);
        self.out.fillBranch("dR_ggtautauSVFit"+self.postfix,  ggtautaudRSVFit);
        self.out.fillBranch("dPhi_ggtautauSVFit"+self.postfix,  ggtautaudPhiSVFit);
        
        self.out.fillBranch("nselectedTau"+self.postfix, nSelTaus)
        
        self.out.fillBranch("selectedTau"+self.postfix+"_ptSVFit",  selectedTau_ptSVFit);   
        self.out.fillBranch("selectedTau"+self.postfix+"_etaSVFit",  selectedTau_etaSVFit); 
        self.out.fillBranch("selectedTau"+self.postfix+"_phiSVFit",  selectedTau_phiSVFit); 
        self.out.fillBranch("selectedTau"+self.postfix+"_mSVFit",  selectedTau_mSVFit);
        
        self.out.fillBranch("selectedMuon_ptSVFit",  selectedMuon_ptSVFit);   
        self.out.fillBranch("selectedMuon_etaSVFit",  selectedMuon_etaSVFit); 
        self.out.fillBranch("selectedMuon_phiSVFit",  selectedMuon_phiSVFit); 
        self.out.fillBranch("selectedMuon_mSVFit",  selectedMuon_mSVFit); 
        
        self.out.fillBranch("selectedElectron_ptSVFit",  selectedElectron_ptSVFit);   
        self.out.fillBranch("selectedElectron_etaSVFit",  selectedElectron_etaSVFit); 
        self.out.fillBranch("selectedElectron_phiSVFit",  selectedElectron_phiSVFit); 
        self.out.fillBranch("selectedElectron_mSVFit",  selectedElectron_mSVFit); 
        
        return True
    
    
    
HHggtautauModule2016LL = lambda : HHggtautauProducer(jetSelection= lambda j : j.pt > 15, muSelection= lambda mu : mu.pt > 9, eSelection= lambda e : e.pt > 9, data = False, year="2016", hadtau1="Loose", hadtau2="Loose") 
HHggtautauModule2017LL = lambda : HHggtautauProducer(jetSelection= lambda j : j.pt > 15, muSelection= lambda mu : mu.pt > 9, eSelection= lambda e : e.pt > 9, data = False, year="2017", hadtau1="Loose", hadtau2="Loose") 
HHggtautauModule2018LL = lambda : HHggtautauProducer(jetSelection= lambda j : j.pt > 15, muSelection= lambda mu : mu.pt > 9, eSelection= lambda e : e.pt > 9, data = False, year="2018", hadtau1="Loose", hadtau2="Loose") 

HHggtautauModule2016MM = lambda : HHggtautauProducer(jetSelection= lambda j : j.pt > 15, muSelection= lambda mu : mu.pt > 9, eSelection= lambda e : e.pt > 9, data = False, year="2016", hadtau1="Medium", hadtau2="Medium") 
HHggtautauModule2017MM = lambda : HHggtautauProducer(jetSelection= lambda j : j.pt > 15, muSelection= lambda mu : mu.pt > 9, eSelection= lambda e : e.pt > 9, data = False, year="2017", hadtau1="Medium", hadtau2="Medium") 
HHggtautauModule2018MM = lambda : HHggtautauProducer(jetSelection= lambda j : j.pt > 15, muSelection= lambda mu : mu.pt > 9, eSelection= lambda e : e.pt > 9, data = False, year="2018", hadtau1="Medium", hadtau2="Medium") 

HHggtautauModule2016LVVV = lambda : HHggtautauProducer(jetSelection= lambda j : j.pt > 15, muSelection= lambda mu : mu.pt > 9, eSelection= lambda e : e.pt > 9, data = False, year="2016", hadtau1="Loose", hadtau2="VVVLoose") 
HHggtautauModule2017LVVV = lambda : HHggtautauProducer(jetSelection= lambda j : j.pt > 15, muSelection= lambda mu : mu.pt > 9, eSelection= lambda e : e.pt > 9, data = False, year="2017", hadtau1="Loose", hadtau2="VVVLoose") 
HHggtautauModule2018LVVV = lambda : HHggtautauProducer(jetSelection= lambda j : j.pt > 15, muSelection= lambda mu : mu.pt > 9, eSelection= lambda e : e.pt > 9, data = False, year="2018", hadtau1="Loose", hadtau2="VVVLoose") 

