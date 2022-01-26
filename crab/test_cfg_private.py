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
#config.Data.inputDBS = 'global'

datasets=[
  
["/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_0.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_1.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_2.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_3.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_4.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_5.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_6.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_7.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_8.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_9.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_10.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_11.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_12.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_13.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_14.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_15.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_16.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_17.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_18.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_19.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_20.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_21.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_22.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_23.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_24.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSOSWWH_incl_C2V_3_Azure_v1/merged/output_25.root",],

["/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_0.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_1.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_2.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_3.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_4.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_5.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_6.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_7.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_8.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_9.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_10.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_11.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_12.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_13.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_14.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_15.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_16.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_17.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_18.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_19.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_20.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_21.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_22.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_23.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_24.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWWH_incl_v2_C2V_3_Azure/merged/output_25.root",],

["/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_0.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_1.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_2.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_3.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_4.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_5.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_6.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_7.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_8.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_9.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_10.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_11.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_12.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_13.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_14.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_15.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_16.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_17.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_18.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_19.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_20.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_21.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_22.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_23.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_24.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSWZH_incl_C2V_3_Azure_v1/merged/output_25.root",],

["/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_0.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_1.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_2.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_3.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_4.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_5.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_6.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_7.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_8.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_9.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_10.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_11.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_12.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_13.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_14.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_15.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_16.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_17.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_18.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_19.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_20.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_21.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_22.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_23.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_24.root",
"/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_25.root",]

]


#config.Data.outputPrimaryDataset = "VBSHWWSignalGeneration" #override

config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 5 
#config.Data.totalUnits = 20 #override

config.Data.outLFNDirBase = '/store/user/legianni/skimNanoVVH-Hadronic'+version # cannot getUsernameFromSiteDB
config.Data.publication = False
config.Data.outputDatasetTag = 'skimNano-VVH'+version


config.section_("Site")
config.Site.storageSite = "T2_US_UCSD"
config.Site.whitelist = ["T2_US_UCSD"] # i know where the files are!!!!

from CRABAPI.RawCommand import crabCommand

#from https://github.com/cmstas/HggAnalysisDev/tree/main/Skimming
#import sys
#sys.path.append(base+"/..//HggAnalysisDev/Skimming")
#from sa import *
#from allsamples import allsamples

config.JobType.scriptArgs=["arg=mc16"]


#config.Data.userInputFiles=files
#config.Data.totalUnits = len(files)

count=43

for d in datasets:
  files=d
  config.Data.userInputFiles=d
  config.Data.totalUnits = len(d)
  
  name=files[0]
  config.Data.outputDatasetTag='skimNano-VVH'+version
  config.Data.outputPrimaryDataset = name.split("/")[-3]
  config.General.requestName = 'skimNano-'+name.split("/")[-3]+"____"+str(count)
  count+=1
  
  print "Submitting ", "nfiles ", len(files), "found at",  files[0:1], " extra ARG ", config.JobType.scriptArgs
  print config
  crabCommand('submit', config = config, dryrun = False) ## dryrun = True for local test
  print "DONE"

