using namespace ROOT::VecOps;
using Vint = ROOT::VecOps::RVec<int>;
using Vfloat = ROOT::VecOps::RVec<float>;
#include "TString.h"
#include "TTree.h"
#include "TTreeFormula.h"
// #include <vector>



Vint getNLowest_fromIdx(
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


        Vfloat sortedValues = Sort(selectedValues);
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

Vint getNLowest(
    Vfloat  mu_values,
    int     NHighest,
    bool    doAbs
) {

    // Creamos un vector de índices
        Vint mu_idx;
        for (auto i=0; i< mu_values.size();++i) {mu_idx.push_back(i);};
    
    // Evaluamos
        Vint passingMu = getNLowest_fromIdx(mu_values,mu_idx,NHighest,doAbs);
        return passingMu;
        
    

    return passingMu;
};