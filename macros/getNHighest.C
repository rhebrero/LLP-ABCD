using namespace ROOT::VecOps;
using Vint = ROOT::VecOps::RVec<int>;
using Vfloat = ROOT::VecOps::RVec<float>;
#include "TString.h"
#include "TTree.h"
#include "TTreeFormula.h"
#include <vector>



Vint getNHighest(
    Vfloat  mu_values,
    Vint    mu_idx,
    int     NHighest,
    bool    doAbs
) {

    // Inicializamos las variables
        Vfloat selectedValues;
        for (auto jMu : mu_idx) {selectedValues.push_back(mu_values[jMu]);}
        if (doAbs) {
            selectedValues = abs(selectedValues);
        }


        Vfloat sortedValues = Sort(selectedValues, [](double x, double y) {return 1/x < 1/y;});
        Vint passingMu;


    // Miramos si pasan el corte
        for (auto iHighest=0; iHighest < NHighest; ++iHighest) {

            for (auto jMu = 0; jMu < selectedValues.size(); ++jMu) {
                if ( sortedValues[iHighest] == selectedValues[jMu] ) {
                    //No hagas nada si no pasa el corte
                        passingMu.push_back(mu_idx[jMu]);
                }else{
                    //Guardar el índice del muon
                }
            }
        }
        
    

    return passingMu;
};