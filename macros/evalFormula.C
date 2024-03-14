using Vbool = ROOT::VecOps::RVec<bool>;
using Vfloat = ROOT::VecOps::RVec<float>;
using Vint = ROOT::VecOps::RVec<int>;
#include <map>
#include "TString.h"
#include "TTree.h"
#include "TTreeFormula.h"
#include <iostream>

Vint evalFormula(
    TTreeFormula *formula
) {

    // Inicializamos las variables 
        Vint passingMu;
        
    
    // Almacenamos el valor lógico de cada uno
        for (unsigned int i=0; i < formula -> GetNdata(); ++i) {
                passingMu.push_back(formula -> EvalInstance(i));

        }

    return passingMu;
};
