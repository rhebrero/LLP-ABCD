using Vbool = ROOT::VecOps::RVec<bool>;
using Vfloat = ROOT::VecOps::RVec<float>;
using Vint = ROOT::VecOps::RVec<int>;
#include "TString.h"
#include "TFormula.h"
#include <iostream>

Vint isGood(
    Vint    nMatchedStations        ,
    Vint    nTrackerLayers          ,
    Vfloat  pt                      ,
    Vfloat  ptError                 ,
    int     cut_nMatchedStations    ,
    int     cut_nTrackerLayers      ,
    float   cut_pt                  ,
    float   cut_ptRelError
) {

    // Inicializamos las variables 
        Vint passingMu;
        unsigned int nMuons = pt.size();
        int result;

    // Almacenamos el valor lógico de cada uno
        for (unsigned int i=0; i < nMuons; ++i) {
            result =    (nMatchedStations[i]    > cut_nMatchedStations  ) &&
                        (nTrackerLayers[i]      > cut_nTrackerLayers    ) &&
                        (pt[i]                  > cut_pt                ) &&
                        (ptError[i]/pt[i]       < cut_ptRelError        );

            passingMu.push_back(result);
        }

    return passingMu;
};