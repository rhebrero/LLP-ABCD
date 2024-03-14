using Vbool = ROOT::VecOps::RVec<bool>;
using Vfloat = ROOT::VecOps::RVec<float>;
using Vint = ROOT::VecOps::RVec<int>;
#include "TString.h"
#include "TFormula.h"
#include <iostream>

Vint isPrompt(
    Vfloat  d0          ,
    Vfloat  d0sig       ,
    float   cut_d0      ,
    float   cut_d0sig
) {

    // Inicializamos las variables 
        Vint passingMu;
        unsigned int nMuons = d0.size();
        int result;

    // Almacenamos el valor lógico de cada uno
        for (unsigned int i=0; i < nMuons; ++i) {
            result =    (d0[i]      <= cut_d0    ) ||
                        (d0sig[i]   <= cut_d0sig );

            passingMu.push_back(result);
        }

    return passingMu;
};