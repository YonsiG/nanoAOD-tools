#include "PhysicsTools/NanoAODTools/interface/PyJetResolutionWrapper.h"
#include "PhysicsTools/NanoAODTools/interface/PyJetResolutionScaleFactorWrapper.h"
#include "PhysicsTools/NanoAODTools/interface/PyJetParametersWrapper.h"
#include "PhysicsTools/NanoAODTools/interface/WeightCalculatorFromHistogram.h"
#include "PhysicsTools/NanoAODTools/interface/ReduceMantissa.h"
#include "PhysicsTools/NanoAODTools/interface/EnergyScaleCorrection.h"
#include "PhysicsTools/NanoAODTools/interface/SVFitFunc.h"

PyJetResolutionWrapper jetRes;
PyJetResolutionScaleFactorWrapper jetResScaleFactor;
PyJetParametersWrapper jetParams;
WeightCalculatorFromHistogram wcalc;
ReduceMantissaToNbitsRounding red(12);
EnergyScaleCorrection PhotonScaleEGM;
SVFitFunc svfitfunc;
