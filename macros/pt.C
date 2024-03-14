using namespace ROOT::VecOps;
using Vint      = ROOT::VecOps::RVec<int>;
using Vfloat    = ROOT::VecOps::RVec<float>;
using Vdouble   = ROOT::VecOps::RVec<double>;
#include <iostream>
#include "TTree.h"
#include "TTreeFormula.h"
#include "TMath.h" // Incluir la biblioteca TMath de ROOT
// #include <vector>


Vfloat pt(
    vector<double>  px,
    vector<double>  py,
    unsigned int nMuons
) {

    Vfloat pt;
    TLorentzVector p;

    for (unsigned int i = 0; i < nMuons; ++i) {
        p.SetPxPyPzE(px[i],py[i],0.0,0.0);
        pt.push_back(p.Pt());
    }
    return pt;
}