#ifndef PhysicsTools_NanoAODTools_SVFitFunc_h
#define PhysicsTools_NanoAODTools_SVFitFunc_h

#include "TauAnalysis/ClassicSVfit/interface/ClassicSVfit.h"
#include "TauAnalysis/ClassicSVfit/interface/MeasuredTauLepton.h"
#include "TauAnalysis/ClassicSVfit/interface/svFitHistogramAdapter.h"
#include "TauAnalysis/ClassicSVfit/interface/FastMTT.h"
#include <vector>

//helper function called to compute the SVfit mass in events with tau candidates
//needs library https://github.com/SVfit/ClassicSVfit/tree/fastMTT_19_02_2019 (updated branch fastMTT_19_02_2019) and https://github.com/SVfit/SVfitTF
//tested under cmssw

using namespace classic_svFit;

class SVFitFunc
{
public:
SVFitFunc(int = 0);
~SVFitFunc();

std::vector<double> SVfit_results(float measuredMETx, float measuredMETy, float covMET_XX, float covMET_XY, float covMET_YY,int tauDecay_mode1, int tauDecay_mode2, int category1, int category2, float tau1_pt,float  tau1_eta, float tau1_phi, float tau1_mass, float tau2_pt, float tau2_eta, float tau2_phi, float tau2_mass);

};

#endif
