#from WMCore.Configuration import Configuration
#from CRABClient.UserUtilities import config #getUsernameFromSiteDB
from CRABClient.UserUtilities import config as Configuration

version="__v1"

import os 
base = os.environ["CMSSW_BASE"]

config = Configuration()

config.section_("General")
config.General.requestName = 'skimNano-testVVH999999999'
config.General.transferLogs = True
 
config.General.workArea = base+'/..'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_VVH.sh'
#config.JobType.scriptArgs= "foo"
# hadd nano will not be needed once nano tools are in cmssw
config.JobType.inputFiles = ['crab_script_VVH.py', '../scripts/haddnano.py', 'keep_and_drop.txt',
"../NanoTools/NanoCORE/libNANO_CORE.so","../NanoTools/NanoCORE/Config.h","../NanoTools/NanoCORE/TauSelections.h","../NanoTools/NanoCORE/MuonSelections.h","../NanoTools/NanoCORE/ElectronSelections.h","../NanoTools/NanoCORE/Nano.h","../NanoTools/NanoCORE/Base.h"
]
config.JobType.sendPythonFolder = True

config.JobType.allowUndistributedCMSSW = True #shouldn't be necessary

config.section_("Data")
#config.Data.inputDataset = '/DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'

datasets=[
"/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
"/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",

"/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
"/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
"/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
"/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
"/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",

"/WJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
"/WJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
"/WJetsToQQ_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
"/WJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",

"/ZJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
"/ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
"/ZJetsToQQ_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
"/ZJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM"

]

#datasets=[
#"/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
#]

#config.Data.outputPrimaryDataset = "VBSHWWSignalGeneration" #override

config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 20
#config.Data.totalUnits = 20 #override

config.Data.outLFNDirBase = '/store/user/legianni/skimNanoVVH-Hadronic'+version # cannot getUsernameFromSiteDB
config.Data.publication = False
config.Data.outputDatasetTag = 'skimNano-VVH'+version


config.section_("Site")
config.Site.storageSite = "T2_US_UCSD"
#config.Site.whitelist = ["T2_US_UCSD"] # i know where the files are!!!!

from CRABAPI.RawCommand import crabCommand

#from https://github.com/cmstas/HggAnalysisDev/tree/main/Skimming
#import sys
#sys.path.append(base+"/..//HggAnalysisDev/Skimming")
#from sa import *
#from allsamples import allsamples

config.JobType.scriptArgs=["arg=mc16"]


#config.Data.userInputFiles=files
#config.Data.totalUnits = len(files)

count=33

for d in datasets:
 config.Data.outputDatasetTag = 'skimNano-VVH'+version
 config.Data.inputDataset = d
 config.General.requestName = 'skimNano-'+d.split("/")[1]+"____"+str(count)
 count+=1
 print "Submitting ", "nfiles ", d, "found ",  " extra ARG ", config.JobType.scriptArgs
 print config
 crabCommand('submit', config = config, dryrun = False) ## dryrun = True for local test
 print "DONE"

