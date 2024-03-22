using namespace ROOT::VecOps;
using Vint = ROOT::VecOps::RVec<int>;
using Vfloat = ROOT::VecOps::RVec<float>;
#include "TString.h"
#include "TTree.h"
#include "TTreeFormula.h"
// #include <vector>
#include <iostream>


Vint getNHighest_fromIdx(
    Vfloat  mu_values,
    Vint    mu_idx,
    int     NHighest,
    bool    doAbs
) {
    // Initialize variables
        Vfloat selectedValues;
        Vfloat sortedValues;
        Vint passingMu;

    if (mu_idx.size() == 0) {return passingMu;} // In case no muon to select
    
    // Inicializamos las variables
        for (auto jMu : mu_idx) {selectedValues.push_back(mu_values[jMu]);}
        
    // En caso de quere usar el valor absoluto para comparar
        if (doAbs) {
            sortedValues = Sort(selectedValues, [](double x, double y) {return abs(1/x) < abs(1/y);});
        } else {
            sortedValues = Sort(selectedValues, [](double x, double y) {return 1/x < 1/y;});
        }
        


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



Vint getNHighest(
    Vfloat  mu_values,
    int     NHighest,
    bool    doAbs
) {

    // Creamos un vector de índices
        Vint mu_idx;
        for (auto i=0; i< mu_values.size();++i) {mu_idx.push_back(i);};
    
    // Evaluamos
        Vint passingMu = getNHighest_fromIdx(mu_values,mu_idx,NHighest,doAbs);
        return passingMu;

};

Vint getNHighest_fromMask(
    Vfloat  mu_values,
    Vint    mask,
    int     NHighest,
    bool    doAbs
) {

    // Creamos un vector de índices
        Vint mu_idx;
        for (auto i=0; i< mu_values.size();++i) {if (mask[i] == 1) {mu_idx.push_back(i);}};
    
    // Evaluamos
        Vint passingMu = getNHighest_fromIdx(mu_values,mu_idx,NHighest,doAbs);
        return passingMu;

};

Vint getNHighest_fromBranch(
    Vint    mu_idx,
    int     NHighest
) {


    // Creamos un vector de índices
        Vint mu_selectedIdx;
        int nPassing = mu_idx.size();
        // std::cout << NHighest << " primeros elementos de un vector de tamaño " << nPassing << std::endl;

        for (int i=0; i< NHighest;++i) {
            if (i < nPassing) {
                // std::cout << i << " : " << mu_idx[i] << std::endl;
                mu_selectedIdx.push_back(mu_idx[i]);
            } else {
                // std::cout << i << " : -999" << std::endl;
                mu_selectedIdx.push_back(-999);
            }
        };
        return mu_selectedIdx;

};