using Vbool = ROOT::VecOps::RVec<bool>;
using Vfloat = ROOT::VecOps::RVec<float>;
using Vint = ROOT::VecOps::RVec<int>;
#include <map>
#include "TString.h"
#include "TTree.h"
#include "TTreeFormula.h"



Vint selectionMask(
    char        *cutString,
    TTree       *tree
) {

    // Inicializamos las variables 
        TTreeFormula* formula = new TTreeFormula("selection",cutString,tree);
        Vint passingMu;
        unsigned int muSize = formula -> GetNdata();


    // Miramos si pasan el corte
        for (unsigned int i=0; i < muSize; ++i) {
            if ( formula -> EvalInstance(i) == 0 ) {
                //No hagas nada si no pasa el corte
            }else{
                //Guardar el índice del muon
                passingMu.push_back(i);
            }
        }
    

    return passingMu;
};