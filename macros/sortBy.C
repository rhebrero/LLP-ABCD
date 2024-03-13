using namespace ROOT::VecOps;
using Vint = ROOT::VecOps::RVec<int>;
using Vfloat = ROOT::VecOps::RVec<float>;
#include "TString.h"
#include "TTree.h"
#include "TTreeFormula.h"
// #include <vector>


Vint sortBy_fromIdx(
    Vfloat  mu_values,
    Vint    mu_idx,
    bool    doAbs
) {

    // Inicializamos las variables
        Vfloat selectedValues;
        for (auto jMu : mu_idx) {selectedValues.push_back(mu_values[jMu]);}

    // En caso de quere usar el valor absoluto para comparar
        Vfloat sortedValues;
        if (doAbs) {
            sortedValues = Sort(selectedValues, [](double x, double y) {return abs(1/x) < abs(1/y);});
        } else {
            sortedValues = Sort(selectedValues, [](double x, double y) {return 1/x < 1/y;});
        }

        
        Vint passingMu;
        unsigned int nMuons = mu_idx.size();

    // Miramos si pasan el corte
        for (auto iHighest=0; iHighest < nMuons; ++iHighest) {

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



Vint sortBy(
    Vfloat  mu_values,
    bool    doAbs
) {

    // Creamos un vector de índices
        Vint mu_idx;
        for (auto i=0; i< mu_values.size();++i) {mu_idx.push_back(i);};
    
    // Evaluamos
        Vint passingMu = sortBy_fromIdx(mu_values,mu_idx,doAbs);
        return passingMu;

};

Vint sortBy_fromMask(
    Vfloat  mu_values,
    Vint    mask,
    bool    doAbs
) {

    // Creamos un vector de índices
        Vint mu_idx;
        for (auto i=0; i< mu_values.size();++i) {if (mask[i] == 1) {mu_idx.push_back(i);}};
    
    // Evaluamos
        Vint passingMu = sortBy_fromIdx(mu_values,mu_idx,doAbs);
        return passingMu;

};

Vint sortBy_fromCut(
    TTree   *tree,
    char    *cutString,
    Vfloat  mu_values,
    bool    doAbs
) {
        TTreeFormula *formula = new TTreeFormula("selection",cutString,tree);
    // Creamos un vector de índices
        Vint mu_idx;
        for (auto i=0; i< mu_values.size();++i) {if (formula -> EvalInstance(i) == 1) {mu_idx.push_back(i);}};
    
    // Evaluamos
        Vint passingMu = sortBy_fromIdx(mu_values,mu_idx,doAbs);

        delete formula;
        return passingMu;

};