#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *

#this would take care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from  PhysicsTools.NanoAODTools.postprocessing.examples.exampleModule import *

from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *

from  PhysicsTools.NanoAODTools.postprocessing.examples.skimModule import *

#very basic selection which is covered then by the actual Hgg selection and crop at 1000 evts
selection='''1'''

import sys
print sys.argv

#work on a local file
# a modified nanoAOD which contians extra phton features -> to be merged soon to the central stuff
files=["/hadoop/cms/store/user/phchang/VBSHWWSignalGeneration/RunIISummer20UL18_VBSZZH_incl_C2V_3_Azure_v1/merged/output_0.root"]

#2016 modules MC
#jetmetUncertainties2016, puAutoWeight_2016, muonScaleRes2016, PrefCorr2016
PrefCorr2016 = lambda : PrefCorr("L1prefiring_jetpt_2016BtoH.root", "L1prefiring_jetpt_2016BtoH", "L1prefiring_photonpt_2016BtoH.root", "L1prefiring_photonpt_2016BtoH")

#2017 modules MC
#jetmetUncertainties2017, puAutoWeight_2017, muonScaleRes2017, PrefireCorr2017
PrefireCorr2017 = lambda : PrefCorr('L1prefiring_jetpt_2017BtoF.root', 'L1prefiring_jetpt_2017BtoF', 'L1prefiring_photonpt_2017BtoF.root', 'L1prefiring_photonpt_2017BtoF')

#2018 modules MC
#jetmetUncertainties2018, puAutoWeight_2018, muonScaleRes2018


p = PostProcessor(".", 
                    inputFiles(), #NOT IN LOCAL
                    selection.replace('\n',''),
                    branchsel="keep_and_drop.txt",
                    outputbranchsel="keep_and_drop.txt",
                    modules=[vbsHwwSkimProducer_hadronic()],
                    provenance=True,
                    fwkJobReport=True, #NOT IN LOCAL
                    jsonInput=runsAndLumis() #NOT IN LOCAL
                    )
#NB the gammaWeightSF needs a gg selection as of now, while gammaSF is not related to a gg pair
# as a result HggModule2018() must be run before gammaWeightSF()

# keep and drop printout
print p.branchsel._ops
print p.outputbranchsel._ops

print "bo"

p.run()

print("DONE")
