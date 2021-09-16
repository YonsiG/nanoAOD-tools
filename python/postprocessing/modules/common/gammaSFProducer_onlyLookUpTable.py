#look up table systematics for photons

import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 

import json,array

class gammaSFProducer(Module):
    def __init__(self, sysnames=["Material", "ShowerShape", "FNU"], sysweights=["electronVeto", "presel", "looseMva"]):
        #load helper modules if any
        #load data files
        self.sysnames=sysnames
        self.sysweights=sysweights
        with open('%s/src/PhysicsTools/NanoAODTools/data/egamma/data_pho.txt' % os.environ['CMSSW_BASE'] ) as json_file:
            self.data = json.load(json_file)
        with open('%s/src/PhysicsTools/NanoAODTools/data/egamma/data_weight.txt' % os.environ['CMSSW_BASE'] ) as json_file2:
            self.data2 = json.load(json_file2)

        #THIS COULD redo EGM correction, but not smear ??
        #self.EGMCorrector=ROOT.EnergyScaleCorrection("PhysicsTools/NanoAODTools/data/egamma/ScalesSmearings/Run2018_Step2Closure_CoarseEtaR9Gain_v2")
        # check if necessary
 
    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        for sys in self.sysnames:
            for ud in ["Up", "Down"]:
                self.out.branch("Photon_pt"+sys+ud, "F", lenVar="nPhoton")
        for sys in self.sysweights:
            for ud in ["Up", "Down", "Central"]:
                self.out.branch("Photon_"+sys+"Weight"+ud, "F", lenVar="nPhoton")
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def getSFUpDown(self, sys, values):
        info=self.data[sys]
        bins=info['bins']
        indexbin=-1

        for i in range(len(values)):
            var1=values[i]
            bins=info['bins'][i]            
            for j in range(max(indexbin,0),len(bins)):
                if var1<max(bins[j]) and var1>=min(bins[j]):
                    indexbin=j
                    break
                
        if indexbin>=0:
            return info["uncertainties"][j]
        else:
            return 0

    def getSFCentralUpDown(self, sys, values):
         info=self.data2[sys+"Bins"]
         bins=info['bins']
         indexbin=-1
 
         for i in range(len(values)):
             var1=values[i]
             bins=info['bins'][i]
             for j in range(max(indexbin,0),len(bins)):
                 if var1<max(bins[j]) and var1>=min(bins[j]):
                     indexbin=j
                     break
 
         if indexbin>=0:
             return info["values"][j], info["uncertainties"][j]
         else:
             return 1,0

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        photons = Collection(event, "Photon")
        run = getattr(event, "run") 
        
        pts=np.array([pho.pt for pho in photons])
        
        for sys in self.sysnames:
            if sys=="Material":
                sf_photons = np.array([ self.getSFUpDown("materialBinsMoriond17",[pho.eta,pho.r9]) for pho in photons])
                pt_up=pts*(1+sf_photons)
                pt_down=pts*(1-sf_photons)
                self.out.fillBranch("Photon_pt"+sys+"Up", pt_up)
                self.out.fillBranch("Photon_pt"+sys+"Down", pt_down)
            elif sys=="FNU":
                sf_photons = np.array([ self.getSFUpDown("FNUFBins",[pho.eta,pho.r9]) for pho in photons])
                pt_up=pts*(1+sf_photons)
                pt_down=pts*(1-sf_photons)
                self.out.fillBranch("Photon_pt"+sys+"Up", pt_up)
                self.out.fillBranch("Photon_pt"+sys+"Down", pt_down)
            elif sys=="ShowerShape":
                sf_photons = np.array([ self.getSFUpDown("showerShapeBins",[abs(pho.eta),pho.r9]) for pho in photons])
                pt_up=pts*(1+sf_photons)
                pt_down=pts*(1-sf_photons)
                self.out.fillBranch("Photon_pt"+sys+"Up", pt_up)
                self.out.fillBranch("Photon_pt"+sys+"Down", pt_down)
            else:
                print "ANOTHER TYPE"
            
        for sys in self.sysweights:
            
            if sys=="electronVeto":
              
              ws=np.array([1.0 for pho in photons])
              wsUp=np.array([1.0 for pho in photons])
              wsDown=np.array([1.0 for pho in photons])

              for i in range(len(photons)):
                pho=photons[i]
                photon_SCeta=pho.isScEtaEB+2*pho.isScEtaEE
                photon_r9=pho.r9
                SFCentralUpDown1=self.getSFCentralUpDown(sys, [photon_SCeta,photon_r9])
                
                ws[i]*=SFCentralUpDown1[0]
                wsUp[i]*=(SFCentralUpDown1[0]+SFCentralUpDown1[1])
                wsDown[i]*=(SFCentralUpDown1[0]-SFCentralUpDown1[1])
                
              self.out.fillBranch("Photon_"+sys+"WeightCentral", ws)
              self.out.fillBranch("Photon_"+sys+"WeightUp", wsUp)
              self.out.fillBranch("Photon_"+sys+"WeightDown", wsDown)
                
            elif sys=="presel":
              
              ws=np.array([1.0 for pho in photons])
              wsUp=np.array([1.0 for pho in photons])
              wsDown=np.array([1.0 for pho in photons])

              for i in range(len(photons)):
                pho=photons[i]
                photon_SCeta=pho.isScEtaEB+2*pho.isScEtaEE
                photon_r9=pho.r9
                SFCentralUpDown1=self.getSFCentralUpDown(sys, [photon_SCeta,photon_r9])
                
                ws[i]*=SFCentralUpDown1[0]
                wsUp[i]*=(SFCentralUpDown1[0]+SFCentralUpDown1[1])
                wsDown[i]*=(SFCentralUpDown1[0]-SFCentralUpDown1[1])
                
              self.out.fillBranch("Photon_"+sys+"WeightCentral", ws)
              self.out.fillBranch("Photon_"+sys+"WeightUp", wsUp)
              self.out.fillBranch("Photon_"+sys+"WeightDown", wsDown)
              
            elif sys=="looseMva":
              
              ws=np.array([1.0 for pho in photons])
              wsUp=np.array([1.0 for pho in photons])
              wsDown=np.array([1.0 for pho in photons])

              for i in range(len(photons)):
                pho=photons[i]
                photon_SCeta=pho.isScEtaEB+2*pho.isScEtaEE
                photon_r9=pho.r9
                SFCentralUpDown1=self.getSFCentralUpDown(sys, [photon_SCeta,photon_r9])
                
                ws[i]*=SFCentralUpDown1[0]
                wsUp[i]*=(SFCentralUpDown1[0]+SFCentralUpDown1[1])
                wsDown[i]*=(SFCentralUpDown1[0]-SFCentralUpDown1[1])
                
              self.out.fillBranch("Photon_"+sys+"WeightCentral", ws)
              self.out.fillBranch("Photon_"+sys+"WeightUp", wsUp)
              self.out.fillBranch("Photon_"+sys+"WeightDown", wsDown)
                 
            else:
                print "ANOTHER TYPE"

        
        
        return True


gammaSFL = lambda : gammaSFProducer(sysnames=["Material", "ShowerShape", "FNU"], sysweights=["electronVeto", "presel", "looseMva"])

        
    
    

