using namespace ROOT::VecOps;
using Vint = ROOT::VecOps::RVec<int>;
using Vfloat = ROOT::VecOps::RVec<float>;
#include "TString.h"
#include "TTree.h"
#include "TTreeFormula.h"
// #include <vector>


auto getNHighest_fromIdx(
    Vfloat  mu_values,
    int     NIdx
) {
    return mu_values[NIdx];
};
