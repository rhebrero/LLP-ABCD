using namespace ROOT::VecOps;
using Vint = ROOT::VecOps::RVec<int>;
using Vfloat = ROOT::VecOps::RVec<float>;
#include "TString.h"
#include "TTree.h"
#include "TTreeFormula.h"
// #include <vector>


Vfloat copyVFloat(
    Vfloat  mu_values
) {
    return mu_values;
};

Vint copyVInt(
    Vint  mu_values
) {
    return mu_values;
};

float copyFloat(
    Vfloat  mu_values
) {
    return mu_values[0];
};

int copyInt(
    Vint  mu_values
) {
    return mu_values[0];
};